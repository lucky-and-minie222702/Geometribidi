from Geometry2D.Basis2D import *

class CoordinateSys2D:
    def __init__(self, 
                 points: list | list[Point2D] | np.ndarray, 
                 primary: str = "x", 
                 angle: int = 0, 
                 og: Tuple[int, int] = (0, 0), 
                 from_raw_points: bool = True,
                 optimize: bool = True):

        Checker.check_primary_point(primary)
        self.__primary = primary
        Checker.check_angle(angle)
        self.__angle = angle
        if from_raw_points:
            self.__points = np.array(Point2D.to_points(points, primary, angle,))
        else:
            self.__points = points
        self.__og = og
        
        if optimize:
            self.remove_duplicate()

    def remove_duplicate(self):
        unique = []
        for p in self.__points:
            if not p in unique:
                unique.append(p)
        self.__points = np.array(unique)

    @property
    def points(self):
        return self.__points
    
    @property
    def primary(self):
        return self.__primary
    
    @property
    def angle(self):
        return self.__angle

    @property
    def og(self):
        return self.__og
        
    def rotate(self, angle: int):
        for idx in range(len(self.points)):
            self.points[idx].rotate(angle)
        self.__angle = angle
    
    def set_og(self, x: float, y: float):
        self.__og = (x, y)
        for idx in range(len(self.points)):
            self.points[idx].set_og(x, y)

    def set_primary(self, primary: str):
        minn = np.min(self.points, axis=0)
        if primary == "angle2":
            self.set_og(*minn)
        for idx in range(len(self.points)):
            self.points[idx].set_primary(primary)
        self.__primary = primary

    def sort_points(self, 
                    descending: bool = False, 
                    in_place: bool = True, 
                    og: Tuple[int, int] = (0, 0)):
        
        last = (None, None)
        if self.primary == "angle1":
            last = self.og
            self.set_og(*og)
        res = np.sort(self.points, kind = "heapsort")
        if descending:
            res = np.flip(res)
        if in_place:
            self.__points = res
        else:
            return res
        if self.primary == "angle1":
            self.set_og(*last)
    
    def is_points_sorted(self) -> bool:
        return np.all(self.points[:-1] <= self.points[1:])

    def map_points(self, func, return_new: bool = False, in_place: bool = True):
        points = self.points
        for idx in range(len(self.points)):
            if in_place: 
                self.__points[idx] = func(self.__points[idx])
            if return_new:
                points[idx] = func(points[idx])
        if return_new:
            return CoordinateSys2D(points)

    def draw_graph(self) -> list:
        self.sort_points()
        graph = []
        for idx in range(len(self.points)-1):
            p1, p2 = Point2D(*self.points[idx]), Point2D(*self.points[idx+1])
            graph += Segment2D(p1, p2).connection()[:-1:] 
        return graph


    def draw_polygon(self, dividing_line: int | Line2D = -1, as_segment: bool = True) -> list[Segment2D] | list[Point2D]:
        self.sort_points()
        if dividing_line == -1:
            last_primary = self.__primary
            self.set_primary("y")
            points = self.sort_points(in_place = False)
            self.set_primary(last_primary)
            dividing_line = Line2D(
                a = 0,
                b = 1,
                c = -points[len(points)//2].y
            )
        elif isinstance(dividing_line, int):
            dividing_line = Line2D(
                a = 0,
                b = 1,
                c = -dividing_line
            )
        raw_p = dividing_line.x_y_range(0, 2)
        dp1 = Point2D(*raw_p[0])
        dp2 = Point2D(*raw_p[1])
        
        border: list[Segment2D]  = []
        points = []
        # upper hull
        points = [p for p in self.points if Fundamental2D.direction(dp1, dp2, p) <= 0]
        for idx in range(len(points)):
            points[idx].set_primary("x")
        points = sorted(points)
        for idx in range(len(points)-1):
            p1, p2 = points[idx], points[idx+1]
            border.append(Segment2D(p1, p2))
            
        points= []
        # lower hull
        points = [p for p in self.points if Fundamental2D.direction(dp1, dp2, p) > 0]
        for idx in range(len(points)):
            points[idx].set_primary("x_flip")
        points = sorted(points)
        points.reverse()
        
        border.append(Segment2D(
            border[-1].p2,
            points[0]
        ))
        
        for idx in range(len(points)-1):
            p1, p2 = points[idx], points[idx+1]
            border.append(Segment2D(p1, p2))

        border.append(Segment2D(
            border[0].p1,
            border[-1].p1
        ))

        if as_segment:
            return border
        
        graph = []
        for p in border:
            graph += p.connection()[:-1:]
        return graph

    def __repr__(self) -> str:
        return f"{self.points}"
    
    def __iter__(self):
        return iter(self.points)
    
    def __len__(self):
        return len(self.points)
