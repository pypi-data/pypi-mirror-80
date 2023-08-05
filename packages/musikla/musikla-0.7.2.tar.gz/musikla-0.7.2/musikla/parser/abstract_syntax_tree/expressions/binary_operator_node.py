from musikla.core.value import CallableValue
from musikla.parser.printer import CodePrinter
from ..node import Node
from .expression_node import ExpressionNode
from musikla.core import Value, Music
from typing import Optional, Tuple, Union

class BinaryOperatorNode( ExpressionNode ):
    def __init__ ( self, left : Node, right : Node, position : Tuple[int, int, int] = None ):
        super().__init__( position )

        self.left : Node = left
        self.right : Node = right

    def __eval__ ( self, context ):
        return None

class PlusBinaryOperatorNode(BinaryOperatorNode):
    def __eval__ ( self, context ):
        left_value = self.left.eval( context )
        right_value = self.right.eval( context )

        return left_value + right_value

    def to_source ( self, printer : CodePrinter ):
        self.left.to_source( printer )

        printer.add_token( ' + ' )

        self.right.to_source( printer )

class MinusBinaryOperatorNode(BinaryOperatorNode):
    def __eval__ ( self, context ):
        left_value = self.left.eval( context )
        right_value = self.right.eval( context )

        return left_value - right_value
    
    def to_source ( self, printer : CodePrinter ):
        self.left.to_source( printer )

        printer.add_token( ' - ' )

        self.right.to_source( printer )

class PowBinaryOperatorNode(BinaryOperatorNode):
    def __eval__ ( self, context ):
        left_value = self.left.eval( context.fork(cursor = 0) )
        right_value = self.right.eval( context.fork(cursor = 0) )

        return left_value ** right_value
    
    def to_source ( self, printer : CodePrinter ):
        self.left.to_source( printer )

        printer.add_token( ' ** ' )

        self.right.to_source( printer )

class MultBinaryOperatorNode(BinaryOperatorNode):
    def __eval__ ( self, context ):
        left_value = self.left.eval( context.fork( cursor = 0 ) )
        right_value = self.right.eval( context.fork( cursor = 0 ) )

        return left_value * right_value
    
    def to_source ( self, printer : CodePrinter ):
        self.left.to_source( printer )

        printer.add_token( ' * ' )

        self.right.to_source( printer )

class DivBinaryOperatorNode(BinaryOperatorNode):
    def __eval__ ( self, context ):
        left_value = self.left.eval( context )
        right_value = self.right.eval( context )

        return left_value / right_value
    
    def to_source ( self, printer : CodePrinter ):
        self.left.to_source( printer )

        printer.add_token( ' / ' )

        self.right.to_source( printer )

class AndLogicOperatorNode(BinaryOperatorNode):
    def __eval__ ( self, context ):
        left_value = self.left.eval( context )

        if not left_value: return False

        right_value = self.right.eval( context )

        return bool( right_value )

    def to_source ( self, printer : CodePrinter ):
        self.left.to_source( printer )

        printer.add_token( ' and ' )

        self.right.to_source( printer )

class OrLogicOperatorNode(BinaryOperatorNode):
    def __eval__ ( self, context ):
        left_value = self.left.eval( context )

        if left_value:
            return left_value

        right_value = self.right.eval( context )

        return right_value if right_value else False

    def to_source ( self, printer : CodePrinter ):
        self.left.to_source( printer )

        printer.add_token( ' or ' )

        self.right.to_source( printer )

class ComparisonOperatorNode(BinaryOperatorNode):
    operator : Optional[str] = None

    def __init__ ( self, left : Node, right : Node, position : Tuple[int, int, int] = None ):
        super().__init__( left, right, position )

    def compare ( self, a, b ):
        pass

    def __eval__ ( self, context, assignment : bool = False ):
        left_value = self.left.eval( context )
        right_value = self.right.eval( context )

        return self.compare( left_value, right_value )

    def to_source ( self, printer : CodePrinter ):
        self.left.to_source( printer )

        printer.add_token( ' ' + self.operator + ' ' )

        self.right.to_source( printer )

class GreaterEqualComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = '>='

    def compare ( self, a, b ): return a >= b

class GreaterComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = '>'

    def compare ( self, a, b ): return a > b

class EqualComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = '=='

    def compare ( self, a, b ): return a == b

class NotEqualComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = '!='

    def compare ( self, a, b ): return a != b

class LesserEqualComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = '<='

    def compare ( self, a, b ): return a <= b

class LesserComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = '<'

    def compare ( self, a, b ): 
        return a < b

class IsComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = 'in'

    def compare ( self, a, b ): 
        if isinstance( a, CallableValue ): a = a.raw()
        
        if isinstance( b, CallableValue ): b = b.raw()

        return a is b or type(a) is b

class IsNotComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = 'notin'

    def compare ( self, a, b ): 
        if isinstance( a, CallableValue ): a = a.raw()
        
        if isinstance( b, CallableValue ): b = b.raw()

        return ( a is not b ) and ( type(a) is not b )

class InComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = 'in'

    def compare ( self, a, b ): 
        return a in b

class NotInComparisonOperatorNode(ComparisonOperatorNode):
    operator : str = 'notin'

    def compare ( self, a, b ): 
        return a not in b
