from musikla.parser.printer import CodePrinter
from typing import Tuple
from .expression_node import ExpressionNode
from ..node import Node
from ..stack_frame_node import StackFrameNode
from musikla.core import Context

class BlockNode( ExpressionNode ):
    def __init__ ( self, body : Node = None, position : Tuple[int, int, int] = None ):
        super().__init__( position )

        self.body = StackFrameNode( body, position = position )
        self.fork_context : bool = True
        self.create_stack_frame : bool = True

    def __eval__ ( self, context : Context ):
        forked = context.fork( symbols = context.symbols.fork( opaque = False ) ) if self.fork_context else context

        try:
            if self.create_stack_frame:
                return self.body.eval( forked )
            else:
                return self.body.child.eval( forked )
        finally:
            context.join( forked )

    def to_source ( self, printer : CodePrinter ):
        with printer.block():
            self.body.to_source( printer )
