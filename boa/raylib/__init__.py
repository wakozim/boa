from __future__ import annotations

import os
import sys
import ctypes
from ctypes import wintypes
from enum import IntEnum, auto
from typing import Union, List, Any, Tuple


# ----------------------------
#   Aliases for ctypes types
# ----------------------------

Float = ctypes.c_float
Int = ctypes.c_int
VoidPtr = ctypes.c_void_p
UInt = ctypes.c_uint
Bool = ctypes.c_bool
CharPtr = ctypes.c_char_p
Char = ctypes.c_char


# ---------------
#   Load raylib
# ---------------

if sys.platform == 'linux':
    raylib_path = os.path.join(
            os.path.dirname(__file__),
            "raylib-5.5_linux_amd64",
            "lib",
            "libraylib.so"
    )
elif sys.platform == 'win32':
    # WARNING: I've only tested it with wine.
    # It may not work in real conditions.
    raylib_path = os.path.join(
            os.path.dirname(__file__),
            "raylib-5.5_win64_msvc16",
            "lib",
            "raylib.dll"
    )
else:
    raise RuntimeError('Unsupported platform')

raylib = ctypes.cdll.LoadLibrary(raylib_path)


# ---------------------------
#   Structures declarations
# ---------------------------


# Vector2, 2 components
class Vector2(ctypes.Structure):
    _fields_ = [
        ('x', Float),   # Vector x component
        ('y', Float)    # Vector y component
    ]

    def __str__(self) -> str:
        return f'({self.x} {self.y})'

    def __repr__(self) -> str:
        return f'Vector2({self.x}, {self.y})'

    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0

    def __add__(self, other: Vector2) -> Vector2:
        if isinstance(other, Vector2):
            return vector2_add(self, other)
        elif isinstance(other, int) or isinstance(other, float):
            return vector2_add_value(self, other)
        else:
            return NotImplemented

    def __radd__(self, other: Vector2) -> Vector2:
        if isinstance(other, Vector2):
            return vector2_add(self, other)
        elif isinstance(other, int) or isinstance(other, float):
            return vector2_add_value(self, other)
        else:
            return NotImplemented

    def __sub__(self, value: Union[Vector2, float]) -> Vector2:
        if isinstance(value, Vector2):
            return vector2_subtract(self, value)
        elif isinstance(value, float) or isinstance(value, int):
            return vector2_subtract_value(self, value)
        else:
            return NotImplemented

    def __rsub__(self, value: Union[Vector2, float]) -> Vector2:
        if isinstance(value, Vector2):
            return vector2_subtract(self, value)
        elif isinstance(value, float) or isinstance(value, int):
            return vector2_subtract_value(self, value)
        else:
            return NotImplemented

    def __mul__(self, value: Union[Vector2, float]) -> Vector2:
        if isinstance(value, Vector2):
            return vector2_multiply(self, value)
        elif isinstance(value, float) or isinstance(value, int):
            return vector2_scale(self, value)
        else:
            return NotImplemented

    def __rmul__(self, value: Union[Vector2, float]) -> Vector2:
        if isinstance(value, Vector2):
            return vector2_multiply(self, value)
        elif isinstance(value, float) or isinstance(value, int):
            return vector2_scale(self, value)
        else:
            return NotImplemented

    def __truediv__(self, other) -> Vector2:
        if isinstance(other, Vector2):
            return vector2_divide(self, other)
        elif isinstance(other, float) or isinstance(other, int):
            return Vector2(self.x / other, self.y / other)
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2):
            return NotImplemented
        return other.x == self.x and other.y == self.y


# Vector3, 3 components
class Vector3(ctypes.Structure):
    _fields_ = [
        ('x', Float),   # Vector x component
        ('y', Float),   # Vector y component
        ('z', Float)    # Vector z component
    ]


# Vector4, 4 components
class Vector4(ctypes.Structure):
    _fields_ = [
        ('x', Float),   # Vector x component
        ('y', Float),   # Vector y component
        ('z', Float),   # Vector z component
        ('w', Float)    # Vector w component
    ]


# Quaternion, 4 components (Vector4 alias)
Quaternion = Vector4;


# Matrix, 4x4 components, column major, OpenGL style, right-handed
'''
class Matrix:
    float m0, m4, m8, m12;  // Matrix first row (4 components)
    float m1, m5, m9, m13;  // Matrix second row (4 components)
    float m2, m6, m10, m14; // Matrix third row (4 components)
    float m3, m7, m11, m15; // Matrix fourth row (4 components)
'''


# Color, 4 components, R8G8B8A8 (32bit)
class Color(ctypes.Structure):
    _fields_ = [
        ("r", Char),    # Color red value
        ("g", Char),    # Color green value
        ("b", Char),    # Color blue value
        ("a", Char)     # Color alpha value
    ]


