from typing import List
from math import atan2

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
    from PyQt6.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


#
# This is the class you have to complete.
#

class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()

        # sort points by descending x
        points = sorted(points, key=lambda x: x.x(), reverse=True)  # O(nlogn)

        t2 = time.time()

        # get the lowest y value
        lowest_y = min(points, key=lambda y: y.y())

        t3 = time.time()

        # line_points = graham_scan(points, lowest_y)
        # line_points = convex_hull_d_and_c(points, lowest_y)
        line_points = dc(points)
        print(dc(points))
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        n = len(line_points)
        polygon = [QLineF(line_points[i], line_points[(i + 1) % n]) for i in range(n)]

        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.20f} sec'.format(t4 - t3))
        print(t4 - t3)

    # total complexity is O(nlogn) due to the sorting of the points


def graham_scan(points: List[QPointF], start_point: QPointF) -> List[QPointF]:
    n = len(points)
    angles = [(atan2(point.y() - start_point.y(), point.x() - start_point.x()), point) for point in points]
    angles.sort()  # O(nlogn)
    hull = [start_point, angles[0][1]]
    for i in range(1, n):  # O(n)
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], angles[i][1]) <= 0:
            hull.pop()
        hull.append(angles[i][1])
    return hull


def cross_product(p1: QPointF, p2: QPointF, p3: QPointF) -> float:
    return (p2.x() - p1.x()) * (p3.y() - p1.y()) - (p2.y() - p1.y()) * (p3.x() - p1.x())


# partition all the points recursively to groups of 3 points
# merge the points together into a convex hull
def dc(points: List[QPointF]):
    # assume points is sorted
    if len(points) <= 3:
        return points

    mid = len(points) // 2
    return merge(dc(points[:mid]), dc(points[mid:]))  # left half, right half


def merge(left: List[QPointF], right: List[QPointF]):
    # Combine the two lists of QPointF objects into a single list of tuples
    points = [(point.x(), point.y()) for point in left + right]

    # Find the point with the lowest y-coordinate (breaking ties with the lowest x-coordinate)
    start = min(points, key=lambda x: (x[1], x[0]))

    # Initialize a list to store the vertex points of the convex hull
    hull_points = []

    # Find the next vertex by iterating through all other points and keeping track of the one with the
    # smallest angle relative to the start point
    current = start
    while True:
        hull_points.append(current)
        next_vertex = points[0]
        for i in range(1, len(points)):
            if (next_vertex == current) or (
                    (points[i][1] - current[1]) * (next_vertex[0] - current[0])
                    > (next_vertex[1] - current[1]) * (points[i][0] - current[0])
            ):
                next_vertex = points[i]
        current = next_vertex
        if current == start:
            break

    # Convert the vertex points back to QPointF objects
    hull_points = [QPointF(*point) for point in hull_points]

    return hull_points
