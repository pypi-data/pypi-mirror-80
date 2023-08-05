from musikla.core import Context
from musikla.core.events import MusicEvent
from musikla.core.events.transformers import Transformer
from typing import Any, Iterable, Optional
from configparser import ConfigParser
import argparse

class ArgumentParserError(Exception): pass

class ArgumentParser( argparse.ArgumentParser ):
    def error( self, message ):
        raise ArgumentParserError( message )

class Sequencer:
    def __init__ ( self ):
        self.realtime = False

        self.transformer : Optional[Transformer] = None

    def set_transformers ( self, *transformers : Transformer ):
        if transformers:
            self.transformer = Transformer.pipeline( 
                *transformers,
                Transformer.subscriber( self.on_event, self.on_close )
            )
        else:
            self.transformer = None

    @property
    def playing ( self ) -> bool:
        raise BaseException( "Abstract property Sequencer.playing accessed." )

    def get_time ( self ) -> int:
        raise BaseException( "Abstract method Sequencer.get_time called." )

    def on_event ( self, event : MusicEvent ):
        raise BaseException( "Abstract method Sequencer.on_event called." )
    
    def on_close ( self ):
        raise BaseException( "Abstract method Sequencer.on_close called." )

    def register_event ( self, event : MusicEvent ):
        if self.transformer is None:
            self.on_event( event )
        else:
            self.transformer.add_input( event )

    def register_events_many ( self, events : Iterable[MusicEvent] ):
        for event in events:
            self.register_event( event )

    def join ( self ):
        raise BaseException( "Abstract method Sequencer.join called." )

    def start ( self ):
        raise BaseException( "Abstract method Sequencer.start called." )

    def close ( self ):
        if self.transformer is None:
            self.on_close()
        else:
            self.transformer.end_input()

class SequencerFactory:
    default : bool = False

    def __init__ ( self, context : Context, config : ConfigParser ):
        self.name : str = ""
        self.argparser : Optional[ArgumentParser] = None
        self.context : Context = context
        self.config : ConfigParser = config

        self.init()
    
    def init ( self ):
        pass

    def from_str ( self, uri : str, args : Any = None ) -> Optional[Sequencer]:
        return None
