"""
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * - Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * - Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * - Neither the name of prim nor the names of its contributors may be used to
 * endorse or promote products derived from this software without specific prior
 * written permission.
 *
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
"""
import matplotlib.ticker
import math
import ssplot

class MultilinePlot(object):
  """
  This class create plots with multiple lines from similar data.
  """

  _kwargs = {}

  def __init__(self, plt, xdata, ydatas):
    """
    This constructs default plot information
    """
    for ydata in ydatas:
      assert len(xdata) == len(ydata)

    self._plt = plt
    self._xdata = xdata
    self._ydatas = ydatas
    self._num_lines = len(self._ydatas)

    self._plot_style = ssplot.PlotStyle.default()
    self._figure_size = ssplot.FigureSize.parse(ssplot.FigureSize.default())
    self._title = None
    self._xlabel = None
    self._ylabel = None
    self._data_labels = None
    self._xmin = None
    self._xmax = None
    self._ymin = None
    self._ymax = None
    self._xauto_frame = 0.0
    self._yauto_frame = 0.0
    self._xgrid = True
    self._ygrid = True
    self._grid_style = ssplot.GridStyle.default()
    self._xmajor_ticks = 10
    self._xminor_ticks = 20
    self._ymajor_ticks = 10
    self._yminor_ticks = 20
    self._legend_location = 'upper left'
    self._legend_columns = 1
    self._legend_title = None
    self._xscale = None
    self._yscale = None
    self._xticklabels_verbose = False
    self._yticklabels_verbose = False

  def set_plot_style(self, value):
    assert value in ssplot.PlotStyle.styles()
    self._plot_style = value

  def set_figure_size(self, value):
    self._figure_size = ssplot.FigureSize.parse(value)

  def set_title(self, value):
    self._title = value

  def set_xlabel(self, value):
    self._xlabel = value

  def set_ylabel(self, value):
    self._ylabel = value

  def set_data_labels(self, value):
    assert len(value) == self._num_lines
    self._data_labels = value

  def set_xmin(self, value):
    self._xmin = value

  def set_xmax(self, value):
    self._xmax = value

  def set_ymin(self, value):
    self._ymin = value

  def set_ymax(self, value):
    self._ymax = value

  def set_xauto_frame(self, value):
    self._xauto_frame = value

  def set_yauto_frame(self, value):
    self._yauto_frame = value

  def set_xgrid(self, value):
    self._xgrid = bool(value)

  def set_ygrid(self, value):
    self._ygrid = bool(value)

  def set_grid_style(self, value):
    assert value in ssplot.GridStyle.styles()
    self._grid_style = value

  def set_xmajor_ticks(self, value):
    if value == None:
      self._xmajor_ticks = None
    else:
      assert value > 0
      self._xmajor_ticks = value

  def set_xminor_ticks(self, value):
    if value == None:
      self._xminor_ticks = None
    else:
      assert value > 0
      self._xminor_ticks = value

  def set_ymajor_ticks(self, value):
    if value == None:
      self._ymajor_ticks = None
    else:
      assert value > 0
      self._ymajor_ticks = value

  def set_yminor_ticks(self, value):
    if value == None:
      self._yminor_ticks = None
    else:
      assert value > 0
      self._yminor_ticks = value

  def set_legend_location(self, value):
    self._legend_location = value

  def set_legend_columns(self, value):
    assert isinstance(value, int) and value > 0
    self._legend_columns = value

  def set_legend_title(self, value):
    self._legend_title = value

  def set_xscale(self, value):
    self._xscale = value

  def set_yscale(self, value):
    self._yscale = value

  def set_xticklabels_verbose(self, value):
    self._xticklabels_verbose = bool(value)

  def set_yticklabels_verbose(self, value):
    self._yticklabels_verbose = bool(value)

  def set(self, **kwargs):
    for k in kwargs:
      value = kwargs[k]
      func = MultilinePlot._kwargs[k]
      func(self, value)

  @staticmethod
  def add_args(parser, *skip):
    for s in skip:
      assert s in MultilinePlot._kwargs.keys(), 'bad skip: {}'.format(s)
    if 'plot_style' not in skip:
      parser.add_argument('--plot_style', type=str,
                          choices=ssplot.PlotStyle.styles(),
                          help='the style of the plot')
    if 'figure_size' not in skip:
      parser.add_argument('--figure_size',
                          type=ssplot.FigureSize.parse,
                          help='the size of the figure (e.g., \'12x6\')')
    if 'title' not in skip:
      parser.add_argument('--title', type=str,
                          help='the title of the plot')
    if 'xlabel' not in skip:
      parser.add_argument('--xlabel', type=str,
                          help='the label of the x-axis')
    if 'ylabel' not in skip:
      parser.add_argument('--ylabel', type=str,
                          help='the label of the y-axis')
    if 'data_labels' not in skip:
      parser.add_argument('--data_labels', type=str, action='append',
                          help='the label of the data (give all or no labels)')
    if 'xmin' not in skip:
      parser.add_argument('--xmin', type=float, default=None,
                          help='the minimum value of the x-axis')
    if 'xmax' not in skip:
      parser.add_argument('--xmax', type=float, default=None,
                          help='the maximum value of the x-axis')
    if 'ymin' not in skip:
      parser.add_argument('--ymin', type=float, default=None,
                          help='the minimum value of the y-axis')
    if 'ymax' not in skip:
      parser.add_argument('--ymax', type=float, default=None,
                          help='the maximum value of the y-axis')
    if 'xauto_frame' not in skip:
      parser.add_argument('--xauto_frame', type=float,
                          help='percent of area to frame the x-axis')
    if 'yauto_frame' not in skip:
      parser.add_argument('--yauto_frame', type=float,
                          help='percent of area to frame the y-axis')
    if 'xgrid' not in skip:
      parser.add_argument('--xgrid', type=ssplot.str_to_bool,
                          help='whether or not to enable the x-axis grid')
    if 'ygrid' not in skip:
      parser.add_argument('--ygrid', type=ssplot.str_to_bool,
                          help='whether or not to enable the y-axis grid')
    if 'grid_style' not in skip:
      parser.add_argument('--grid_style', type=str,
                          choices=ssplot.GridStyle.styles(),
                          help='the style of the grid')
    if 'xmajor_ticks' not in skip:
      parser.add_argument('--xmajor_ticks', type=int,
                          help='number of x-axis major ticks')
    if 'xminor_ticks' not in skip:
      parser.add_argument('--xminor_ticks', type=int,
                          help='number of x-axis minor ticks')
    if 'ymajor_ticks' not in skip:
      parser.add_argument('--ymajor_ticks', type=int,
                          help='number of y-axis major ticks')
    if 'yminor_ticks' not in skip:
      parser.add_argument('--yminor_ticks', type=int,
                          help='number of y-axis minor ticks')
    if 'legend_location' not in skip:
      parser.add_argument('--legend_location', type=str,
                          help='location of legend (see Matplotlib docs)')
    if 'legend_columns' not in skip:
      parser.add_argument('--legend_columns', type=int,
                          help='number of legend columns')
    if 'legend_title' not in skip:
      parser.add_argument('--legend_title', type=str,
                          help='the title of the legend')
    if 'xscale' not in skip:
      parser.add_argument('--xscale', type=str,
                          help='the scale of the x-axis')
    if 'yscale' not in skip:
      parser.add_argument('--yscale', type=str,
                          help='the scale of the y-axis')
    if 'xticklabels_verbose' not in skip:
      parser.add_argument('--xticklabels_verbose', type=ssplot.str_to_bool,
                          help='whether or not to turn x-axis ticklabels '
                          'verbose')
    if 'yticklabels_verbose' not in skip:
      parser.add_argument('--yticklabels_verbose', type=ssplot.str_to_bool,
                          help='whether or not to turn y-axis ticklabels '
                          'verbose')

  def apply_args(self, args, *skip):
    for s in skip:
      assert s in MultilinePlot._kwargs.keys()
    if 'plot_style' not in skip and args.plot_style is not None:
      self.set_plot_style(args.plot_style)
    if 'figure_size' not in skip and args.figure_size is not None:
      self.set_figure_size(args.figure_size)
    if 'title' not in skip and args.title is not None:
      self.set_title(args.title)
    if 'xlabel' not in skip and args.xlabel is not None:
      self.set_xlabel(args.xlabel)
    if 'ylabel' not in skip and args.ylabel is not None:
      self.set_ylabel(args.ylabel)
    if 'data_labels' not in skip and args.data_labels is not None:
      self.set_data_labels(args.data_labels)
    if 'xmin' not in skip and args.xmin is not None:
      self.set_xmin(args.xmin)
    if 'xmax' not in skip and args.xmax is not None:
      self.set_xmax(args.xmax)
    if 'ymin' not in skip and args.ymin is not None:
      self.set_ymin(args.ymin)
    if 'ymax' not in skip and args.ymax is not None:
      self.set_ymax(args.ymax)
    if 'xauto_frame' not in skip and args.xauto_frame is not None:
      self.set_xauto_frame(args.xauto_frame)
    if 'yauto_frame' not in skip and args.yauto_frame is not None:
      self.set_yauto_frame(args.yauto_frame)
    if 'xgrid' not in skip and args.xgrid is not None:
      self.set_xgrid(args.xgrid)
    if 'ygrid' not in skip and args.ygrid is not None:
      self.set_ygrid(args.ygrid)
    if 'grid_style' not in skip and args.grid_style is not None:
      self.set_grid_style(args.grid_style)
    if 'xmajor_ticks' not in skip and args.xmajor_ticks is not None:
      self.set_xmajor_ticks(args.xmajor_ticks)
    if 'xminor_ticks' not in skip and args.xminor_ticks is not None:
      self.set_xminor_ticks(args.xminor_ticks)
    if 'ymajor_ticks' not in skip and args.ymajor_ticks is not None:
      self.set_ymajor_ticks(args.ymajor_ticks)
    if 'yminor_ticks' not in skip and args.yminor_ticks is not None:
      self.set_yminor_ticks(args.yminor_ticks)
    if 'legend_location' not in skip and args.legend_location is not None:
      self.set_legend_location(args.legend_location)
    if 'legend_columns' not in skip and args.legend_columns is not None:
      self.set_legend_columns(args.legend_columns)
    if 'legend_title' not in skip and args.legend_title is not None:
      self.set_legend_title(args.legend_title)
    if 'xscale' not in skip and args.xscale is not None:
      self.set_xscale(args.xscale)
    if 'yscale' not in skip and args.yscale is not None:
      self.set_yscale(args.yscale)
    if ('xticklabels_verbose' not in skip and
        args.xticklabels_verbose is not None):
      self.set_xticklabels_verbose(args.xticklabels_verbose)
    if ('yticklabels_verbose' not in skip and
        args.yticklabels_verbose is not None):
      self.set_yticklabels_verbose(args.yticklabels_verbose)

  def plot(self, plotfile):
    # create figure
    fig = self._plt.figure(figsize=self._figure_size)
    ax = fig.add_subplot(1, 1, 1)

    # create a PlotStyle object
    ps = ssplot.PlotStyle(self._plot_style, self._plt, self._num_lines)

    # compute plot bounds
    if len(self._xdata) > 0:
      xmin = self._xmin
      xmax = self._xmax
      ymin = self._ymin
      ymax = self._ymax

      if xmin == None:
        xmin = min(self._xdata)
      if xmax == None:
        xmax = max(self._xdata)
      if ymin == None:
        ymin = min(map(min, self._ydatas))
      if ymax == None:
        ymax = max(map(max, self._ydatas))
    else :
      xmin = 0
      xmax = 1
      ymin = 0
      ymax = 1

    xspan = xmax - xmin
    yspan = ymax - ymin
    xmin -= (xspan * self._xauto_frame)
    xmax += (xspan * self._xauto_frame)
    ymin -= (yspan * self._yauto_frame)
    ymax += (yspan * self._yauto_frame)
    xspan = xmax - xmin
    yspan = ymax - ymin

    # figure out where markers should be placed (target 20 markers)
    if len(self._xdata) > 1:
      mark_every = math.ceil((int(xspan) / (self._xdata[1]-self._xdata[0])) / 20)
    else:
      mark_every = 1

    # plot the lines
    if len(self._xdata) > 0:
      for idx, ydata in enumerate(self._ydatas):
        # retrieve the plot style info
        style = ps[idx]

        # create line
        line = ax.plot(self._xdata,
                       ydata,
                       color=style['color'],
                       linestyle=style['line_style'],
                       linewidth=style['line_width'],
                       marker=style['marker_style'],
                       markersize=style['marker_size'],
                       markevery=mark_every)[0]

        # set line label
        if self._data_labels is not None:
          line.set_label(self._data_labels[idx])
    else:
      ssplot.empty_text(ax, (xmax - xmin) / 2, (ymax - ymin) / 2)

    # set title
    if self._title is not None:
      ax.set_title(self._title, fontsize=ssplot.PLOT_TITLE_FONTSIZE)

    # set axis labels
    if self._xlabel is not None:
      ax.set_xlabel(self._xlabel)
    if self._ylabel is not None:
      ax.set_ylabel(self._ylabel)

    # create legend
    if len(self._xdata) > 0 and self._data_labels is not None:
      ax.legend(
        loc=self._legend_location,
        ncol=self._legend_columns, title=self._legend_title,
        fancybox=True, facecolor='white', edgecolor='black',
        framealpha=1.0)

    # set plot bounds
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # ticks
    if self._xmajor_ticks is not None:
      ax.xaxis.set_major_locator(
        matplotlib.ticker.MaxNLocator(self._xmajor_ticks))
    if self._xminor_ticks is not None:
      ax.xaxis.set_minor_locator(
        matplotlib.ticker.MaxNLocator(self._xminor_ticks))
    if self._ymajor_ticks is not None:
      ax.yaxis.set_major_locator(
        matplotlib.ticker.MaxNLocator(self._ymajor_ticks))
    if self._yminor_ticks is not None:
      ax.yaxis.set_minor_locator(
        matplotlib.ticker.MaxNLocator(self._yminor_ticks))

    # grid
    grid_kwargs = ssplot.GridStyle.style(self._grid_style)
    if self._xgrid is not None:
      ax.xaxis.grid(True, **grid_kwargs)
    if self._ygrid is not None:
      ax.yaxis.grid(True, **grid_kwargs)
    ax.set_axisbelow(True)

    # set axis scales
    if self._xscale is not None:
      if self._xscale is 'log':
        ax.set_xscale('log')
      elif self._xscale.startswith('log'):
        ax.set_xscale('log', basex=int(self._xscale[3:]))
      else:
        ax.set_xscale(self._xscale)
    if self._yscale is not None:
      if self._yscale is 'log':
        ax.set_yscale('log')
      elif self._yscale.startswith('log'):
        ax.set_yscale('log', basey=int(self._yscale[3:]))
      else:
        ax.set_yscale(self._yscale)

    # verbose tick labels
    if self._xticklabels_verbose:
      ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
      ax.ticklabel_format(axis='x', style='plain', useOffset=False)
    if self._yticklabels_verbose:
      ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
      ax.ticklabel_format(axis='y', style='plain', useOffset=False)

    # generate the plot
    fig.tight_layout()
    fig.savefig(plotfile)

