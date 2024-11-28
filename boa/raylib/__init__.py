from __future__ import annotations

import os
import ctypes
from enum import IntEnum, Enum, auto
from typing import Union


# ----------------------------
#   Aliases for ctypes types
# ----------------------------

Float = ctypes.c_float
Int = ctypes.c_int
Bool = ctypes.c_bool
CharPtr = ctypes.c_char_p
Char = ctypes.c_char


# ---------------
#   Load raylib
# ---------------

raylib_path = os.path.join(
        os.path.dirname(__file__),
        "raylib-5.5_linux_amd64",
        "lib",
        "libraylib.so"
)
raylib = ctypes.cdll.LoadLibrary(raylib_path)


# ---------------------------
#   Structures declarations
# ---------------------------

class Vector2(ctypes.Structure):
    _fields_ = [
        ("x", Float),
        ("y", Float)
    ]

    def __str__(self) -> str:
        return f'<Vector2 x={self.x}, y={self.y}>'

    def __bool__(self) -> bool:
        return self.x != 0 and self.y != 0

    def __add__(self, value: Vector2) -> Vector2:
        if isinstance(value, Vector2):
            return vector2_add(self, value)
    
    def __sub__(self, value: Union[Vector2, float]) -> Vector2:
        if isinstance(value, Vector2):
            return vector2_subtract(self, value)
        elif isinstance(value, float) or isinstance(value, int):
            return vector2_subtract_value(self, ctypes.c_float(value))

    def __mul__(self, value: Union[Vector2, float]) -> Vector2:
        if isinstance(value, Vector2):
            return vector2_multiply(self, value)
        elif isinstance(value, float) or isinstance(value, int):
            return vector2_scale(self, ctypes.c_float(value))

    def __eq__(self, vector: Vector2) -> bool:
        if isinstance(vector, Vector2):
            return vector.x == self.x and vector.y == self.y
        else:
            return False


class Color(ctypes.Structure):
    _fields_ = [
        ("r", Char),
        ("g", Char),
        ("b", Char),
        ("a", Char)
    ]


# Colors
# TODO: Maybe create enum for it?
LIGHTGRAY  = Color( 200, 200, 200, 255 )   # Light Gray
GRAY       = Color( 130, 130, 130, 255 )   # Gray
DARKGRAY   = Color( 80, 80, 80, 255 )      # Dark Gray
YELLOW     = Color( 253, 249, 0, 255 )     # Yellow
GOLD       = Color( 255, 203, 0, 255 )     # Gold
ORANGE     = Color( 255, 161, 0, 255 )     # Orange
PINK       = Color( 255, 109, 194, 255 )   # Pink
RED        = Color( 230, 41, 55, 255 )     # Red
MAROON     = Color( 190, 33, 55, 255 )     # Maroon
GREEN      = Color( 0, 228, 48, 255 )      # Green
LIME       = Color( 0, 158, 47, 255 )      # Lime
DARKGREEN  = Color( 0, 117, 44, 255 )      # Dark Green
SKYBLUE    = Color( 102, 191, 255, 255 )   # Sky Blue
BLUE       = Color( 0, 121, 241, 255 )     # Blue
DARKBLUE   = Color( 0, 82, 172, 255 )      # Dark Blue
PURPLE     = Color( 200, 122, 255, 255 )   # Purple
VIOLET     = Color( 135, 60, 190, 255 )    # Violet
DARKPURPLE = Color( 112, 31, 126, 255 )    # Dark Purple
BEIGE      = Color( 211, 176, 131, 255 )   # Beige
BROWN      = Color( 127, 106, 79, 255 )    # Brown
DARKBROWN  = Color( 76, 63, 47, 255 )      # Dark Brown
WHITE      = Color( 255, 255, 255, 255 )   # White
BLACK      = Color( 0, 0, 0, 255 )         # Black
BLANK      = Color( 0, 0, 0, 0 )           # Blank (Transparent)
MAGENTA    = Color( 255, 0, 255, 255 )     # Magenta
RAYWHITE   = Color( 245, 245, 245, 255 )   # White (raylib logo)


# ----------------------
#   Enums declarations
# ----------------------

class TraceLogLevel(IntEnum):
    # Display all logs
    ALL     = auto(0)
    # Trace logging, intended for internal use only
    TRACE   = auto()
    # Debug logging, used for internal debugging,
    # it should be disabled on release builds
    DEBUG   = auto()
    # Info logging, used for program execution info
    INFO    = auto()
    # Warning logging, used on recoverable failures
    WARNING = auto()
    # Error logging, used on unrecoverable failures
    ERROR   = auto()
    # Fatal logging, used to abort program: exit(EXIT_FAILURE)
    FATAL   = auto()
    # Disable logging
    NONE    = auto()