# Colors
# TODO: Maybe create enum for it?
LIGHTGRAY  = Color(200, 200, 200, 255)   # Light Gray
GRAY       = Color(130, 130, 130, 255)   # Gray
DARKGRAY   = Color(80, 80, 80, 255)      # Dark Gray
YELLOW     = Color(253, 249, 0, 255)     # Yellow
GOLD       = Color(255, 203, 0, 255)     # Gold
ORANGE     = Color(255, 161, 0, 255)     # Orange
PINK       = Color(255, 109, 194, 255)   # Pink
RED        = Color(230, 41, 55, 255)     # Red
MAROON     = Color(190, 33, 55, 255)     # Maroon
GREEN      = Color(0, 228, 48, 255)      # Green
LIME       = Color(0, 158, 47, 255)      # Lime
DARKGREEN  = Color(0, 117, 44, 255)      # Dark Green
SKYBLUE    = Color(102, 191, 255, 255)   # Sky Blue
BLUE       = Color(0, 121, 241, 255)     # Blue
DARKBLUE   = Color(0, 82, 172, 255)      # Dark Blue
PURPLE     = Color(200, 122, 255, 255)   # Purple
VIOLET     = Color(135, 60, 190, 255)    # Violet
DARKPURPLE = Color(112, 31, 126, 255)    # Dark Purple
BEIGE      = Color(211, 176, 131, 255)   # Beige
BROWN      = Color(127, 106, 79, 255)    # Brown
DARKBROWN  = Color(76, 63, 47, 255)      # Dark Brown
WHITE      = Color(255, 255, 255, 255)   # White
BLACK      = Color(0, 0, 0, 255)         # Black
BLANK      = Color(0, 0, 0, 0)           # Blank (Transparent)
MAGENTA    = Color(255, 0, 255, 255)     # Magenta
RAYWHITE   = Color(245, 245, 245, 255)   # White (raylib logo)


# Rectangle, 4 components
class Rectangle(ctypes.Structure):
    _fields_ = [
        ('x', Float),       # Rectangle top-left corner position x
        ('y', Float),       # Rectangle top-left corner position y
        ('width', Float),   # Rectangle width
        ('height', Float)   # Rectangle height
    ]


# Image, pixel data stored in CPU memory (RAM)
class Image(ctypes.Structure):
    _fields_ = [
        ('data', VoidPtr),  # Image raw data
        ('width', Int),     # Image base width
        ('height', Int),    # Image base height
        ('mipmaps', Int),   # Mipmap levels, 1 by default
        ('format', Int)     # Data format (PixelFormat type)
    ]


# Texture, tex data stored in GPU memory (VRAM)
class Texture(ctypes.Structure):
    _fields_ = [
        ("id", Int),        # OpenGL texture id
        ("width", Int),     # Texture base width
        ("height", Int),    # Texture base height
        ("mipmaps", Int),   # Mipmap levels, 1 by default
        ("format", Int)     # Data format (PixelFormat type)
    ]


# Texture2D, same as Texture
Texture2D = Texture


# TextureCubemap, same as Texture
TextureCubemap = Texture


# RenderTexture, fbo for texture rendering
class RenderTexture(ctypes.Structure):
    _fields_ = [
        ("id", Int),            # OpenGL framebuffer object id
        ("texture", Texture),   # Color buffer attachment texture
        ("depth", Texture)      # Depth buffer attachment texture
    ]


RenderTexture2D = RenderTexture


# ----------------------
#   Enums declarations
# ----------------------

class TextureFilter(IntEnum):
    # No filter, just pixel approximation
    POINT = auto(0),
    # Linear filtering
    BILINEAR = auto(),
    # Trilinear filtering (linear with mipmaps)
    TRILINEAR = auto(),
    # Anisotropic filtering 4x
    ANISOTROPIC_4X = auto(),
    # Anisotropic filtering 8x
    ANISOTROPIC_8X = auto(),
    # Anisotropic filtering 16x
    ANISOTROPIC_16X = auto(),


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


def _wrapper(func, result_type, *args_types):
    func.argtypes = args_types
    func.restype = result_type
    return func


# raylib.h functions bindings

_DrawFPS = _wrapper(raylib.DrawFPS, None, Int, Int)
_ColorFromHSV = _wrapper(raylib.ColorFromHSV, Color, Float, Float, Float)
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
_DrawLineEx = _wrapper(raylib.DrawLineEx, None, Vector2, Vector2, Float, Color)
_GetFrameTime = _wrapper(raylib.GetFrameTime, Float)
_IsKeyPressed = _wrapper(raylib.IsKeyPressed, Bool, Int)
_SetTraceLogLevel = _wrapper(raylib.SetTraceLogLevel, None, Int)
_LoadRenderTexture = _wrapper(raylib.LoadRenderTexture, RenderTexture, Int, Int)
_BeginTextureMode = _wrapper(raylib.BeginTextureMode, None, RenderTexture2D)
_EndTextureMode = _wrapper(raylib.EndTextureMode, None)
# Draw text (using default font)
# RLAPI void DrawText(const char *text, int posX, int posY, int fontSize, Color color);
_DrawText = _wrapper(raylib.DrawText, None, CharPtr, Int, Int, Int, Color)
# Measure string width for default font
# RLAPI int MeasureText(const char *text, int fontSize);
_MeasureText = _wrapper(raylib.MeasureText, Int, CharPtr, Int)
# Draw a Texture2D
_DrawTexture = _wrapper(raylib.DrawTexture, None, Texture2D, Int, Int, Color)
# Draw a Texture2D with extended parameters
_DrawTextureEx = _wrapper(raylib.DrawTextureEx, None, Texture2D, Vector2, Float, Float, Color)
# Set texture scaling filter mode
_SetTextureFilter = _wrapper(raylib.SetTextureFilter, None, Texture2D, Int)
# Draw a part of a texture defined by a rectangle with 'pro' parameters
_DrawTexturePro = _wrapper(raylib.DrawTexturePro, None, Texture2D, Rectangle, Rectangle, Vector2, Float, Color)
# RLAPI void DrawCircleV(Vector2 center, float radius, Color color)
# Draw a color-filled circle (Vector version)
_DrawCircleV = _wrapper(raylib.DrawCircleV, None, Vector2, Float, Color)
# RLAPI Color ColorAlpha(Color color, float alpha)
# Get color with alpha applied, alpha goes from 0.0f to 1.0f
_ColorAlpha = _wrapper(raylib.ColorAlpha, Color, Color, Float)


