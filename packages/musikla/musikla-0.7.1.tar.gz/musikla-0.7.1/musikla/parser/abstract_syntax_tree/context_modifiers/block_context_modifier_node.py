from typing import Tuple
from .. import MusicNode
from musikla.core import Music

class BlockContextModifierNode( MusicNode ):
    def __init__ ( self, body, position : Tuple[int, int, int] = None ):
        super().__init__( position )

        self.body = body
    
    def modify ( self, context ):
        pass

    def restore ( self, context ):
        pass

    def get_events ( self, context ):
        block_context = context.fork()

        events = self.modify( block_context )

        if isinstance( events, Music ):
            for event in events.expand( context ): yield event

        try:
            if self.body != None:
                events = self.body.eval( block_context )

                if isinstance( events, Music ):
                    for event in events.expand( block_context ): yield event

            events = self.restore( block_context )

            if isinstance( events, Music ):
                for event in events.expand( context ): yield event
        finally:
            context.join( block_context )
