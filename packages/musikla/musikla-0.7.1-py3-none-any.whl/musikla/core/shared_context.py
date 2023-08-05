from typing import Dict

class SharedContext():
    def __init__ ( self ):
        self.channel_count = 24
        self.channels = dict()
        self.release_channels = True

    @property
    def available_channels ( self ):
        return filter( lambda i: i not in self.channels, range( 1, self.channel_count ) )

    def register_instrument ( self, instrument ):
        channel = next( self.available_channels, None )

        if channel == None:
            raise BaseException( "No channel available found" )

        self.channels[ channel ] = instrument

        instrument.channel = channel

    def unregister_instrument ( self, instrument ):
        if self.release_channels:
            del self.channels[ instrument.channel ]

            instrument.channel = None