class KeyboardKey(IntEnum):
    NULL            = 0,        # Key: NULL, used for no key pressed
    # Alphanumeric keys
    APOSTROPHE      = 39,       # Key: '
    COMMA           = 44,       # Key: ,
    MINUS           = 45,       # Key: -
    PERIOD          = 46,       # Key: .
    SLASH           = 47,       # Key: /
    ZERO            = 48,       # Key: 0
    ONE             = 49,       # Key: 1
    TWO             = 50,       # Key: 2
    THREE           = 51,       # Key: 3
    FOUR            = 52,       # Key: 4
    FIVE            = 53,       # Key: 5
    SIX             = 54,       # Key: 6
    SEVEN           = 55,       # Key: 7
    EIGHT           = 56,       # Key: 8
    NINE            = 57,       # Key: 9
    SEMICOLON       = 59,       # Key: ;
    EQUAL           = 61,       # Key: =
    A               = 65,       # Key: A | a
    B               = 66,       # Key: B | b
    C               = 67,       # Key: C | c
    D               = 68,       # Key: D | d
    E               = 69,       # Key: E | e
    F               = 70,       # Key: F | f
    G               = 71,       # Key: G | g
    H               = 72,       # Key: H | h
    I               = 73,       # Key: I | i
    J               = 74,       # Key: J | j
    K               = 75,       # Key: K | k
    L               = 76,       # Key: L | l
    M               = 77,       # Key: M | m
    N               = 78,       # Key: N | n
    O               = 79,       # Key: O | o
    P               = 80,       # Key: P | p
    Q               = 81,       # Key: Q | q
    R               = 82,       # Key: R | r
    S               = 83,       # Key: S | s
    T               = 84,       # Key: T | t
    U               = 85,       # Key: U | u
    V               = 86,       # Key: V | v
    W               = 87,       # Key: W | w
    X               = 88,       # Key: X | x
    Y               = 89,       # Key: Y | y
    Z               = 90,       # Key: Z | z
    LEFT_BRACKET    = 91,       # Key: [
    BACKSLASH       = 92,       # Key: '\'
    RIGHT_BRACKET   = 93,       # Key: ]
    GRAVE           = 96,       # Key: `
    # Function keys
    SPACE           = 32,       # Key: Space
    ESCAPE          = 256,      # Key: Esc
    ENTER           = 257,      # Key: Enter
    TAB             = 258,      # Key: Tab
    BACKSPACE       = 259,      # Key: Backspace
    INSERT          = 260,      # Key: Ins
    DELETE          = 261,      # Key: Del
    RIGHT           = 262,      # Key: Cursor right
    LEFT            = 263,      # Key: Cursor left
    DOWN            = 264,      # Key: Cursor down
    UP              = 265,      # Key: Cursor up
    PAGE_UP         = 266,      # Key: Page up
    PAGE_DOWN       = 267,      # Key: Page down
    HOME            = 268,      # Key: Home
    END             = 269,      # Key: End
    CAPS_LOCK       = 280,      # Key: Caps lock
    SCROLL_LOCK     = 281,      # Key: Scroll down
    NUM_LOCK        = 282,      # Key: Num lock
    PRINT_SCREEN    = 283,      # Key: Print screen
    PAUSE           = 284,      # Key: Pause
    F1              = 290,      # Key: F1
    F2              = 291,      # Key: F2
    F3              = 292,      # Key: F3
    F4              = 293,      # Key: F4
    F5              = 294,      # Key: F5
    F6              = 295,      # Key: F6
    F7              = 296,      # Key: F7
    F8              = 297,      # Key: F8
    F9              = 298,      # Key: F9
    F10             = 299,      # Key: F10
    F11             = 300,      # Key: F11
    F12             = 301,      # Key: F12
    LEFT_SHIFT      = 340,      # Key: Shift left
    LEFT_CONTROL    = 341,      # Key: Control left
    LEFT_ALT        = 342,      # Key: Alt left
    LEFT_SUPER      = 343,      # Key: Super left
    RIGHT_SHIFT     = 344,      # Key: Shift right
    RIGHT_CONTROL   = 345,      # Key: Control right
    RIGHT_ALT       = 346,      # Key: Alt right
    RIGHT_SUPER     = 347,      # Key: Super right
    KB_MENU         = 348,      # Key: KB menu
    # Keypad keys
    KP_0            = 320,      # Key: Keypad 0
    KP_1            = 321,      # Key: Keypad 1
    KP_2            = 322,      # Key: Keypad 2
    KP_3            = 323,      # Key: Keypad 3
    KP_4            = 324,      # Key: Keypad 4
    KP_5            = 325,      # Key: Keypad 5
    KP_6            = 326,      # Key: Keypad 6
    KP_7            = 327,      # Key: Keypad 7
    KP_8            = 328,      # Key: Keypad 8
    KP_9            = 329,      # Key: Keypad 9
    KP_DECIMAL      = 330,      # Key: Keypad .
    KP_DIVIDE       = 331,      # Key: Keypad /
    KP_MULTIPLY     = 332,      # Key: Keypad *
    KP_SUBTRACT     = 333,      # Key: Keypad -
    KP_ADD          = 334,      # Key: Keypad +
    KP_ENTER        = 335,      # Key: Keypad Enter
    KP_EQUAL        = 336,      # Key: Keypad =
    # Android key buttons
    BACK            = 4,        # Key: Android back button
    MENU            = 82,       # Key: Android menu button
    VOLUME_UP       = 24,       # Key: Android volume up button
    VOLUME_DOWN     = 25        # Key: Android volume down button


