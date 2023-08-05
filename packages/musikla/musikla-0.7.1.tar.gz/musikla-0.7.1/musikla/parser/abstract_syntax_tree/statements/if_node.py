from musikla.parser.printer import CodePrinter
from typing import Optional, Tuple
from musikla.core import Context
from ..node import Node
from .statement_node import StatementNode

class IfStatementNode( StatementNode ):
    def __init__ ( self, condition : Node, body : Node, else_body : Node = None, position : Tuple[int, int, int] = None ):
        from ..expressions.block_node import BlockNode

        super().__init__( position )

        self.condition : Node = condition
        self.body : Node = body
        self.else_body : Optional[Node] = else_body

        if isinstance( self.body, BlockNode ):
            self.body.fork_context = False
            self.body.create_stack_frame = False

        if isinstance( self.else_body, BlockNode ):
            self.else_body.fork_context = False
            self.else_body.create_stack_frame = False

    def __eval__ ( self, context : Context ):
        condition_value = self.condition.eval( context )

        result = None

        if condition_value:
            result = self.body.eval( context )
        elif self.else_body != None:
            result = self.else_body.eval( context )

        return result

    def to_source ( self, printer : CodePrinter ):
        from ..expressions.group_node import GroupNode
        from ..expressions.block_node import BlockNode

        printer.add_token( 'if ' )

        self.condition.to_source( printer )

        if not isinstance( self.condition, GroupNode ) and not isinstance( self.body, BlockNode ):
            printer.add_token( " then " )
        else:
            printer.add_token( " " )

        self.body.to_source( printer )

        if self.else_body is not None:
            printer.add_token( " else " )

            self.else_body.to_source( printer )
