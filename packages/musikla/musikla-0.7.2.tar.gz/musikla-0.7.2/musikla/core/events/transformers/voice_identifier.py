from .transformer import Transformer
from musikla.core import Voice
from musikla.core.events import MusicEvent, NoteEvent, RestEvent, ChordEvent, DurationEvent
from typing import List, Optional, Tuple

class SlidingAverage():
    def __init__ ( self, capacity : int = 0 ):
        self.history : List[float] = []
        self.capacity = capacity
        self.sum : float = 0
        self.count : int = 0

    def __iadd__ ( self, value : float ):
        if self.count == 0:
            self.sum = value
            self.count = 1

            if self.capacity > 0:
                self.history.append( value )
        else:
            #  ( ( self.average / self.count ) + ( value / ( self.count + 1 ) ) )
            self.sum += value

            if self.capacity == 0 or self.count < self.capacity:
                self.count += 1
            else:
                self.sum -= self.history.pop( 0 )

            if self.capacity > 0:
                self.history.append( value )

        return self

    def __int__ ( self ):
        if self.count == 0:
            return 0

        return int( self.sum / self.count )
        
    def __float__ ( self ):
        if self.count == 0:
            return 0

        return float( self.sum / self.count )

class VoiceIdentifierVoice():
    def __init__ ( self, transformer : 'VoiceIdentifierTransformer', parent : Voice, index : int, staff : int = None ):
        self.transformer : VoiceIdentifierTransformer = transformer
        self.parent_name : str = parent.name
        self.parent_staff : Optional[int] = staff
        self.voice : Voice = parent.clone( parent.name + '/' + str( index ) )
        self.index = index
        self.average_pitch : SlidingAverage = SlidingAverage()
        self.auto_create_rests : bool = True
        self.auto_create_end_rests : bool = True
        self.last_event : Optional[MusicEvent] = None

    @property
    def last_timestamp ( self ):
        if self.last_event is None:
            return 0

        return self.last_event.timestamp
    
    @property
    def last_end_timestamp ( self ):
        if not self.last_event:
            return 0

        return self.last_event.end_timestamp
    
    @property
    def last_duration ( self ):
        if not self.last_event:
            return 0

        return self.last_event.duration

    def overlap_percentages ( self, timestamp : int, duration : int ) -> Tuple[float, float]:
        """
        This function returns two values, both between 0 and 1, that represent
        how much of each event is overlapping. For example, if the overlap is of
        50ms, and last event lasted 200ms, while the new event lasts 100ms.
        The result of this function would be (0.25, 0.5), which means 25% and 50%
        respectively.

        It should be called only when self.last_end_timestamp > timestamp
        """

        overlap_dur = self.last_end_timestamp - timestamp

        # When last_duration is == 0, we consider the overlapping percentage
        # to be 1, which means 100%
        overlap_perc1 = overlap_dur / self.last_duration if self.last_duration > 0 else 1

        overlap_perc2 = overlap_dur / duration if duration > 0 else 1

        return (overlap_perc1, overlap_perc2)

    def is_busy_at ( self, timestamp : int, duration : int = None ) -> bool:
        if self.last_end_timestamp <= timestamp:
            return False

        if duration is None:
            return True
        
        over1, over2 = self.overlap_percentages( timestamp, duration )

        # TODO Allow cutting emitted events
        # return over1 > self.transformer.autofix_overlaps_percentage \
        #    and over2 > self.transformer.autofix_overlaps_percentage
        return over2 > self.transformer.autofix_overlaps_percentage

    def is_connected_at ( self, timestamp : int ) -> bool:
        # TODO Implement overlap control here too
        return abs( timestamp - self.last_end_timestamp ) <= 3

    def distance ( self, event : NoteEvent ) -> float:
        return abs( int( event ) - int( self.average_pitch ) )

    def create_rest ( self, target : int, visible : bool = True ) -> RestEvent:
        duration = target - self.last_end_timestamp

        value = self.voice.from_duration_absolute( duration )

        return RestEvent(
            timestamp = self.last_end_timestamp,
            visible = visible,
            duration = duration,
            value = value,
            voice = self.voice,
            staff = self.parent_staff
        )

    def append ( self, *events : MusicEvent ):
        for event in events:
            if isinstance( event, NoteEvent ) or isinstance( event, ChordEvent ):
                self.average_pitch += int( event ) if isinstance( event, NoteEvent ) \
                                else  sum( event.pitches ) / len( event.pitches )

                # TODO Allow setting a minimum rest duration. If the empty space between the events is less than
                # said minimum, then no rest is created
                if self.auto_create_rests and self.last_end_timestamp < event.timestamp - 1:
                    self.transformer.add_output( self.create_rest( event.timestamp ) )

            if self.last_end_timestamp > event.timestamp:
                # o1, o2 = self.overlap_percentages( event.timestamp, event.duration )
                event = event.clone(
                    timestamp = self.last_end_timestamp,
                    end_timestamp = event.end_timestamp
                )

            self.transformer.add_output( event.clone( voice = self.voice ) )

            self.last_event = event

