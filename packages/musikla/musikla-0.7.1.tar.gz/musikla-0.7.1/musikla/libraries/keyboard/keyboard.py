from decimal import InvalidOperation
from musikla.core import Context, Value, Music
from musikla.core.theory import Note
from musikla.core.events import NoteEvent
from typing import Callable, List, Dict, Optional, Union, Any, cast
from musikla.parser.abstract_syntax_tree import Node, MusicSequenceNode
from musikla.parser.abstract_syntax_tree.expressions import FunctionExpressionNode, ConstantNode
from musikla.audio import Player, InteractivePlayer
from .event import KeyStroke, PianoKey, KeyboardEvent
from .action import KeyAction

class SubscriberEvent:
    def __init__ ( self ):
        self.listeners : List[Callable] = []

    def add_listener ( self, fn : Callable ):
        self.listeners.append( fn )

    def __iadd__ ( self, fn ):
        if callable( fn ):
            return self.add_listener( fn )
        
        return NotImplemented    

    def remove_listener ( self, fn : Callable ):
        if fn in self.listeners:
            self.listeners.remove( fn )
    
    def __isub__ ( self, fn ):
        if callable( fn ):
            return self.remove_listener( fn )
        
        return NotImplemented    

    def trigger ( self, *args ):
        for obs in self.listeners:
            obs( *args )

    def __call__ ( self, *args ):
        self.trigger( *args )

class KeyActionSubscriber:
    def __init__ ( self, 
            on_press : Callable = None,
            on_release : Callable = None,
            on_start : Callable = None,
            on_stop : Callable = None
        ):
        self.on_press : Optional[Callable] = on_press
        self.on_release : Optional[Callable] = on_release
        self.on_start : Optional[Callable] = on_start
        self.on_stop : Optional[Callable] = on_stop
    
