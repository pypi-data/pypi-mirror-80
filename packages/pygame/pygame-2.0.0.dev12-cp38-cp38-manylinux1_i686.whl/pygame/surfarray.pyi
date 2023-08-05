from typing import Tuple
from pygame.surface import Surface
import numpy

def array2d(surface: Surface) -> numpy.ndarray: ...
def pixels2d(surface: Surface) -> numpy.ndarray: ...
def array3d(surface: Surface) -> numpy.ndarray: ...
def pixels3d(surface: Surface) -> numpy.ndarray: ...
def array_alpha(surface: Surface) -> numpy.ndarray: ...
def pixels_alpha(surface: Surface) -> numpy.ndarray: ...
def pixels_red(surface: Surface) -> numpy.ndarray: ...
def pixels_green(surface: Surface) -> numpy.ndarray: ...
def pixels_blue(surface: Surface) -> numpy.ndarray: ...
def array_colorkey(surface: Surface) -> numpy.ndarray: ...
def make_surface(array: numpy.ndarray) -> Surface: ...
def blit_array(surface: Surface, array: numpy.ndarray) -> None: ...
def map_array(surface: Surface, array3d: numpy.ndarray) -> numpy.ndarray: ...
def use_arraytype(arraytype: str) -> None: ...
def get_arraytype() -> str: ...
def get_arraytypes() -> Tuple[str]: ...
