# encoding: utf-8
# Copyright (C) 2014 by Brendan Cox

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# todo:
# better X axis
# maybe a functions for: grid_to_plot and plot_to_grid

import subprocess

class Plot(object):
    def __init__(self, x, y):
        # make sure values are sorted by ascending x values
        self.x_values, self.y_values = zip(*sorted(zip(x, y)))
        self._set_tty_size()
        self.y_axis_width = 9
        self.x_axis_height = 2
        self.canvas = [[' '] * (self.term_width - self.y_axis_width)
                       for row in range(self.term_height - self.x_axis_height)]
        self.x_axis_canvas = []
        self.y_axis_canvas = []
        self._draw_plot()

    def _set_tty_size(self):
        """Mac and linux usually have stty installed, windows users can change
        this to use console, I don't have a windows machine to test
        this out on.
        """
        try:
            rows, columns = subprocess.check_output(['stty', 'size']).split()
            self.term_width = int(columns) - 1
            self.term_height = int(int(rows) * .75)
        except Exception:
            self.term_width = 60
            self.term_height = 17

    def _draw_plot(self):
        self._create_axis()
        self._fill_values()
        self._draw()

    def _create_axis(self):
        """For now draw every other value on the y axis and 2 endpoint values
        on the x axis because that's easy.

        I am not proud of this...

        """
        min_x = self.x_values[0]
        max_x = self.x_values[-1]
        span_x = max_x - min_x
        min_y = min(self.y_values)
        max_y = max(self.y_values)
        span_y = max_y - min_y

        # we'll create the y axis from the bottom up because its easier to think about it that way
        num_y_steps = self.term_height - self.x_axis_height
        for i in range(num_y_steps):
            if i % 2 == 0 or i == num_y_steps:
                val = span_y / float(num_y_steps - 1) * i + min_y
                str_val = str(val)[0 : self.y_axis_width - 1]
                txt = '{:>{field_width}}|'.format(str_val,
                                                  field_width=(self.y_axis_width - 1))
            else:
                txt = ' ' * (self.y_axis_width - 1) + '|'
            self.y_axis_canvas.append(txt)
        self.y_axis_canvas.reverse()
        self.y_axis_canvas.append(' ' * self.y_axis_width)

        # x axis
        overscore = u"\u203E"
        self.x_axis_canvas.append(' ' * self.y_axis_width +
                                  overscore * (self.term_width - self.y_axis_width))
        min_x_str = str(min_x)
        max_x_str = str(max_x)
        fill = ' ' * (self.term_width -
                      self.y_axis_width - len(min_x_str) - len(max_x_str))
        self.x_axis_canvas.append(
            ' ' * self.y_axis_width + min_x_str + fill + max_x_str)

    def _fill_values(self):
        # todo, dedupe with create axis
        min_x = self.x_values[0]
        max_x = self.x_values[-1]
        span_x = max_x - min_x
        min_y = min(self.y_values)
        max_y = max(self.y_values)
        span_y = max_y - min_y
        i = 0
        canvas_width = self.term_width - self.y_axis_width
        canvas_height = self.term_height - self.x_axis_height
        for col in range(canvas_width):
            col_x_val = col * (span_x / float(canvas_width)) + min_x
            while (i < len(self.x_values) - 2 and
                   col_x_val > self.x_values[i]):
                i += 1
            a = self.x_values[i]
            b = self.x_values[i + 1]
            x_pct = (col_x_val - a) / float(b - a)
            y_val = (1 - x_pct) * self.y_values[i] + (x_pct * self.y_values[i+1])
            y_row = int(round(((y_val - min_y) / span_y) * (canvas_height - 1)))
            y_row_inverted = canvas_height - y_row - 1
            self.canvas[y_row_inverted][col] = '*'

    def _draw(self):
        print
        for row in range(self.term_height - self.x_axis_height):
            print self.y_axis_canvas[row] + ''.join(self.canvas[row])
        for row in range(self.x_axis_height):
            print self.x_axis_canvas[row]
        print


if __name__ == '__main__':
    import math
    xvals, yvals = [], []
    for i in range(1, 2000, 5):
        xx = i / 100.0
        xvals.append(xx)
        yvals.append(math.sin(xx) / float(i ** 0.5))
    Plot(xvals, yvals)
