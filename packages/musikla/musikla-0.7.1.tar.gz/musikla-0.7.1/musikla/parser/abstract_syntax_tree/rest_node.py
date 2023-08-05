from musikla.parser.printer import CodePrinter
from typing import Tuple
from .music_node import MusicNode
from musikla.core.events import RestEvent

class RestNode( MusicNode ):
    def __init__ ( self, value = None, visible = False, position : Tuple[int, int, int] = None ):
        super().__init__( position )
        
        self.value = value
        self.visible = visible

    def to_source ( self, printer : CodePrinter ):
        printer.add_token( RestEvent( 0, 0, self.value, visible = self.visible ).to_string( ( 'r', 'r' ) ) )

    def get_events ( self, context ):
        rest = RestEvent(
            timestamp = context.cursor,
            duration = context.get_duration( self.value ),
            value = context.get_value( self.value ),
            voice = context.voice,
            visible = self.visible,
            staff = 0
        )

        context.cursor += rest.duration

        yield rest
