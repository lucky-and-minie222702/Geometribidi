import numpy as np
from functools import total_ordering
import Checker
from typing import Tuple, List
import math
from mpmath import radians, sin, cos, tan, sqrt
from mpmath import mp
mp.dps = 100

def in_range(x: float, start: float, end: float, only_inside: bool = False) -> bool:
    if only_inside:
        return x > start and x < end
    else:
        return (x > start or math.isclose(x, start)) and (x < end or math.isclose(x, end))

@total_ordering
class Point:
    def to_points(points, primary: str = "x") -> List["Point"]:
        points = [Point(*p, primary) for p in points]
        return points

    def __init__(self, x: float, y: float, primary: str = "x", og: Tuple[float, float] = (0, 0)):
        self.__x = x
        self.__y = y
        Checker.check_primary_point(primary)
        self.__primary = primary
        self.__angle = 0
        self.__og = og
        self.__ogxy = (self.__x, self.__y)
        
    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def xy(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @property 
    def primary(self) -> str:
        return self.__primary
    
    @property 
    def angle(self) -> float:
        return self.__angle
    
    @property
    def og(self) -> Tuple[float, float]:
        return self.__og
    
    @property
    def angle_zero(self) -> Tuple[float, float]:
        return self.__ogxy

    def set_primary(self, primary: str):
        Checker.check_primary_point(primary)
        self.__primary = primary

    def rotate_default(self):
        self.__x, self.__y = self.__ogxy

    def rotate(self, angle: float, in_place: bool = True, return_new: bool = False) -> "Point":
        Checker.check_angle(angle)
        Checker.check_angle_for_rotate(angle)
        angle += self.angle
        if angle > 360 or math.isclose(angle, 360):
            angle = angle - 360
        if in_place:
            self.__angle = angle
            angle = radians(angle)
            self.__x = self.__ogxy[0]*cos(angle) + self.__ogxy[1]*sin(angle)
            self.__y = self.__ogxy[0]*sin(angle) + self.__ogxy[1]*cos(angle)
            self.__x = float(self.__x)
            self.__y = float(self.__y)
        if return_new:
            angle = math.radians(angle)
            x = self.__ogxy[0]*cos(angle) + self.__ogxy[1]*sin(angle)
            y = self.__ogxy[0]*cos(angle) + self.__ogxy[1]*sin(angle)
            x = float(x)
            y = float(y)
            return Point(x, y)

    def set_og(self, x: float, y: float):
        self.__og = (x, y)

    def distance_to(self, other: "Point") -> float:
        return sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2
        )
    
    def shift_x(self, val: float, in_place: bool = True, return_new: bool = False) -> "Point":
        if in_place:
            self.__x += val
            self.__ogxy = (self.__x, self.__y)
        if return_new:
            return Point(self.x + val, self.y)
    
    def shift_y(self, val: float, in_place: bool = True, return_new: bool = False) -> "Point":
        if in_place:
            self.__y += val
            self.__ogxy = (self.__x, self.__y)
        if return_new:
            return Point(self.x + val, self.y)
        
    def set_xy(self, x: float, y: float, in_place: bool = True, return_new: bool = False) -> "Point":
        if in_place:
            self.__x, self.__y = x, y
            self.__ogxy = (self.__x, self.__y)
        if return_new:
            return Point(x, y)
    
    def __eq__(self, other: "Point") -> bool:
        if self.primary != "angle1" and not self.primary == "angle2":
            return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        elif self.primary == "angle1":
            line1: Line = Line.from_fixed_points(Point(*self.__og), self)
            line2: Line = Line.from_fixed_points(Point(*self.__og), other)
            line3: Line = Line(0, 1, 0)
            ang1 = line1.angle_with(line3)
            ang2 = line2.angle_with(line3)
            return math.isclose(ang1, ang2)
        else: # angle2
            return Fundamental.direction(Point(*self.__og), self, other) == 0

    def __lt__(self, other: "Point") -> bool:
        if self.primary == "x":
            if not math.isclose(self.x, other.x):
                return self.x < other.x
            else:
                return self.y < other.y
        elif self.primary == "y":
            if not math.isclose(self.y, other.y):
                return self.y < other.y
            else:
                return self.x < other.x
        elif self.primary == "x_flip":
            if not math.isclose(self.x, other.x):
                return self.x < other.x
            else:
                return self.y > other.y
        elif self.primary == "y_flip":
            if not math.isclose(self.y, other.y):
                return self.y < other.y
            else:
                return self.x > other.x
        elif self.primary == "angle1":
            line1: Line = Line.from_fixed_points(Point(*self.__og), self)
            line2: Line = Line.from_fixed_points(Point(*self.__og), other)
            line3: Line = Line(0, 1, 0)
            ang1 = line1.angle_with(line3)
            ang2 = line2.angle_with(line3)
            return ang1 < ang2
        elif self.primary == "angle2":
            return Fundamental.direction(Point(*self.__og), self, other) == -1

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __iter__(self):
        return iter([self.x, self.y])

