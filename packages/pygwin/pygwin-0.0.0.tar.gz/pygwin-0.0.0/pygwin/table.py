#!/usr/bin/env python3

'''definition of class Table'''

from . import Node, Util, Label


class Table(Node):  # pylint: disable=R0902
    '''Table nodes are two-dimensional arrays of nodes.'''

    def __init__(self, **kwargs):
        '''create a table Node.  the table is initially empty if kwarg cells
        is None.  if not None, kwarg cells must be an {(int,int):
        Node} dictionary with key=coordinate of the cell and
        value=content of the cell.  cells of which coordinates do not
        appear in the dictionary are empty.  if not None, kwarg
        colspan is an {(int,int): int} dict, indicating for each cell
        the number of columns the cell spans'''
        Node.__init__(self, **kwargs)

        #  check arguments
        cells = kwargs.get('cells', dict())
        colspan = kwargs.get('colspan', dict())
        rowspan = kwargs.get('rowspan', dict())
        Util.check_type(cells, dict, name='cells', none_accepted=True)
        Util.check_type(colspan, dict, name='colspan', none_accepted=True)
        Util.check_type(rowspan, dict, name='rowspan', none_accepted=True)

        self.__cells = dict()
        self.__rowspan = dict()
        self.__colspan = dict()
        self.__cols = 0
        self.__rows = 0
        self.__widths = None
        self.__heights = None
        for ij in cells:
            self.set_cell(ij, cells[ij],
                          colspan=colspan.get(ij, 1),
                          rowspan=rowspan.get(ij, 1))

    def __str__(self):
        return 'table'

    def __len__(self):
        return len(self.__cells)

    def new_row(self, cells, colspan=None, rowspan=None):
        '''add a row composed of cells at the bottom of the table.  cells must
        be a dictionary of {int: Node} with key=column number,
        value=cell content.  if not None, colspan and rowspan must be
        dictionaries of {int: int} with key=column number and
        value=colspan or rowspan of the cell'''
        i = self.__rows
        for j in cells:
            cs = colspan[j] if colspan is not None and j in colspan else 1
            rs = rowspan[j] if rowspan is not None and j in rowspan else 1
            self.set_cell((i, j), cells[j], colspan=cs, rowspan=rs)

    def set_span(self, ij, colspan=1, rowspan=1):
        '''set the colspan and rowspan of the ij (an int couple) cell of the
        table.  ij cell must exists otherwise ValueError is raised'''
        if ij not in self.__cells:
            raise ValueError('{} not in cells'.format(ij))
        if colspan > 1:
            if self.__colspan is None:
                self.__colspan = dict()
            self.__colspan[ij] = colspan
        if rowspan > 1:
            if self.__rowspan is None:
                self.__rowspan = dict()
            self.__rowspan[ij] = rowspan
        self.update_manager()
        self.reset_size()

    def set_cell(self, ij, node, colspan=1, rowspan=1):
        '''put node in the ij (an int couple) cell of the table with specified
        colspan and rowspan'''
        if ij in self.__cells:
            self.__cells[ij].unref()
        node = Label.node_of(node)
        self.__cells[ij] = node
        node.set_style('valign', 'center', update=False)
        self.set_span(ij, colspan=colspan, rowspan=rowspan)
        i, j = ij
        self.__rows = max(self.__rows, i + self.__cell_rows(ij))
        self.__cols = max(self.__cols, j + self.__cell_cols(ij))
        self.add_child(node)
        self.update_manager()
        self.reset_size()

    def empty(self):
        '''remove all cells from table'''
        for ij in self.__cells:
            self.__cells[ij].unref()
        self.__cols = 0
        self.__rows = 0
        self.__cells = dict()
        self.update_manager()
        self.reset_size()

    def _compute_inner_size(self):
        hspacing = self.get_style('hspacing')
        vspacing = self.get_style('vspacing')

        self.__widths = {j: 0 for j in range(self.__cols)}
        self.__heights = {i: 0 for i in range(self.__rows)}

        #  compute sizes of all cells
        s = {
            cell: self.__cells[cell].compute_size()
            for cell in self.__cells
        }

        self.__compute_column_widths(s)

        #  compute max cell height for each row
        for i in range(self.__rows):
            for j in range(self.__cols):
                if (i, j) in self.__cells:
                    _, min_h = self.__cells[i, j].size
                    self.__heights[i] = max(
                        min_h, self.__heights[i], s[i, j][1])

        #  set the container size of all cells
        for i, j in self.__cells:
            width = 0
            cols = self.__cell_cols((i, j))
            for k in range(cols):
                width += self.__widths[j + k]
            width += (cols - 1) * hspacing
            csize = (width, self.__heights[i])
            self.__cells[i, j].container_size = csize

        #  compute the final result
        w = 0
        j = 0
        while j < self.__cols:
            cols = self.__cell_cols((0, j))
            for k in range(cols):
                w += self.__widths[j + k]
            w += cols
            j += cols
        h = sum(self.__heights[i] for i in range(self.__rows))
        if self.__cols > 1:
            w += (self.__cols - 1) * hspacing
        if self.__rows > 1:
            h += (self.__rows - 1) * vspacing

        return w, h

    def _position(self, pos):
        hspacing = self.get_style('hspacing')
        vspacing = self.get_style('vspacing')
        h = 0
        i = 0
        while i < self.__rows:
            w = 0
            j = 0
            while j < self.__cols:
                if (i, j) in self.__cells:
                    cell = self.__cells[i, j]
                    cell.position((pos[0] + w, pos[1] + h))
                    w += cell.container_size[0]
                else:
                    w += self.__widths[j]
                w += hspacing
                j += self.__cell_cols((i, j))
            h += self.__heights[i] + vspacing
            i += 1

    def __cell_cols(self, ij):
        if self.__colspan is not None and ij in self.__colspan:
            return self.__colspan[ij]
        return 1

    def __cell_rows(self, ij):
        if self.__rowspan is not None and ij in self.__rowspan:
            return self.__rowspan[ij]
        return 1

    def __compute_column_widths(self, sizes):
        hspacing = self.get_style('hspacing')
        notdone = dict()
        for j in range(self.__cols):
            wmax = 0

            #  traverse cells of this column that spans a single
            #  column
            for i in range(self.__rows):
                if (i, j) in self.__cells:
                    cell = self.__cells[i, j]
                    if self.__cell_cols((i, j)) == 1:
                        wmax = max(wmax, cell.size[0])

            #  check closed cells
            for i in notdone:
                cij, cw, ccols = notdone[i]
                if ccols == 1:
                    wmax = max(cw, wmax)

            #  update opened cells
            for i in notdone:
                cij, cw, ccols = notdone[i]
                notdone[i] = cij, cw - wmax - hspacing, ccols - 1

            #  remove closing cells
            notdone = {k: v for k, v in notdone.items() if v[2] > 0}

            #  open new cells
            for i in range(self.__rows):
                if (i, j) in self.__cells:
                    cell = self.__cells[i, j]
                    cols = self.__cell_cols((i, j))
                    if cols > 1:
                        notdone[i] = \
                            (i, j), sizes[i, j][0] - wmax - hspacing, cols - 1

            self.__widths[j] = wmax

    def _iter_tree(self):
        for ij in self.__cells:
            yield from self.__cells[ij].iter_tree()