def draw_fps(x: int, y: int) -> None:
    _DrawFPS(int(x), int(y))


def color_from_hsv(hue: float, saturation: float, value: float) -> Color:
    return _ColorFromHSV(float(hue), float(saturation), float(value))


def load_render_texture(width: int, height: int) -> RenderTexture:
    return _LoadRenderTexture(int(width), int(height))


def set_trace_log_level(level: int) -> None:
    _SetTraceLogLevel(level)


def set_texture_filter(texture: Texture, filter_: int) -> None:
    _SetTextureFilter(texture, int(filter_))


def init_window(width: int, height: int, title: str) -> None:
    _InitWindow(int(width), int(height), title.encode('UTF-8'))


def close_window() -> None:
    _CloseWindow()


def draw_rectangle(x: int, y: int, width: int, height: int, color: Color) -> None:
    _DrawRectangle(int(x), int(y), int(width), int(height), color)


def draw_line_ex(start_pos: Vector2, end_pos: Vector2, thick: float, color: Color):
    _DrawLineEx(start_pos, end_pos, float(thick), color)


def draw_text(text: str, x: int, y: int, font_size: int, color: Color) -> None:
    _DrawText(text.encode('UTF-8'), int(x), int(y), int(font_size), color)


def measure_text(text: str, font_size: int) -> int:
    return _MeasureText(text.encode('UTF-8'), int(font_size))


def draw_texture(texture: Texture2D, x: int, y: int, tint: Color) -> None:
    _DrawTexture(texture, int(x), int(y), tint)


def draw_texture_ex(texture: Texture2D, position: Vector2, rotation: float, scale: float, tint: Color):
    _DrawTextureEx(texture, position, float(rotation), float(scale), tint)


def draw_texture_pro(texture: Texture2D, source: Rectangle, dest: Rectangle, origin: Vector2, rotation: float, tint: Color):
    _DrawTexturePro(texture, source, dest, origin, float(rotation), tint)


def draw_rectangle_v(position: Vector2, size: Vector2, color: Color) -> None:
    _DrawRectangleV(position, size, color)


def draw_circle_v(position: Vector2, radius: float, color: Color) -> None:
    _DrawCircleV(position, float(radius), color)


def set_target_fps(fps: int) -> None:
    _SetTargetFPS(int(fps))


def window_should_close() -> bool:
    return _WindowShouldClose()


def begin_drawing() -> None:
    _BeginDrawing()


def begin_texture_mode(texture: RenderTexture2D) -> None:
    _BeginTextureMode(texture)


def end_texture_mode() -> None:
    _EndTextureMode()


def get_screen_width() -> int:
    return _GetScreenWidth()


def get_screen_height() -> int:
    return _GetScreenHeight()


def clear_background(color: Color) -> None:
    _ClearBackground(color)


def get_frame_time() -> float:
    return _GetFrameTime()


def end_drawing() -> None:
    _EndDrawing()


def is_key_pressed(key: int) -> None:
    return _IsKeyPressed(int(key))


def color_alpha(color: Color, alpha: float) -> Color:
    return _ColorAlpha(color, float(alpha))


# raymath.h functions bindings

_Vector2Add = _wrapper(raylib.Vector2Add, Vector2, Vector2, Vector2)
_Vector2Divide = _wrapper(raylib.Vector2Divide, Vector2, Vector2, Vector2)
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


def vector2_divide(vec1: Vector2, vec2: Vector2) -> Vector2:
    return _Vector2Divide(vec1, vec2)


def vector2_lerp(vec1: Vector2, vec2: Vector2, amount: float) -> Vector2:
    return _Vector2Lerp(vec1, vec2, float(amount))


def vector2_scale(vec: Vector2, scale: float) -> Vector2:
    return _Vector2Scale(vec, scale)


def vector2_subtract(vec1: Vector2, vec2: Vector2) -> Vector2:
    return _Vector2Subtract(vec1, vec2)


def vector2_subtract_value(vec: Vector2, value: float) -> Vector2:
    return _Vector2SubtractValue(vec, value)
