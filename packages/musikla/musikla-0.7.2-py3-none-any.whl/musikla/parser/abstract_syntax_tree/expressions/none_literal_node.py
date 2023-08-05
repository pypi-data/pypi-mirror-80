from musikla.parser.printer import CodePrinter
from typing import Tuple
from .expression_node import ExpressionNode
from musikla.core import Value

class NoneLiteralNode( ExpressionNode ):
    def __init__ ( self, position : Tuple[int, int, int] = None ):
        super().__init__( position )

        self.value = None

    def __eval__ ( self, context, assignment : bool = False ):
        return self.value
    
    def to_source ( self, printer : CodePrinter ):
        printer.add_token( "none" )
