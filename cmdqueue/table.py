import os

def print_row(col_lens, row, separator='|', space=' ', outer_space=True, limit_col=None, separator_on_extra_rows=True):
    line_length = sum(col_lens) + 3*(len(col_lens)-1) + (2 if outer_space else 0)
    if limit_col != None:
        try:
            termwidth = os.get_terminal_size().columns
            # without this min() the table uses the full term width if limit_col is set
            extra_line_space = min(termwidth - line_length, 0)
            limit_col_max_len = col_lens[limit_col] + extra_line_space
        except:
            limit_col_max_len = col_lens[limit_col]
        limit_col_max_len = max(limit_col_max_len, 1)
    else:
        limit_col_max_len = max(col_lens)
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
            if limit_col == i and len(col) > limit_col_max_len:
                col = col[:limit_col_max_len-1] + '…'
            if limit_col == i:
                row_normalized.append(col.ljust(limit_col_max_len, space))
            else:
                row_normalized.append(col.ljust(col_lens[i], space))
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

def print_table(headers, rows, separator='|', outer_space=True, limit_col=None, separator_on_extra_rows=True):
    """
        headers: list of headers
        rows: list of rows each being a list of fields
        separator: vertical separator between table fields
        outer_space: add a space as padding to the left and right side of each row
        limit_col: number of column to limit in width to still fit the table on screen
        separator_on_extra_rows: support multiline fields (field being a list instead of a string)
    """
    col_lens = [get_col_len(hc) for hc in headers or rows[0]]
    for row in rows:
        for i, col_len in enumerate(col_lens):
            col_lens[i] = max(col_len, get_col_len(row[i]))
    if headers:
        print_row(col_lens, headers, separator, outer_space=outer_space, limit_col=limit_col)
        print_row(col_lens, ['']*len(col_lens), '+', '-', outer_space, limit_col=limit_col)
    for row in rows:
        print_row(col_lens, row, separator, outer_space=outer_space, limit_col=limit_col, separator_on_extra_rows=separator_on_extra_rows)