MultilinePlot._kwargs = {
  'plot_style': MultilinePlot.set_plot_style,
  'figure_size': MultilinePlot.set_figure_size,
  'title': MultilinePlot.set_title,
  'xlabel': MultilinePlot.set_xlabel,
  'ylabel': MultilinePlot.set_ylabel,
  'data_labels': MultilinePlot.set_data_labels,
  'xmin': MultilinePlot.set_xmin,
  'xmax': MultilinePlot.set_xmax,
  'ymin': MultilinePlot.set_ymin,
  'ymax': MultilinePlot.set_ymax,
  'xauto_frame': MultilinePlot.set_xauto_frame,
  'yauto_frame': MultilinePlot.set_yauto_frame,
  'xgrid': MultilinePlot.set_xgrid,
  'ygrid': MultilinePlot.set_ygrid,
  'xmajor_ticks': MultilinePlot.set_xmajor_ticks,
  'xminor_ticks': MultilinePlot.set_xminor_ticks,
  'ymajor_ticks': MultilinePlot.set_ymajor_ticks,
  'yminor_ticks': MultilinePlot.set_yminor_ticks,
  'legend_location': MultilinePlot.set_legend_location,
  'legend_columns': MultilinePlot.set_legend_columns,
  'legend_title': MultilinePlot.set_legend_title,
  'xscale': MultilinePlot.set_xscale,
  'yscale': MultilinePlot.set_yscale,
  'xticklabels_verbose': MultilinePlot.set_xticklabels_verbose,
  'yticklabels_verbose': MultilinePlot.set_yticklabels_verbose
}