class Fundamental:
    MAX = 1e9
    MIN = 1e-9
    Pi = math.pi
    def direction(A: Point | Tuple[float, float], B: Point | Tuple[float, float], C: Point | Tuple[float, float], return_area: bool = False) -> int | float:
        Ax, Ay = A
        Bx, By = B
        Cx, Cy = C
        area = (Bx - Ax) * (By + Ay) + (Cx - Bx) * (Cy + By) + (Ax - Cx) * (Ay + Cy)
        if return_area:
            return area
        if area < 0:
            return -1
        elif area > 0:
            return 1
        else:
            return 0
        
    def collinear(points: List[Point] | np.ndarray) -> bool:
        Checker.check_len_collinear_points(points)
        for idx in range(len(points) - 2):
            p1, p2, p3, = points[idx:idx+3:]
            if Fundamental.direction(p1, p2, p3) != 0:
                return False
        return True

@total_ordering
class Line:
    def __init__(self, a: float, b: float, c: float):
        self.__coef_a = a
        self.__coef_b = b
        self.__coef_c = c
    @property
    def coef_a(self) -> float:
        return self.__coef_a

    @property
    def coef_b(self) -> float:
        return self.__coef_b
    
    @property
    def coef_c(self) -> float:
        return self.__coef_c
    
    @property
    def coefs(self) -> Tuple[float, float, float]:
        return (self.coef_a, self.coef_b, self.coef_c)

    def intersect(self, other: "Line") -> Tuple[float, float] | int:
        a1, b1, c1 = self.coefs
        a2, b2, c2 = other.coefs
        delta = a1 * b2 - a2 * b1

        if delta == 0:
            if a1 * c2 == a2 * c1 and b1 * c2 == b2 * c1:
                # coincident
                return 1
            else:
                # parallel
                return 0
        
        delta_x = -c1 * b2 + c2 * b1
        delta_y = -a1 * c2 + a2 * c1

        x = delta_x / delta
        y = delta_y / delta

        return x, y
    
    @classmethod
    def from_slope_intercept(cls, m: float, intercept: float, is_raw: bool = False) -> "Line":
        a = m
        b = -1
        c = -intercept
        if is_raw:
            return a, b, c
        else:
            return cls(a, b, c)

    @classmethod
    def from_fixed_points(cls, p1: Point | Tuple[float, float], p2: Point | Tuple[float, float], return_raw: bool = False) -> "Line":
        if not isinstance(p1, Point):
            p1 = Point(*p1)
        if not isinstance(p2, Point):
            p2 = Point(*p2)
        a =  p2.y - p1.y
        b = p1.x - p2.x
        c = (p2.x * p1.y) - (p1.x * p2.y)
        if return_raw:
            return a, b, c
        else:
            return cls(a, b, c)

    def create_intersecting_line(self, x0: float, y0: float, angle: float, return_raw: bool = False) -> Tuple[int, int, int] | "Line":
        a, b, c = self.coefs
        theta_rad = math.radians(angle)
        
        if b == 0:
            m1 = float('inf')
        else:
            m1 = -a / b

        if m1 == float('inf'):
            m2 = math.tan(theta_rad)
        else:
            tan_theta = math.tan(theta_rad)
            m2 = (m1 + tan_theta) / (1 - m1 * tan_theta)
        
        if m2 == float('inf'):
            A, B, C = 1, 0, -x0
        else:
            A = -m2
            B = 1
            C = m2 * x0 - y0
        
        if return_raw:
            return A, B, C
        else:
            return Line(A, B, C)

    def to_slope_intercept(self) -> Tuple[float, float]:
        a, b, c = self.coefs
        if not math.isclose(b, 0):
            m = -a / b
            intercept = -c / b
        else: 
            return None, None
        return m, intercept

    def distance_to(self, p: Point) -> float:
        a, b, c = self.coefs
        top = abs(a * p.x + b * p.y + c) 
        bot = sqrt(a**2 + b**2)
        d = top / bot
        return d
    
    def angle_with(self, other: "Line", closest: bool = False) -> float:
        a1, b1, c1 = self.coefs
        a2, b2, c2 = other.coefs

        dot_product = a1 * a2 + b1 * b2
        magnitude1 = sqrt(a1**2 + b1**2)
        magnitude2 = sqrt(a2**2 + b2**2)

        if magnitude1 == 0 or magnitude2 == 0:
            # a == 0
            return None
        if closest:
            dot_product = abs(dot_product)
        cos_theta = dot_product / (magnitude1 * magnitude2)
        cos_theta = min(1, max(-1, cos_theta))
        
        theta = math.acos(cos_theta)
        theta_degrees = math.degrees(theta)
        
        return theta_degrees
    
    def x_to_y(self, x: float) -> float:
        a, b, c = self.coefs
        if not math.isclose(b, 0):
            y = -(c + a * x) / b
        else:
            y = -c / a
        return y
    
    def x_y_range(self, start: float, count: float, step: float = 1) -> List[Tuple[float, float]]:
        x = start
        res = []
        while len(res) < count:
            res.append([x, self.x_to_y(x)])
            x += step
        return res

    def x_y_dense(self, start: float, end: float, sparsity: float) -> List[Tuple[float, float]]:
        Checker.check_sparsity(sparsity)
        step = (end - start) * sparsity
        res = self.x_y_range(start, int(1 / sparsity), step)
        return res

    def __eq__(self, other: "Line") -> bool:
        a = math.isclose(self.coef_a, other.coef_a)
        b = math.isclose(self.coef_b, other.coef_b)
        c = math.isclose(self.coef_c, other.coef_c)
        return a and b and c
    
    def __lt__(self, other):
        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.coef_a}x + {self.coef_a}y + {self.coef_c} = 0"

    def __iter__(self):
        return iter([self.coef_a, self.coef_b, self.coef_c])


