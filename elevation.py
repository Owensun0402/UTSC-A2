"""Assignment 2 functions."""

from copy import deepcopy


# Examples to use in doctests:
THREE_BY_THREE = [[1, 2, 1],
                  [4, 6, 5],
                  [7, 8, 9]]

FOUR_BY_FOUR = [[1, 2, 6, 5],
                [4, 5, 3, 2],
                [7, 9, 8, 1],
                [1, 2, 1, 4]]

UNIQUE_3X3 = [[1, 2, 3],
              [9, 8, 7],
              [4, 5, 6]]

UNIQUE_4X4 = [[10, 2, 3, 30],
              [9, 8, 7, 11],
              [4, 5, 6, 12],
              [13, 14, 15, 16]]

# Used to compare floats in doctests:
# If the difference between the expected return value and the actual return
# value is less than EPSILON, we will consider the test passed.
EPSILON = 0.005


# We provide a full docstring for this function as an example.
def compare_elevations_within_row(elevation_map: list[list[int]], map_row: int,
                                  level: int) -> list[int]:
    """Return a new list containing the three counts: the number of
    elevations from row number map_row of elevation map elevation_map
    that are less than, equal to, and greater than elevation level.

    Precondition: elevation_map is a valid elevation map.
                  0 <= map_row < len(elevation_map).

    >>> compare_elevations_within_row(THREE_BY_THREE, 1, 5)
    [1, 1, 1]
    >>> compare_elevations_within_row(FOUR_BY_FOUR, 1, 2)
    [0, 1, 3]

    """
    lst = [0, 0, 0]
    for i in elevation_map[map_row]:
        if i < level:
            lst[0] += 1
        elif i == level:
            lst[1] += 1
        else:
            lst[2] += 1
    return lst



# We provide a partial doctest in this function as an example of
# testing a function that modifies its input. Note the use of deepcopy
# to create a copy of the nested list to use in the function call. We
# do this to make sure that different doctests do not affect each
# other.
def update_elevation(elevation_map: list[list[int]], start: list[int],
                     stop: list[int], delta: int) -> None:
    """

    >>> THREE_BY_THREE_COPY = deepcopy(THREE_BY_THREE)
    >>> update_elevation(THREE_BY_THREE_COPY, [1, 0], [1, 1], -2)
    >>> THREE_BY_THREE_COPY
    [[1, 2, 1], [2, 4, 5], [7, 8, 9]]
    >>> FOUR_BY_FOUR_COPY = deepcopy(FOUR_BY_FOUR)
    >>> update_elevation(FOUR_BY_FOUR_COPY, [1, 2], [3, 2], 1)
    >>> FOUR_BY_FOUR_COPY
    [[1, 2, 6, 5], [4, 5, 4, 2], [7, 9, 9, 1], [1, 2, 2, 4]]

    """
    if start[0] == stop [0]:

        while start[1] <= stop[1]:
            if elevation_map[start[0]][start[1]] + delta <= 0:
                elevation_map[start[0]][start[1]] = 0
            else:
                elevation_map[start[0]][start[1]] = elevation_map[start[0]][start[1]] + delta
            start[1] += 1
    elif start[1] == stop[1]:

        while start[0] <= stop[0]:
            if elevation_map[start[0]][start[1]] + delta <= 0:
                elevation_map[start[0]][start[1]] = 0
            else:
                elevation_map[start[0]][start[1]] = elevation_map[start[0]][start[1]] + delta
            start[0] += 1


# We provide a partial doctest in this function as an example of
# testing a function that returns a float. Note the use of abs and
# EPSILON to check if two floats are "close enough". We do this to
# deal with inevitable errors that arise in floating point arithmetic.
def get_average_elevation(elevation_map: list[list[int]]) -> float:
    """
    >>> abs(get_average_elevation(UNIQUE_3X3) - 5.0) < EPSILON
    True
    >>> abs(get_average_elevation(FOUR_BY_FOUR) - 3.8125) < EPSILON
    True
    """
    average = 0
    count = 0
    for i in elevation_map:
        for j in i:
            average += j
            count += 1
    return average / count