class Keyboard:
    @staticmethod
    def as_event ( key_value : Any ) -> KeyboardEvent:
        if type( key_value ) == str:
            return KeyStroke.parse( key_value )
        elif isinstance( key_value, Music ) or isinstance( key_value, NoteEvent )  or isinstance( key_value, Note ):
            return PianoKey( key_value )
        elif isinstance( key_value, KeyboardEvent ):
            return key_value
        else:
            raise Exception( "Keyboard value is invalid" )

    def __init__ ( self, context : Context ):
        self.context : Context = context        
        self._player : Optional[Player] = None

        self.keys : Dict[KeyboardEvent, KeyAction] = dict()
        self.global_flags : Dict[str, int] = dict()
        self.global_prefixes : List[Node] = list()

        self._on_new_player_observers : List[Callable] = []

        self.manual_lifetime : bool = False

    def on_new_player ( self, player : InteractivePlayer ):
        for obs in self._on_new_player_observers:
            obs( self, player )

    def add_new_player_observer ( self, observer : Callable ):
        self._on_new_player_observers.append( observer )
    
    def remove_new_player_observer ( self, observer : Callable ):
        if observer in self._on_new_player_observers:
            self._on_new_player_observers.remove( observer )

    @property
    def player ( self ) -> Player:
        if self._player is None:
            from .library import KeyboardLibrary

            lib : KeyboardLibrary = cast( KeyboardLibrary, self.context.library( KeyboardLibrary ) )

            self._player = lib.player

        return self._player

    def get_keyboard_flag ( self, context : Context, node : Optional[Node], name : str ) -> bool:
        if node != None:
            value : Value = node.eval( context )

            return bool( value )

        return name in self.global_flags and self.global_flags[ name ] > 0

    def register_key ( self, context : Context, key : Node, expression : Node, args : List[str] = [], toggle : Node = None, hold : Node = None, repeat : Node = None, extend : Node = None, release : Node = None ):
        toggle_value = self.get_keyboard_flag( context, toggle, "toggle" )
        hold_value = self.get_keyboard_flag( context, hold, "hold" )
        repeat_value = self.get_keyboard_flag( context, repeat, "repeat" )
        extend_value = self.get_keyboard_flag( context, extend, "extend" )
        release_value = self.get_keyboard_flag( context, release, "release" )
        
        key_value = key.eval( context )

        if self.global_prefixes:
            expression = MusicSequenceNode( [ *self.global_prefixes, expression ] )

        key_event = Keyboard.as_event( key_value )

        action = KeyAction(
            key = key_event,
            expr = expression,
            args = args,
            context = context,
            toggle = toggle_value,
            hold = hold_value,
            repeat = repeat_value,
            extend = extend_value,
            release = release_value
        )

        self.keys[ action.key ] = action

    def push_flags ( self, context : Context, *flags : Node ):
        for flag in flags:
            value : str = flag.eval( context )

            if Value.typeof( value ) == str:
                if value in self.global_flags:
                    self.global_flags[ value ] += 1
                else:
                    self.global_flags[ value ] = 1

    def pop_flags ( self, context : Context, *flags : Node ):
        for flag in flags:
            value : str = flag.eval( context )

            if Value.typeof( value ) == str:
                if value in self.global_flags:
                    self.global_flags[ value ] -= 1

                    if self.global_flags[ value ] == 0:
                        del self.global_flags[ value ]

    def push_prefix ( self, context : Context, expression : Node ):
        self.global_prefixes.append( expression )

    def pop_prefix ( self, context : Context ):
        self.global_prefixes.pop()

    def start_all ( self ):
        for key in self.keys.values():
            key.play( self.context, self.player, {} )

    def stop_all ( self ):
        for key in self.keys.values():
            key.stop( self.context, self.player )

    def start ( self, key : Union[ KeyboardEvent, str ] ):
        key_stroke : KeyboardEvent = cast( KeyboardEvent, KeyStroke.parse( key ) if Value.typeof( key ) == str else key )

        if key_stroke in self.keys:
            self.keys[ key_stroke ].play( self.context, self.player, key_stroke.get_parameters(), self.on_new_player )

    def stop ( self, key : Union[ KeyboardEvent, str ] ):
        key_stroke : KeyboardEvent = cast( KeyboardEvent, KeyStroke.parse( key ) if Value.typeof( key ) == str else key )

        if key_stroke in self.keys:
            self.keys[ key_stroke ].stop( self.context, self.player )

    def __getitem__ ( self, key ):
        key_stroke : KeyboardEvent = cast( KeyboardEvent, KeyStroke.parse( key ) if Value.typeof( key ) == str else key )

        return self.keys[ key_stroke ]

    def __contains__ ( self, key : Union[ KeyboardEvent, str ] ) -> bool:
        key_stroke : KeyboardEvent = cast( KeyboardEvent, KeyStroke.parse( key ) if Value.typeof( key ) == str else key )

        return key_stroke in self.keys

    def on_press ( self, key : Union[ KeyboardEvent, str ] ):
        key_stroke : KeyboardEvent = cast( KeyboardEvent, KeyStroke.parse( key ) if Value.typeof( key ) == str else key )

        if key_stroke in self.keys:
            self.keys[ key_stroke ].on_press( self.context, self.player, key_stroke.get_parameters(), self.on_new_player )

    def on_release ( self, key : Union[str, KeyboardEvent] ):
        key_stroke : KeyboardEvent = cast( KeyboardEvent, KeyStroke.parse( key ) if Value.typeof( key ) == str else key )

        if key_stroke in self.keys:
            self.keys[ key_stroke ].on_release( self.context, self.player, self.on_new_player )

    @property
    def is_closed ( self ) -> bool:
        from .library import KeyboardLibrary

        lib : KeyboardLibrary = cast( KeyboardLibrary, self.context.library( KeyboardLibrary ) )
        
        return self not in lib.keyboards

    def close ( self, closing : bool = False ) -> 'Keyboard':
        from .library import KeyboardLibrary

        self.stop_all()

        if not closing:
            keyboard : KeyboardLibrary = cast( KeyboardLibrary, self.context.library( KeyboardLibrary ) )

            keyboard.close( self )
        
        return self

    def open ( self ) -> 'Keyboard':
        from .library import KeyboardLibrary

        lib : KeyboardLibrary = cast( KeyboardLibrary, self.context.library( KeyboardLibrary ) )
        
        if self not in lib.keyboards:
            lib.keyboards.append( self )

        return self

    def _assert_keyboard ( self, obj ):
        if obj is None:
            raise InvalidOperation( "Cannot combine a keyboard with 'None'" )
            
        if not isinstance( obj, Keyboard ):
            raise InvalidOperation( f"Cannot combine a keyboard with '{ type( obj ) }'" )

    def clone ( self, auto_close : bool = True ):
        from .library import KeyboardLibrary

        lib : KeyboardLibrary = cast( KeyboardLibrary, self.context.library( KeyboardLibrary ) )

        keyboard = lib.create()
        
        if auto_close and not self.manual_lifetime:
            self.close()

        keyboard.context = self.context
        keyboard.keys = dict( self.keys )
        keyboard.global_flags = dict( self.global_flags )
        keyboard.global_prefixes = list( self.global_prefixes )
        keyboard.manual_lifetime = self.manual_lifetime
        
        return keyboard

    def map_actions ( self, context : Context, mapper : Node ) -> 'Keyboard':
        mapper = Value.eval( context, mapper ).raw() if isinstance( mapper, Node ) else mapper

        keyboard = self.clone()

        for key, action in self.keys.items():
            keyboard.keys[ key ] = mapper( context, ConstantNode( action ) )

        return keyboard

    def map ( self, context : Context, mapper : Node ) -> 'Keyboard':
        mapper = Value.eval( context, mapper ) if isinstance( mapper, Node ) else mapper

        keyboard = self.clone()

        for key, action in self.keys.items():
            keyboard.keys[ key ] = action.clone(
                expr = FunctionExpressionNode( ConstantNode( mapper ), [ ConstantNode( action.key ), action.expr ] )
            )

        return keyboard

    def with_grid ( self, context : Context, grid, mode : str = 'start_end' ) -> 'Keyboard':
        def _mapper ( context : Context, k, music ):
            return grid.align( context, music, mode )

        return self.map( context, _mapper )

    def __add__ ( self, other ):
        from .library import KeyboardLibrary

        self._assert_keyboard( other )

        keyboard : KeyboardLibrary = cast( KeyboardLibrary, self.context.library( KeyboardLibrary ) )

        kb = keyboard.create()

        kb += self
        kb += other

        return kb

    def __sub__ ( self, other ):
        from .library import KeyboardLibrary

        self._assert_keyboard( other )

        keyboard : KeyboardLibrary = cast( KeyboardLibrary, self.context.library( KeyboardLibrary ) )

        kb = keyboard.create()

        kb += self
        kb -= other

        return kb

    def __iadd__ ( self, other ):
        self._assert_keyboard( other )

        if not other.manual_lifetime:
            other.close()

        self.keys.update( other.keys )

        return self
    
    def __isub__ ( self, other ):
        self._assert_keyboard( other )

        for key in other.keys:
            self.keys.pop( key, None )

        return self

# class ActionMapNode(Node):
#     def __init__ ( self, mapper, key : KeyboardEvent, original : Node ):
#         self.mapper = mapper
#         self.key : KeyboardEvent = key
#         self.original : Node = original
    
#     def eval ( self, context : Context ):
#         result = Value.eval( context, self.original )

        

#         return self.mapper( self.key, result )
