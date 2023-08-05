from chunk import Chunk
from typing import Any, Generator, cast, IO
from itertools import islice
import struct
import io

class SoundFont:
    @staticmethod
    def from_file ( file : str ) -> 'SoundFont':
        return SoundFont( cast( IO[bytes], open( file, 'rb' ) ) )

    @staticmethod
    def from_io ( stream : IO[bytes] ) -> 'SoundFont':
        return SoundFont( stream )

    def __init__ ( self, stream : IO[bytes] ):
        self.stream : IO[bytes] = stream

        for ch in islice( self.read_chunks(), 10 ):
            name = ch.chunkname.decode( 'utf-8', errors = 'replace' )

            print( name, ch.chunksize )

            if ( hasattr( self, 'parse_' + name ) ):
                getattr( self, 'parse_' + name )( ch )
    
    def parse_RIFF ( self, chunk : Chunk ):
        print( chunk.read( 4 ).decode( 'utf-8', errors = 'replace' ) )
        pass
    
    def parse_LIST ( self, chunk : Chunk ):
        print( chunk.read( 4 ).decode( 'utf-8', errors = 'replace' ) )
        pass

    def parse_ifil ( self, chunk : Chunk ):
        chunk.seek( chunk.tell() + 4 )
        print( chunk.read( 4 ).decode( 'utf-8', errors = 'replace' ) )
        pass

    def read_chunks ( self ) -> Generator[Chunk, Any, Any]:
        try:
            while True:
                print( self.stream.tell() )

                ch : Chunk = Chunk( self.stream, True )

                yield ch
        except EOFError:
            pass

sf2 = SoundFont.from_file( 'C:\\Users\\PedroSilva\\Downloads\\freepiano_2.2.2.1_win64\\freepiano\\sf2\\FluidR3_GM.sf2' )
