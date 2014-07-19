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
# maybe a functions for:
# optional axis legends

import subprocess

LINE = 1
HISTOGRAM = 2

X_AXIS_VALUE_WIDTH = 15


class Plot(object):
    def __init__(self, x, y = None, plot_type = LINE):
        # allow histograms to input a single vector
        if y is None:
            y = [1] * len(x)
        # make sure values are sorted by ascending x values
        self.x_values, self.y_values = zip(*sorted(zip(x, y)))
        self._set_tty_size()
        self.y_axis_width = 9
        self.x_axis_height = 2
        self._set_min_and_max_values()
        self.plot_type = plot_type
        if self.plot_type == HISTOGRAM:
            self._histogramize_data()
            self._set_min_and_max_values()

        self.canvas = [[' '] * (self.term_width - self.y_axis_width)
                       for row in range(self.term_height - self.x_axis_height)]
        self.x_axis_canvas = []
        self.y_axis_canvas = []
        self._draw_plot()

    def _set_min_and_max_values(self):
        self.min_x = self.x_values[0]
        self.max_x = self.x_values[-1]
        self.span_x = self.max_x - self.min_x
        self.min_y = min(self.y_values)
        self.max_y = max(self.y_values)
        self.span_y = self.max_y - self.min_y

    def _set_tty_size(self):
        """Mac and linux usually have stty installed, windows users can change
        this to use the console module but I don't have a windows
        machine to test that.

        """
        try:
            rows, columns = subprocess.check_output(['stty', 'size']).split()
            self.term_width = int(columns) - X_AXIS_VALUE_WIDTH
            self.term_height = int(int(rows) * .75)
        except Exception:
            self.term_width = 60
            self.term_height = 17

    def _histogramize_data(self):
        """Lump our input data into buckets.  Each column is a bucket

        """
        num_buckets = self.term_width - self.y_axis_width
        self.bucket_width = self.span_x / float(num_buckets)
        new_x_values = []
        for i in range(num_buckets):
            bucket_base_value = self.min_x + i * self.bucket_width
            new_x_values.append(bucket_base_value)
        new_y_values = [0] * num_buckets
        for x_val, y_val in zip(self.x_values, self.y_values):
            which_bucket = min(num_buckets - 1,
                               max(0,
                                   int((x_val - self.min_x) / float(self.bucket_width))))
            new_y_values[which_bucket] += y_val

        self.x_values = new_x_values
        self.x_values[-1] = self.max_x  # gross...
        self.y_values = new_y_values

    def _draw_plot(self):
        self._create_axis()
        self._fill_values()
        self._draw()

    def value_to_coords(value):
        pass

    def coords_to_value(x, y):
        pass

    def _create_axis(self):
        """For now draw every other value on the y axis and 2 endpoint values
        on the x axis because that's easy.

        I am not proud of this...

        """
        # we'll create the y axis from the bottom up because its
        # easier to think about it that way
        num_y_steps = self.term_height - self.x_axis_height
        for i in range(num_y_steps):
            if i % 2 == 0 or i == num_y_steps:
                val = self.span_y / float(num_y_steps - 1) * i + self.min_y
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
        max_x_str = str(self.max_x)

        x_axis_width = self.term_width - self.y_axis_width
        lines = [' ' * (self.y_axis_width - 1), '|']
        values = [' ' * (self.y_axis_width)]
        x = 0

        col_width = self.span_x / x_axis_width
        while x < x_axis_width - 1:
            if x % X_AXIS_VALUE_WIDTH == 0:
                v = self.min_x + x * col_width
                v = str(v)[:12]
                if len(v) + x < x_axis_width - 2:
                    lines.append('|' + (len(v)-1) * overscore)
                    values.append(v)
                    x += len(v)
                else:
                    lines.append(overscore)
                    values.append(' ')
                    x += 1
            else:
                lines.append(overscore)
                values.append(' ')
                x += 1
        lines += '|'
        values += max_x_str
        self.x_axis_canvas.append(''.join(lines))
        self.x_axis_canvas.append(''.join(values))

    def _fill_values(self):
        i = 0
        canvas_width = self.term_width - self.y_axis_width
        canvas_height = self.term_height - self.x_axis_height
        for col in range(canvas_width):
            col_x_val = col * (self.span_x / float(canvas_width)) + self.min_x
            while (i < len(self.x_values) - 2 and
                   col_x_val > self.x_values[i]):
                i += 1
            a = self.x_values[i]
            b = self.x_values[i + 1]
            x_pct = (col_x_val - a) / float(b - a)
            y_val = (1 - x_pct) * self.y_values[i] + (x_pct * self.y_values[i+1])
            y_row = int(round(((y_val - self.min_y) / self.span_y) * (canvas_height - 1)))
            y_row_inverted = canvas_height - y_row - 1
            self.canvas[y_row_inverted][col] = '*'
            if self.plot_type == HISTOGRAM:
                for row in range(y_row_inverted+1, canvas_height):
                    self.canvas[row][col] = '.'

    def _draw(self):
        print
        for row in range(self.term_height - self.x_axis_height):
            print self.y_axis_canvas[row] + ''.join(self.canvas[row])
        for row in range(self.x_axis_height):
            print self.x_axis_canvas[row]
        print
        if self.plot_type == HISTOGRAM:
            print "Bucketwidth = ", self.bucket_width


if __name__ == '__main__':
    import math
    plot_type = HISTOGRAM
    if plot_type == LINE:
        xvals, yvals = [], []
        for i in range(0, 2000, 5):
            xx = i / 100.0
            xvals.append(xx)
            yvals.append(math.sin(xx) * float(i ** 0.5))
        Plot(xvals, yvals, LINE)
    else:
        import random
        xvals = []
        for i in range(100000):
            xvals.append(random.gauss(0, 1.5))
        Plot(xvals, plot_type=HISTOGRAM)
