from logging import warn
from types import FrameType
import numpy as np
import warnings
import math

from torch import Value

def format_unknown_property(receive, expect, name) -> str:
    return f"Uknown {name}, expect |{", ".join(map(lambda x: f"'{x}'", map(str, expect)))}|, receiving '{receive}'"

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
        
def check_coincided_point(a, b, additional_mes: str = ""):
    if a == b:
        raise ValueError(f"Point {a} coincides point {b}, which is not valid{" because " + additional_mes if not additional_mes else ""}")
    
def check_coefficients_standard(a: int, b: int, c: int):
    if b == 0:
        raise ValueError(f"Value b in 'ax + by + c = 0' must not be zero")
    
def check_angle(ang: int):
    if ang < 0 or ang > 360:
        raise ValueError(f"Expect angle between 0 - 360, receiving {ang}")
    
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
    min_allowed = 1e-5
    warn_lim = 1e-3
    if step < min_allowed:
        raise ValueError(f"Step must be greater than minimum value allowed {min_allowed}, receiving {step}")
    if step < warn_lim or math.isclose(step, warn_lim):
        raise_warn(f"Step is relatively small, receiving {step}, greater than {warn_lim} is recommended")

def check_segment_connection_mode(mode: str):
    props = ["closest", "smoothest"]
    if not mode in props:
        raise ValueError(format_unknown_property(mode, props, "segment connection mode"))

def check_sparsity(d: float):
    warn_lim = 1e-6
    if d < 0 or math.isclose(d, 0) or d > 1 or math.isclose(d, 1):
        raise ValueError(f"sparsity must be greater than 0 and less than 1, receiving {d}")
    if d < warn_lim or math.isclose(d, warn_lim):
        raise_warn("Sparsity is too low, may consumes more resources")
        

class SkibidiWarning(UserWarning):
    pass
def raise_warn(mes: str):
    Warning(mes, SkibidiWarning())
