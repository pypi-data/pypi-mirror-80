from .voice import Voice
from .shared_context import SharedContext
from .symbols_scope import SymbolsScope
from typing import Any, Hashable, Optional, cast, TYPE_CHECKING
from fractions import Fraction


if TYPE_CHECKING:
    from musikla.script import Script

class Library:
    def __init__ ( self, namespace : str = None ):
        self.namespace : Optional[str] = namespace
        self.context : Context = cast( Any, None )

    def on_link ( self, script ):
        pass

    def resolve ( self, name : str ) -> str:
        if self.namespace != None and self.namespace != '':
            if self.namespace.endswith( '\\' ) and name.startswith( '\\' ):
                return self.namespace + name[ 1: ]
            elif self.namespace.endswith( '\\' ) or name.startswith( '\\' ):
                return self.namespace + name
            else:
                return self.namespace + '\\' + name
        else:
            return name

    def lookup ( self, name : Hashable, container : str = "", recursive : bool = True, follow_pointers : bool = True, default = None ):
        return self.context.symbols.lookup( self.resolve( name ), container = container, recursive = recursive, follow_pointers = follow_pointers, default = default )

    def assign ( self, name : Hashable, value, container = "", follow_pointers : bool = True ):
        return self.context.symbols.assign( self.resolve( name ), value, container, follow_pointers )

    def lookup_instrument ( self, name ):
        return self.context.symbols.lookup_instrument( self.resolve( name ) )

    def assign_instrument ( self, instrument ):
        self.assign( instrument.name, instrument, container = "instruments" )
        
        return instrument

    def lookup_internal ( self, name ):
        return self.context.symbols.lookup_internal( self.resolve( name ) )

    def assign_internal ( self, name, value ):
        self.context.symbols.assign_internal( self.resolve( name ), value )
    
    def eval_file ( self, script, file ):
        script.execute_file( file, context = self.context, fork = False, silent = True )
    
    def eval ( self, script, code ):
        script.execute( code, context = self.context, fork = False, silent = True )

class Context():
    default : 'Context' = None

    @staticmethod
    def create ():
        ctx = Context(
            # voice = Voice( "default", instrument = Instrument( 'Acoustic Grand Piano', GeneralMidi.AcousticGrandPiano ) )
        )

        ctx.symbols.assign( 'is_prelude', True, container = 'internal' )
        ctx.symbols.assign( ctx.voice.name, ctx.voice )

        return ctx

    def __init__ ( self, 
                   shared : SharedContext = None, 
                   voice : Voice = None,
                   cursor : int = 0,
                   symbols : SymbolsScope = None,
                 ):
        self.shared : SharedContext = shared or SharedContext()
        self.voice : Optional[Voice] = voice or Voice()
        self.cursor : int = cursor
        self.symbols : SymbolsScope = symbols or SymbolsScope()

    @property
    def script ( self ) -> 'Script':
        return self.symbols.lookup( 'script', container = 'internal' )

    def fork ( self, cursor : int = None, symbols : SymbolsScope = None ) -> 'Context':
        return Context(
            shared = self.shared,
            voice = self.voice,
            cursor = self.cursor if cursor == None else cursor,
            symbols = self.symbols if symbols == None else symbols
        )

    def join ( self, *child_context ):
        for context in child_context:
            if type(context) == int:
                if context > self.cursor:
                    self.cursor = context
            else:
                if context.cursor > self.cursor:
                    self.cursor = context.cursor
    
    def get_value ( self, value : float ) -> float:
        return self.voice.get_value( value )

    def get_duration_ratio ( self ) -> float:
        return self.voice.get_duration_ratio()

    def get_duration ( self, value : float = None ) -> int:
        """Transform a not value into the real world milliseconds it takes, according to the voice's tempo and time signature"""
        return self.voice.get_duration( value )

    def from_duration ( self, milliseconds : int ) -> Fraction:
        """Transform a duration in milliseconds to an approximated note value relative to the tempo and time signature"""
        return self.voice.from_duration( milliseconds )

    def is_linked ( self, library : Library ) -> bool:
        return self.symbols.lookup( library.__class__, container = 'libraries' ) != None

    def link ( self, library : Library, script = None ):
        if not self.is_linked( library ):
            library.context = self

            self.symbols.assign( library.__class__, library, container = "libraries" )

            library.on_link( script )

    def library ( self, library ) -> Library:
        return self.symbols.lookup( library, container = "libraries" )

Context.default = Context.create()

class StackFrame:
    def __init__ ( self ):
        self.returned : bool = False
        self.returned_value : Any = None

    def ret ( self, value : Any = None ):
        self.returned = True
        self.returned_value = value