# ------------------------
#  Functions declarations
# ------------------------

def _wrapper(func: int, result_type, *args_types):
    func.argtypes = args_types
    func.restype = result_type
    return func


# raylib.h functions bindings

_ColorFromHVS = _wrapper(raylib.ColorFromHSV, Color, Float, Float, Float)
_SetTargetFPS = _wrapper(raylib.SetTargetFPS, None, Int)
_InitWindow = _wrapper(raylib.InitWindow, None, Int, Int, CharPtr)
_CloseWindow = _wrapper(raylib.CloseWindow, None)
_WindowShouldClose = _wrapper(raylib.WindowShouldClose, Bool)
_BeginDrawing = _wrapper(raylib.BeginDrawing, None)
_EndDrawing = _wrapper(raylib.EndDrawing, None)
_GetScreenWidth = _wrapper(raylib.GetScreenWidth, Int)
_GetScreenHeight = _wrapper(raylib.GetScreenHeight, Int)
_ClearBackground = _wrapper(raylib.ClearBackground, None, Color)
_DrawRectangle = _wrapper(raylib.DrawRectangle, None, Int, Int, Int, Int, Color)
_DrawRectangleV = _wrapper(raylib.DrawRectangleV, None, Vector2, Vector2, Color)
_GetFrameTime = _wrapper(raylib.GetFrameTime, Float)
_IsKeyPressed = _wrapper(raylib.IsKeyPressed, Bool, Int)
_SetTraceLogLevel = _wrapper(raylib.SetTraceLogLevel, None, Int)



def set_trace_log_level(level: int) -> None:
    _SetTraceLogLevel(level)


def init_window(width: int, height: int, title: str) -> None:
    _InitWindow(int(width), int(height), title.encode('UTF-8'))


def close_window() -> None:
    _CloseWindow()


def draw_rectangle(x, y, width, height, color) -> None:
    _DrawRectangle(int(x), int(y), int(width), int(height), color)


def draw_rectangle_v(position: Vector2, size: Vector2, color: Color) -> None:
    _DrawRectangleV(position, size, color)


def set_target_fps(fps: int) -> None:
    _SetTargetFPS(int(fps))


def window_should_close() -> bool:
    return _WindowShouldClose()


def begin_drawing() -> None:
    _BeginDrawing()


def clear_background(color: Color) -> None:
    _ClearBackground(color)


def get_frame_time() -> float:
    return _GetFrameTime()


def end_drawing() -> None:
    _EndDrawing()


def is_key_pressed(key: int) -> None:
    return _IsKeyPressed(int(key))


# raymath.h functions bindings

_Vector2Add = _wrapper(raylib.Vector2Add, Vector2, Vector2, Vector2)
_Vector2Lerp = _wrapper(raylib.Vector2Lerp, Vector2, Vector2, Vector2, Float)
_Vector2Multiply = _wrapper(raylib.Vector2Multiply, Vector2, Vector2, Vector2)
_Vector2Scale = _wrapper(raylib.Vector2Scale, Vector2, Vector2, Float)
_Vector2Subtract = _wrapper(raylib.Vector2Subtract, Vector2, Vector2, Vector2)
_Vector2SubtractValue = _wrapper(raylib.Vector2SubtractValue, Vector2, Vector2, Float)
_Lerp = _wrapper(raylib.Lerp, Float, Float, Float, Float)


def lerp(start: float, end: float, amount: float) -> float:
    return _Lerp(float(start), float(end), float(amount))


def vector2_multiply(vec1: Vector2, vec2: Vector2) -> Vector2:
    return _Vector2Multiply(vec1, vec2)


def vector2_add(vec1: Vector2, vec2: Vector2) -> Vector2:
    return _Vector2Add(vec1, vec2)


def vector2_lerp(vec1: Vector2, vec2: Vector2, amount: float) -> Vector2:
    return _Vector2Lerp(vec1, vec2, float(amount))


def vector2_scale(vec: Vector2, scale: float) -> Vector2:
    return _Vector2Scale(vec, scale)


def vector2_subtract(vec1: Vector2, vec2: float) -> Vector2:
    return _Vector2Subtract(vec1, vec2)


def vector2_subtract_value(vec: Vector2, value: float) -> Vector2:
    return _Vector2SubtractValue(vec, value)
