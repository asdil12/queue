import os
from termcolor import colored

def print_row(col_lens, row, separator='|', space=' ', outer_space=True, limit_cols=None, separator_on_extra_rows=True, colors=None):
    """
        col_lens: list containing max size for each column
        row: list containing cells
        separator: separator between columns
        space: space character to fillup empty space in each column
        outer_space: add a space (see above) char at start & end of row
        limit_cols: id or list of ids of column(s) to shrink to fit the table into the terminal
        separator_on_extra_rows: continue column separators on multiline rows (will make copying text harder but looks better)
        colors: list of same length as row containing color names for the columns (each entry can be None for default color)
    """

    limit_col_max_len = max(col_lens) # this value is never used but python complains otherwise
    limit_col = None
    col_lens = col_lens.copy()
    if limit_cols != None:
        # try to limit each column mentioned in limit_cols
        try:
            termwidth = os.get_terminal_size().columns
        except:
            termwidth = None
        if isinstance(limit_cols, int):
            limit_cols = [limit_cols]
        else:
            limit_cols = list(limit_cols)
        for i, col in enumerate(limit_cols):
            if termwidth:
                # without this min() the table uses the full term width if limit_col is set
                line_length = sum(col_lens) + 3*(len(col_lens)-1) + (2 if outer_space else 0)
                extra_line_space = min(termwidth - line_length, 0)
                limit_col_max_len = col_lens[col] + extra_line_space
            else:
                limit_col_max_len = col_lens[col]
            if limit_col_max_len > 1:
                limit_col = col
                break
            else:
                # we would only have enough space to display … so let's drop the column completely
                # and try to limit the next one in the list
                row.pop(col)
                col_lens.pop(col)
                if colors:
                    colors.pop(col)
                # recalculate col ids in limit_cols
                for j in range(i, len(limit_cols)):
                    if limit_cols[j] > col:
                        limit_cols[j] -= 1

    extra_rows = [row]
    for in_extra_row, row in enumerate(extra_rows):
        row_normalized = []
        for i, col in enumerate(row):
            # expand multiline cells to multiple rows
            if isinstance(col, list):
                for c in col[1:]:
                    extra_row = [''] * len(row)
                    extra_row[i] = c
                    #print(extra_row)
                    extra_rows.append(extra_row)
                    #print(extra_rows)
                col = col[0]
            if limit_col == i:
                if len(col) > limit_col_max_len:
                    if limit_col_max_len == 2:
                        col = col[:limit_col_max_len-1] + '…'
                    else:
                        # remove chars in the middle to hopefully preserve important stuff
                        col = col[:limit_col_max_len-1] + '…'
                # fill up with spaces to ensure that columns of each row stay below each other
                row_normalized.append(col.ljust(limit_col_max_len, space))
            else:
                # fill up with spaces to ensure that columns of each row stay below each other
                row_normalized.append(col.ljust(col_lens[i], space))
        if colors:
            for i, color in enumerate(colors):
                if color:
                    row_normalized[i] = colored(row_normalized[i], color)
        if in_extra_row and not separator_on_extra_rows:
            line = (space * 3).join(row_normalized)
        else:
            line = (space + separator + space).join(row_normalized)
        if outer_space:
            line = space + line + space
        print(line)

def get_col_len(col):
    """
        Returns len of col if col is str - else max col len
    """
    if isinstance(col, list):
        return max(map(len, col))
    else:
        return len(col)

def print_table(headers, rows, separator='|', outer_space=True, limit_col=None, separator_on_extra_rows=True, colors=None):
    """
        headers: list of headers
        rows: list of rows each being a list of fields
        separator: vertical separator between table fields
        outer_space: add a space as padding to the left and right side of each row
        limit_col: number of column to limit in width to still fit the table on screen
        separator_on_extra_rows: support multiline fields (field being a list instead of a string)
        colors: two dimensional array containing table colors
    """
    # generate list containing max size for each column
    col_lens = [get_col_len(hc) for hc in headers or rows[0]]
    for row in rows:
        for i, col_len in enumerate(col_lens):
            col_lens[i] = max(col_len, get_col_len(row[i]))
    if headers:
        print_row(col_lens, headers, separator, outer_space=outer_space, limit_cols=limit_col)
        print_row(col_lens, ['']*len(col_lens), '+', '-', outer_space, limit_cols=limit_col)
    for i, row in enumerate(rows):
        row_colors = colors[i] if colors else None
        print_row(col_lens, row, separator, outer_space=outer_space, limit_cols=limit_col, separator_on_extra_rows=separator_on_extra_rows, colors=row_colors)
