__all__ = [
    "Path",
]

from math import sqrt


class Path(list):
    """
    A class for storing a path on the lattice.
    Positive integers, i>0, are steps in the direction i.
    Negative integers, i<0, are backward steps in the direction i.
    Zero means no movement.
    """

    @property
    def dims(self):
        return max([max(self), abs(min(self))])

    @property
    def start(self):
        return [0] * self.dims

    @property
    def end(self):
        end = self.start
        for i in self:
            if i != 0:
                end[abs(i) - 1] += i // abs(i)
        return end

    @property
    def closed(self):
        return self.end == self.start

    @property
    def orientation(self):
        orient = []
        dims = self.dims
        for i in self:
            if i != 0 and (i not in orient or -i not in orient):
                orient.append(i)
                if len(orient) == dims:
                    break
        return orient

    def _draw_dir_(self, i):
        assert i >= 0
        if i == 1:
            return 1, 0
        if i == 2:
            return 0, 1
        if i == 3:
            return 1 / sqrt(2), 1 / sqrt(2)

    def _draw_move_(self, i):
        if i == 0:
            return 0, 0
        x, y = self._draw_dir_(abs(i))
        if i < 0:
            return -x, -y
        return x, y

    def draw(self):
        from pyx import path, deco, canvas

        c = canvas.canvas()
        x, y = 0, 0
        for i in self:
            dx, dy = self._draw_move_(i)
            ddx, ddy = dx / 10, dy / 10
            c.stroke(
                path.line(x + ddx, y + ddy, x + dx - ddx, y + dy - ddy), [deco.earrow]
            )
            x, y = x + dx, y + dy
        return c

    def _repr_png_(self):
        try:
            return self.draw()._repr_png_()
        except ImportError:
            return None

    def _repr_swg_(self):
        try:
            return self.draw()._repr_swg_()
        except ImportError:
            return None