class VoiceIdentifierTransformer(Transformer):
    """
    This class receives a flat, ordered stream of musical events and splits them in multiple voices and identifies parallel notes/chords
    """
    def __init__ ( self, auto_create_rests : bool = True, auto_create_end_rests : bool = True ):
        super().__init__()

        self.voices : List[VoiceIdentifierVoice] = []

        self.auto_create_rests : bool = auto_create_rests
        
        self.auto_create_end_rests : bool = auto_create_end_rests

        # Value between 0 and 1
        self.autofix_overlaps_percentage : float = 0.1
    
    def create_voice_for ( self, event : DurationEvent ) -> VoiceIdentifierVoice:
        index = max( ( voice.index for voice in self.voices if voice.parent_name == event.voice.name ), default = 0 )

        voice = VoiceIdentifierVoice( self, event.voice, index + 1, event.staff )

        voice.auto_create_rests = self.auto_create_rests
        voice.auto_create_end_rests = self.auto_create_end_rests

        self.voices.append( voice )

        return voice

    def find_voice_for ( self, event : DurationEvent, auto_create : bool = True ) -> Optional[VoiceIdentifierVoice]:
        best_voice, best_voice_dst = None, None

        for voice in self.voices:
            if voice.parent_name != event.voice.name or voice.parent_staff != event.staff:
                continue

            # If the voice already has a sound playing at this timestamp
            if voice.is_busy_at( event.timestamp, event.duration ):
                continue

            if event.staff is not None:
                return voice

            voice_dst = voice.distance( event )

            if best_voice is None or best_voice_dst > voice_dst:
                best_voice = voice
                best_voice_dst = voice_dst

        if best_voice is None and auto_create:
            best_voice = self.create_voice_for( event )

        return best_voice
    
    def find_voice_for_rest ( self, event, auto_create : bool = True ) -> VoiceIdentifierVoice:
        for voice in self.voices:
            if voice.parent_name != event.voice.name or voice.parent_staff != event.staff:
                continue

            # If the voice already has a sound playing at this timestamp
            if voice.is_connected_at( event.timestamp ):
                return voice

        return self.create_voice_for( event )

    def register_rest ( self, event : RestEvent ):
        voice = self.find_voice_for_rest( event )

        if voice is not None:
            voice.append( event )

    def register_note ( self, event : NoteEvent ):
        voice = self.find_voice_for( event )

        if voice is not None:
            voice.append( event )
    
    def register_chord ( self, event : ChordEvent ):
        voice = self.find_voice_for( event )

        if voice is not None:
            voice.append( event )

    def transform ( self ):
        """
        For now, NoteOn/NoteOff events will be ignored. 
        Use the compose transformer before passing events into this notation builder. 
        This might change in the future.
        """
        while True:
            done, event = yield

            if done: break

            if isinstance( event, NoteEvent ):
                self.register_note( event )
            elif isinstance( event, RestEvent ):
                self.register_rest( event )
            elif isinstance( event, ChordEvent ):
                self.register_chord( event )
            else:
                self.add_output( event )

        if self.auto_create_end_rests and self.voices:
            last_voice_timestamp : int = max( [ voice.last_end_timestamp for voice in self.voices ] )

            for voice in self.voices:
                if voice.last_end_timestamp < last_voice_timestamp:
                    self.add_output( voice.create_rest( last_voice_timestamp, visible = False ) )