def find_peak(elevation_map: list[list[int]]) -> list[int]:
    """
    >>> UNIQUE_3X3_COPY = deepcopy(UNIQUE_3X3)
    >>> find_peak(UNIQUE_3X3_COPY)
    [1, 0]
    >>> UNIQUE_4X4_COPY = deepcopy(UNIQUE_4X4)
    >>> find_peak(UNIQUE_4X4_COPY)
    [0, 3]
    """
    max_val = 0
    lst = [0, 0]
    for i in range(len(elevation_map)):
        for j in range(len(elevation_map[i])):
            if elevation_map[i][j] > max_val:
                max_val = elevation_map[i][j]
                lst[0] = i
                lst[1] = j
    return lst




def is_sink(elevation_map: list[list[int]], cell: list[int]) -> bool:
    """

    >>> THREE_BY_THREE_COPY = deepcopy(THREE_BY_THREE)
    >>> is_sink(THREE_BY_THREE_COPY, [0, 2])
    True
    >>> THREE_BY_THREE_COPY = deepcopy(THREE_BY_THREE)
    >>> is_sink(THREE_BY_THREE_COPY, [2, 0])
    False
    >>> THREE_BY_THREE_COPY = deepcopy(THREE_BY_THREE)
    >>> is_sink(THREE_BY_THREE_COPY, [55, 55])
    False
    """

    if is_valid_cell(cell, len(elevation_map)):
        lst = []
        lst.extend(get_adjacent_cells(cell, len(elevation_map)))
        for i in lst:
            if is_cell_lower(elevation_map, i, cell):
                return False
        return True
    return False



def find_local_sink(elevation_map: list[list[int]],
                    cell: list[int]) -> list[int]:
    if is_sink(elevation_map, cell):
        return cell
    else:
        min_val = 0
        lst = [0, 0]
        for i in get_adjacent_cells(cell, elevation_map):
            for j in i:
                if elevation_map[i][j] <= min_val:
                    min_val = elevation_map[i][j]
                    lst[0] = i
                    lst[1] = j
        return lst


def can_hike_to(elevation_map: list[list[int]], start: list[int],
                dest: list[int], supplies: int) -> bool:
    """
    >>> e_map = [[1, 6, 5, 6], [2, 5, 6, 8], [7, 2, 8, 1], [4, 4, 7, 3]]
    >>> can_hike_to(e_map, [3, 3], [2, 2], 10)
    True
    >>> can_hike_to(e_map, [3, 3], [2, 2], 8)
    False
    >>> can_hike_to(e_map, [3, 3], [3, 0], 7)
    True
    >>> can_hike_to(e_map, [3, 3], [3, 0], 6)
    False
    >>> can_hike_to(e_map, [3, 3], [0, 0], 18)
    True
    >>> can_hike_to(e_map, [3, 3], [0, 0], 17)
    False
    """
    if start[0] == dest[0]:
        current_cell = start[1]
        for i in range(abs(dest[1] - start[1])):
            current_cell = current_cell-1
            supplies = supplies - abs(elevation_map[start[0]][current_cell+1] - elevation_map[start[0]][current_cell])
        return supplies >= 0
    elif start[1] == dest[1]:
        current_cell = start[0]
        for i in range(abs(dest[0] - start[0])):
            current_cell = current_cell - 1
            supplies = supplies - abs(elevation_map[current_cell+1][start[1]] - elevation_map[current_cell][start[1]])
        return supplies >= 0
    else:
        current_rowcell = start[0]
        current_columncell = start[1]
        while current_columncell != dest[1] and current_rowcell != dest[0]:
            north_cell = [current_rowcell-1, current_columncell]
            west_cell = [current_rowcell, current_columncell-1]
            if is_cell_lower(elevation_map, north_cell, west_cell) or elevation_map[north_cell[0]][north_cell[1]] == elevation_map[west_cell[0]][west_cell[1]]:
                current_rowcell = current_rowcell - 1
                supplies = supplies - abs(elevation_map[current_rowcell+1][current_columncell] - elevation_map[current_rowcell][current_columncell])
            else:
                current_columncell = current_columncell - 1
                supplies = supplies - abs(
                    elevation_map[current_rowcell][current_columncell+1] - elevation_map[current_rowcell][
                        current_columncell-1])
        while current_columncell == dest[1] and current_rowcell != dest[0]:
            current_rowcell = current_rowcell - 1
            supplies = supplies - abs(elevation_map[current_rowcell + 1][current_columncell] - elevation_map[current_rowcell][current_columncell])
        while current_rowcell == dest[0] and current_columncell != dest[1]:
            current_columncell = current_columncell - 1
            supplies = supplies - abs(elevation_map[current_rowcell][current_columncell + 1] - elevation_map[current_rowcell][current_columncell])
        return supplies >= 0