@total_ordering
class Segment(Line):
    def __init__(self, p1: Point | Tuple[float, float], p2: Point | Tuple[float, float], sort: bool = True):
        if not isinstance(p1, Point):
            p1 = Point(*p1)
        if not isinstance(p2, Point):
            p2 = Point(*p2)

        Checker.check_coincided_point(p1, p2)
        if p1 > p2 and sort:
            p1, p2 = p2, p1
        self.__p1 = p1 # small
        self.__p2 = p2 # large
        a, b, c = Line.from_fixed_points(p1, p2, True)
        super().__init__(a, b, c)

    @property
    def p1(self) -> Point:
        return self.__p1

    @property
    def p2(self) -> Point:
        return self.__p2
    
    @property
    def xy(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        return (self.p1.xy, self.p2.xy)
    
    @property
    def length(self) -> float:
        return self.p1.distance_to(self.p2)

    def is_on(self, p: Point) -> bool:
        x, y = p.xy
        if not math.isclose(self.x_to_y(x), y):
            return False
        if in_range(x, self.p1.x, self.p2.x) and in_range(y, self.p1.y, self.p2.y):
            return True
        return False

    def connection(self, mode: str = "closest", step: float = 1, sparsity: float = 0.1) -> List[Point]:
        Checker.check_step(step)
        Checker.check_segment_connection_mode(mode)
        last = (self.p1, self.p2)
        if self.p1 > self.p2:
            self.__p1, self.__p2 = self.p2, self.p1

        if mode == "closest":
            line = []
            movex = [0, step]
            movey = [0, step] if self.p1.y < self.p2.y else [0, -step]
            p = self.p1
            line.append(p)
            while p != self.p2:
                x, y = line[-1].x, line[-1].y
                minn1, minn2 = Fundamental.MAX, Fundamental.MAX
                for dx in movex:
                    for dy in movey:
                        if (dx, dy) == (0, 0):
                            continue
                        p_tmp = Point(x+dx, y+dy)
                        dis1 = self.distance_to(p_tmp)
                        dis2 = self.p2.distance_to(p_tmp)
                        if ((dis1 < minn1 or math.isclose(dis1, minn1)) and dis2 < minn2) or (dis1 < minn1 and (dis2 < minn2 or math.isclose(dis2, minn2))):
                            minn1 = dis1
                            minn2 = dis2
                            p = p_tmp
                line.append(p)
        elif mode == "smoothest":
            points = self.x_y_dense(self.p1.x, self.p2.x, sparsity)
            line = Point.to_points(points)

        self.__p1, self.__p2 = last
        return line

    def __eq__(self, other: "Segment") -> bool:
        return self.p1 == other.p1 and self.p2 == other.p2
    
    def __lt__(self, other):
        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.p1} - {self.p2}"
    
    def __iter__(self):
        return iter([self.p1, self.p2])

@total_ordering
class Angle:
    def __init__(self, og: Tuple[float, float] | Point, p1: Tuple[float, float] | Point, p2: Tuple[float, float] | Point):
        if not isinstance(p1, Point):
            p1 = Point(*p1)
        if not isinstance(p2, Point):
            p2 = Point(*p2)
        if not isinstance(og, Point):
            og = Point(*og)

        self.__p1 = p1
        self.__p2 = p2
        self.__og = og
        line1 = Line.from_fixed_points(self.__og, self.__p1)
        line2 = Line.from_fixed_points(self.__og, self.__p2)
        self.__sm_angle = line1.angle_with(line2, True)
        
    @property
    def sm_angle(self) -> float:
        return self.__sm_angle
    
    @property
    def lg_angle(self) -> float:
        return 360 - self.__sm_angle
    
    def __eq__(self, other: "Angle") -> bool:
        return math.isclose(self.sm_angle, other.sm_angle)
    
    def __lt__(self, other: "Angle") -> bool:
        return self.sm_angle < other.sm_angle