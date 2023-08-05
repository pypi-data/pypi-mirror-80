from typing import Tuple
from musikla.parser.printer import CodePrinter
from musikla.core import Context
from ..node import Node
from ..music_node import MusicSequenceBase

class WhileLoopStatementNode( MusicSequenceBase ):
    def __init__ ( self, condition : Node, body : Node, position : Tuple[int, int, int] = None ):
        from ..expressions.block_node import BlockNode

        super().__init__( position )

        self.condition : Node = condition
        self.body : Node = body

        if isinstance( self.body, BlockNode ):
            self.body.fork_context = False
            self.body.create_stack_frame = False

    def values ( self, context : Context ):
        condition_value = self.condition.eval( context )

        while condition_value:
            forked = context.fork( symbols = context.symbols.fork( opaque = False ) )

            yield self.body.eval( forked )

            context.join( forked )

            condition_value = self.condition.eval( context )

    def to_source ( self, printer : CodePrinter ):
        from ..expressions.group_node import GroupNode
        from ..expressions.block_node import BlockNode

        printer.add_token( 'while ' )

        self.condition.to_source( printer )

        if not isinstance( self.condition, GroupNode ) and not isinstance( self.body, BlockNode ):
            printer.add_token( " then " )
        else:
            printer.add_token( " " )

        self.body.to_source( printer )
