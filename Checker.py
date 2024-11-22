from types import FrameType
import numpy as np
import inspect
import linecache

def format_unknown_property(receive, expect, name) -> str:
    return f"Uknown {name}, expect |{", ".join(map(lambda x: f"'{x}'", map(str, expect)))}|, receive '{receive}'"

def check_primary_point(primary: str):
    props = ["x", "y", "x_flip", "y_flip", "angle1", "angle2"]
    if not primary in props:
        raise ValueError(format_unknown_property(primary, props, "primary"))

def check_unknow_type_point(p):
    if len(p) != 2:
        raise ValueError("Point is not valid, which isn't a  pair of int32")
    
def check_numpy_point(p: np.ndarray):
    if p.flatten().shape[1] != 2:
        raise ValueError("Point is not valid, which isn't a  pair of int32")
    
def check_str_length(s: str, expected_len: int, method: str = "=="):
    props = ["==", "<=", ">="]
    if not method in props:
        raise ValueError(format_unknown_property(method, props, "str length checker"))
    if method == "==":
        if not len(s) == expected_len:
            raise ValueError(f"String length is not valid, expect {method} {expected_len}")
    elif method == "<=":
        if not len(s) <= expected_len:
            raise ValueError(f"String length is not valid, expect {method} {expected_len}")
    if method == ">=":
        if not len(s) >= expected_len:
            raise ValueError(f"String length is not valid, expect {method} {expected_len}")
        
def check_overlap_point(a, b):
    if a == b:
        raise ValueError(f"Point {a} and {b} overlap")
    
def check_coefficients_standard(a: int, b: int, c: int):
    if b == 0:
        raise ValueError(f"Value b in 'ax + by + c = 0' must not be zero")
    
def check_angle(ang: int):
    if ang < 0 or ang > 360:
        raise ValueError(f"Expect angle between 0 - 360, receive {ang}")
    
def check_angle_for_rotate(ang: int):
    if ang % 90 == 0:
        raise ValueError(f"Cannot rotate the coordinate system {ang} degree")

def raise_warn(mes: str, current_frame: FrameType):
    current_line = current_frame.f_lineno
    current_file = inspect.getfile(current_frame) 
    line_content = ""
    for line_offset in range(-2, 3, 1):
        line_content += linecache.getline(current_file, current_line + line_offset).strip() + "\n    | "
    line_content = line_content[:-7:]
    print(f"Warning: {current_file} - {current_line}: {mes}\n => | {line_content}")