def get_lower_resolution(elevation_map: list[list[int]]) -> list[list[int]]:
    """

    >>> map1 = [[1, 6, 5, 6], [2, 5, 6, 8], [7, 2, 8, 1], [4, 4, 7, 3]]
    >>> get_lower_resolution(map1)
    [[3, 6], [4, 4]]
    >>> map2 = [[7, 9, 1], [4, 2, 1], [3, 2, 3]]
    >>> get_lower_resolution(map2)
    [[5, 1], [2, 3]]
    >>> map3 = [[1, 6, 5, 6, 8], [2, 5, 6, 8, 10], [7, 2, 8, 1, 11], [4, 4, 7, 3, 30], [9, 8, 9 ,11, 42]]
    >>> get_lower_resolution(map3)
    [[3, 6, 9], [4, 4, 20], [8, 10, 42]]
    """
    if len(elevation_map)%2 == 0:
        i = 0
        j = 0
        inner_lst = []
        outer_lst = []
        while i < len(elevation_map):
            while j < len(elevation_map):
                sum = (elevation_map[i][j] + elevation_map[i+1][j] + elevation_map[i+1][j+1] + elevation_map[i][j+1])//4
                inner_lst.append(sum)
                j +=2
            outer_lst.append(inner_lst)
            inner_lst = []
            i += 2
            j = 0
        return outer_lst
    i = 0
    j = 0
    k = 0
    inner_lst = []
    outer_lst = []
    while i < len(elevation_map)-1:
        while j < len(elevation_map)-1:
            sum = (elevation_map[i][j] + elevation_map[i + 1][j] + elevation_map[i + 1][j + 1] + elevation_map[i][
                j + 1]) // 4
            inner_lst.append(sum)
            j += 2
        inner_lst.append((elevation_map[i][j] + elevation_map[i+1][j])//2)
        outer_lst.append(inner_lst)
        inner_lst = []
        i += 2
        j = 0
    while k < len(elevation_map)-1:
        inner_lst.append((elevation_map[len(elevation_map)-1][k]+elevation_map[len(elevation_map)-1][k+1])//2)
        k += 2
    inner_lst.append(elevation_map[len(elevation_map)-1][len(elevation_map)-1])
    outer_lst.append(inner_lst)
    return outer_lst



## SUGGESTED HELPER FUNCTIONS #################################################
# These functions are not required in the assignment. However, we believe it is
# a great idea to define these functions and use them as helpers in the required
# functions.
def is_valid_cell(cell: list[int], dimension: int) -> bool:
    """Return True if and only if cell is a valid cell in an elevation map
    of dimensions dimension x dimension.

    Precondition: cell is a list of length 2.

    >>> is_valid_cell([1, 1], 2)
    True
    >>> is_valid_cell([0, 2], 2)
    False

    """
    return cell[0] < dimension and cell[1] < dimension


def is_cell_lower(elevation_map: list[list[int]], cell_1: list[int],
                  cell_2: list[int]) -> bool:
    """Return True iff cell_1 has a lower elevation than cell_2.

    Precondition: elevation_map is a valid elevation map
                  cell_1 and cell_2 are valid cells in elevation_map

    >>> map = [[0, 1], [2, 3]]
    >>> is_cell_lower(map, [0, 0], [1, 1])
    True
    >>> is_cell_lower(map, [1, 1], [0, 0])
    False

    """

    return elevation_map[cell_1[0]][cell_1[1]] < elevation_map[cell_2[0]][cell_2[1]]


def get_adjacent_cells(cell: list[int], dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to cell in an elevation map with
    dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.

    >>> adjacent_cells = get_adjacent_cells([1, 1], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
    >>> adjacent_cells = get_adjacent_cells([1, 0], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [1, 1], [2, 0], [2, 1]]

    """
    lst = []
    if cell[0] == 0:
        if cell[1] == 0: # upper left
            lst.append([cell[0]+1, cell[1]])
            lst.append([cell[0] + 1, cell[1]+1])
            lst.append([cell[0], cell[1]+1])
        elif cell[1] == dimension - 1: #upper right
            lst.append([cell[0], cell[1] - 1])
            lst.append([cell[0] + 1, cell[1] - 1])
            lst.append([cell[0] + 1, cell[1]])
        else: # upper centre
            lst.append([cell[0], cell[1] - 1])
            lst.append([cell[0], cell[1] + 1])
            lst.append([cell[0] + 1, cell[1] + 1])
            lst.append([cell[0] + 1, cell[1]])
            lst.append([cell[0] + 1, cell[1] - 1])
    elif cell[0] == dimension - 1:
        if cell[1] == 0:  # lower left
            lst.append([cell[0] - 1, cell[1] - 1])
            lst.append([cell[0] - 1, cell[1]])
            lst.append([cell[0], cell[1] - 1])
        elif cell[1] == dimension -1: # lower right
            lst.append([cell[0] - 1, cell[1] - 1])
            lst.append([cell[0] - 1, cell[1]])
            lst.append([cell[0], cell[1] - 1])
        else: # bottom centre
            lst.append([cell[0] - 1, cell[1]])
            lst.append([cell[0] - 1, cell[1] - 1])
            lst.append([cell[0] - 1, cell[1] + 1])
            lst.append([cell[0], cell[1] - 1])
            lst.append([cell[0], cell[1] + 1])
    elif cell[1] == 0: # left centre
        lst.append([cell[0] - 1, cell[1]])
        lst.append([cell[0] - 1, cell[1] + 1])
        lst.append([cell[0], cell[1] + 1])
        lst.append([cell[0] + 1, cell[1] + 1])
        lst.append([cell[0] + 1, cell[1]])

    elif cell[1] == dimension -1:#right centre
        lst.append([cell[0] - 1, cell[1]])
        lst.append([cell[0] - 1, cell[1] - 1])
        lst.append([cell[0], cell[1] - 1])
        lst.append([cell[0] + 1, cell[1]])
        lst.append([cell[0] + 1, cell[1] - 1])
    else:
        lst.append([cell[0] - 1, cell[1]])
        lst.append([cell[0] - 1, cell[1] - 1])
        lst.append([cell[0] - 1, cell[1] + 1])
        lst.append([cell[0], cell[1] - 1])
        lst.append([cell[0], cell[1] + 1])
        lst.append([cell[0] + 1, cell[1] + 1])
        lst.append([cell[0] + 1, cell[1]])
        lst.append([cell[0] + 1, cell[1] - 1])

    return lst


if __name__ == '__main__':
    import doctest
    doctest.testmod()
