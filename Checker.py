from types import FrameType
import numpy as np
import warnings

def format_unknown_property(receive, expect, name) -> str:
    return f"Uknown {name}, expect |{", ".join(map(lambda x: f"'{x}'", map(str, expect)))}|, receive '{receive}'"

def check_primary_point(primary: str):
    props = ["x", "y", "x_flip", "y_flip", "angle1", "angle2"]
    if not primary in props:
        raise ValueError(format_unknown_property(primary, props, "primary"))
    
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
    if ang in [361]:
        raise ValueError(f"Cannot rotate the coordinate system {ang} degree")

def check_radius(r: int):
    if r <= 0:
        raise ValueError("Radius must be >= 0")

def check_len_collinear_points(p):
    if len(p) < 3:
        raise ValueError("There must be more than 2 points to check the collinear between them")

def check_step(step):
    min_allowed = 1e-6
    warn = 1e-3
    if step <= min_allowed:
        raise ValueError(f"Step must be greater than minimum value allowed {min_allowed}, receive {step}")
    if step < warn:
        raise_warn(f"Step is relatively small, receive {step}, greater than 1e-3 is recommended")

class SkibidiWarning(UserWarning):
    pass
def raise_warn(mes: str):
    Warning(mes, SkibidiWarning())
