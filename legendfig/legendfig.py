''' Class for convenient and pretty plotting '''

import matplotlib
import matplotlib.pyplot as plt

from itertools import chain # to flatten the list of axes for NxM plot

class LegendFig:
    def __init__(self, figsize, n=1, sharex=False):
        '''
        figsize [(w,h)]: tuple with figure width x height
        n [int|string|tuple]: number of subplots (int or tuple for NxM) or type of plot ('paramspace')

        '''
        self.n = n # need later for tight layout
        self.fig = None
        self.lgd = None # if lgd is out, need to fit in the tight layout

        if n == 'paramspace':
            # definitions for the axes
            left, width = 0.13, 0.65
            bottom, height = 0.1, 0.65
            spacing = 0.005

            rect_scatter = [left, bottom, width, height]
            rect_histx = [left, bottom + height + spacing, width, 0.2]
            rect_histy = [left + width + spacing, bottom, 0.2, height]

            # start with a rectangular Figure
            self.fig = plt.figure(figsize=figsize)
            # main axis (square plot in the middle)
            self.axes = [plt.axes(rect_scatter)]
            self.axes[0].tick_params(direction='in', top=True, right=True)
            # plot on top of the main one
            self.axes.append(plt.axes(rect_histx))
            self.axes[1].tick_params(direction='in', labelbottom=False)
            # plot at the side
            self.axes.append(plt.axes(rect_histy))
            self.axes[2].tick_params(direction='in', labelleft=False)

        elif type(n) == int:
            fig, ax = plt.subplots(n,figsize=figsize, sharex=sharex)
            self.fig = fig
            # convenient if only have one subplot (not ty type axes[0] all the time)
            self.ax = ax
            # array of all our axes; new axes get added here too (e.g. two subplots, one has 2 y axes, means in total 5 axes in the list)
            self.axes = list(ax) if n > 1 else [ax]

        elif type(n) in (tuple, list):
            # e.g. (2,3) for 2x3 subplots
            if len(n) == 2:
                fig, ax = plt.subplots(n[0], n[1], figsize=figsize)
                self.fig = fig
                self.ax = ax
                self.axes = list(chain(*ax))

            # e.g.[211, 223, 224]
            elif len(n) > 2:
                self.fig = plt.figure(figsize=figsize)

                self.axes = []
                for subp in n:
                    self.axes.append(plt.subplot(subp))
            
            else:
                print_format()

        else:
            print_format()


    def legend(self, out=False, ncol=1, title=None, pos=None, axes=None):
        '''
        Create a customized legend.

        out [True|False]: legend outside of the plot in the bottom (default False)
        ncol [int]: number of columns in the legend (default 1)
        title [string]: legend title
        pos [list of int|string||float]: position of the legend (default "best").
            In case out=False: pos of legend in the plot (e.g. "upper left" or 3)
            In case out=True, moving bbox down (float order of 0.05)
        '''

        if out:
            ## draw legend at the bottom
            # the return legend object is needed later for tight layout
            handles, labels = self.axes[-1].get_legend_handles_labels()
            self.lgd = self.fig.legend(handles, labels, loc = 'lower center', ncol=ncol, fontsize=15, bbox_to_anchor=(0.5, 0.05-pos)) #labelspacing=0. )
            # remove legends from all other subplots
            for ax in self.axes:
                legend = ax.legend()
                legend.remove()

        else:
            # draw legend on each axis
            # in case these are not subplots, but one plot with two y axes, legends might crash
            # -> choose given location
            indices = range(len(self.axes)) if axes == None else axes
            for i in indices:
                if pos != None: loc = pos[i] if type(pos) == list else pos
                else: loc = None

                self.axes[i].legend(ncol=ncol, loc=loc, title=title)


    def pretty(self, large=3, stretch = None, grid='major'):
        '''
        Make the plot pretty.

        large [int]: controls fontsizes (default 3)
        stretch [None|"float"|"year"] change x axis range (default None).
            Useful for cases when the automatic ranges makes the leftmost and
        rightmost point fall right at the frame and get "eaten up"
            None: do not do anything
            "float": increase the range by 10%
            "year": increase the range by 1

        grid ["major"|"minor"]: only major grid, or also minor;
            same as the grid argument of the function ax.grid()
        '''

        ## figure legend (if present)
        if self.lgd:
            if self.lgd.get_title(): self.lgd.get_title().set_fontsize(19 + large)
            for t in self.lgd.get_texts():
                t.set_fontsize(17 + large)        

        for ax in self.axes:
            ## make better x and y limits
            if stretch:
                lims = {'x': list(ax.get_xlim()), 'y': list(ax.get_ylim())}

                strength = 0.005

                if stretch == 'float':
                    for axx in lims:
                        for i in range(2):
                            if lims[axx][i] > 0: lims[axx][i] = lims[axx][i] * (1 + (-1)**(i+1)*strength)
                            elif lims[axx][i] < 0: lims[axx][i] = lims[axx][i] * (1 + (-1)**i*strength)
                            else: lims[axx][i] = (-1)**(i+1) * 0.01


                ax.set_xlim(lims['x'][0], lims['x'][1])
                ax.set_ylim(lims['y'][0], lims['y'][1])

            ## increase tick sizes (numbers)
            for t in ax.get_xaxis().get_ticklabels():
                t.set_fontsize(15 + large)
            for t in ax.get_yaxis().get_ticklabels():
                t.set_fontsize(15 + large)

            ## increase title sizes
            ax.get_xaxis().get_label().set_fontsize(17 + large)
            ax.get_yaxis().get_label().set_fontsize(17 + large)
            ax.title.set_fontsize(20)

            ## increase legend font (if present)
            legend = ax.get_legend()
            if legend:
                if legend.get_title(): legend.get_title().set_fontsize(19 + large)
                for t in legend.get_texts():
                    t.set_fontsize(17 + large)

            ## add gridlines
            if grid: ax.grid(linestyle='--',zorder=0, which=grid)

        ## increase fontsize of texts on the figure
        for t in self.fig.get_children():
            if type(t) == matplotlib.text.Text:
                t.set_fontsize(20)


    def figure(self, name=None):
        '''
        Show the plot or save an image.

        name [string]: name of the figure to be saved (with extension)
        '''
        print('Image:', name)

        if name == None:
            print ('(NOT SAVED)')
            plt.show()
        else:
            self.fig.savefig(name, bbox_extra_artists=(self.lgd,) if self.lgd else None, bbox_inches='tight')
            print ('(saved)')


    def add_axis(self, col=None, ax=0):
        '''
        Add a second Y axis.

        col [string]: colour of the axis. Can be useful to differentiate
            the curves and see which one belongs to which Y axis
        ax [int]: a second axis is created as a twin of the given
            existing axis (default 0).
        '''
        ax2 = self.axes[ax].twinx()
        if col: ax2.tick_params(axis='y', colors=col)
        self.axes.append(ax2)

    def __del__(self):
        if self.fig:
            plt.close(self.fig)


def print_format():
    print('Provide n in format:')
    print('- int for number of subplots')
    print('- tuple (N, M) for NxM subplots')
    print('- tuple e.g. (211,223,224) for specific subplots')
    print('- "paramspace" for a central plot with 2 histos on the sides')