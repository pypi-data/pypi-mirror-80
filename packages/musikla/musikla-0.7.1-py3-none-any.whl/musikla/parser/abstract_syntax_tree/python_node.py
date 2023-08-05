from musikla.parser.printer import CodePrinter
from typing import Tuple, Union, Any
from .node import Node
from musikla.core import Context
import inspect

class PythonNode( Node ):
    
    @staticmethod
    def get_auto_name ( val ):
        return val.__name__

    @staticmethod
    def create_export_decorator ( context : Context ):
        def export ( name : Union[str, any] = None ):
            nonlocal context

            def export_instance ( val ):
                nonlocal name, context

                if name is None:
                    name = PythonNode.get_auto_name( val )
                
                context.symbols.assign( name, val )

                return val
            
            if name is not None and type(name) is not str:
                val, name = name, None

                return export_instance( val )
            else:
                return export_instance

        return export

    def execute ( context : Context, code : Union[str, Any], is_expression : bool = False ):
        if type( code ) is str:
            code = compile( code, "<embedded python>", 'eval' if is_expression else 'exec' )

        custom_globals = {}

        if is_expression:
            custom_locals = PythonContext( context )
        else:
            custom_globals[ 'export' ] = PythonNode.create_export_decorator( context )
            custom_locals = {}

        return eval( code, custom_globals, custom_locals )

    def __init__ ( self, code : str, is_expression : bool = False, position : Tuple[int, int, int] = None ):
        super().__init__( position )

        self.code : str = code
        self.is_expression : bool = is_expression
        self.bytecode = compile( self.code, "<embedded python>", 'eval' if is_expression else 'exec' )
        self.hoisted : bool = not is_expression
    
    def to_source ( self, printer : CodePrinter ):
        if self.is_expression:
            printer.add_token( '@py' )
            with printer.block():
                printer.add_token( self.code )
        else:
            printer.add_token( '@python ' )
            printer.add_token( self.code )

    def __eval__ ( self, context : Context ):
        return PythonNode.execute( context, self.bytecode, self.is_expression )

class PythonContext:
    def __init__ ( self, context : Context ):
        self.context : Context = context
    
    def __getitem__ ( self, key ):
        return self.context.symbols.lookup( key, stop_on = self.context.symbols.prelude, default = KeyError(), raise_default = True )
    
    def __setitem__ ( self, key, value ):
        return self.context.symbols.assign( key, value )
    
    def __contains__ ( self, key ):
        try:
            self[ key ]

            return True
        except KeyError:
            return False

    def get(self, k):
        return self.__getitem__( k )

    def items( self ):
        return iter( () )
    def keys( self ):
        return iter( () )
    def values( self ):
        return iter( () )
    def __len__( self ):
        return 0

    # @overload
    # def get(self, k: _KT, default: Union[_VT_co, _T]) -> Union[_VT_co, _T]: ...
    # def items(self) -> AbstractSet[Tuple[_KT, _VT_co]]: ...
    # def keys(self) -> AbstractSet[_KT]: ...
    # def values(self) -> ValuesView[_VT_co]: ...
    # def __contains__(self, o: object) -> bool: ...