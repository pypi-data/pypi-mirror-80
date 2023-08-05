from musikla.parser.printer import CodePrinter
from typing import Tuple
from .context_modifier_node import ContextModifierNode
from musikla.core.events import ContextChangeEvent
from musikla.core import Context, Voice

class VelocityModifierNode( ContextModifierNode ):
    def __init__ ( self, velocity, position : Tuple[int, int, int] = None ):
        super().__init__( position )

        self.velocity = velocity

    def apply ( self, voice : Voice ):
        voice.velocity = self.velocity

    def modify ( self, context : Context ):
        context.voice = context.voice.clone( velocity = self.velocity )

        yield ContextChangeEvent( context.cursor, "velocity", context.voice.velocity, context.voice, 0 )
    
    def to_source ( self, printer : CodePrinter ):
        printer.add_token( 'V' + str( self.velocity ) )
