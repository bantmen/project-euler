# https://projecteuler.net/problem=96
#
# Solving 50 Sudoku.
# Do brute force search over the possible values for each empty cell
# given the constraints.
#

import time
from collections import defaultdict

start = time.time()


def get_row(ls, i):
    return ls[i]


def get_col(ls, i):
    for l in ls:
        yield l[i]


def coord_to_box_origin(row, col):
    # The grid is partitioned as 3x3 boxes.
    return row // 3 * 3, col // 3 * 3


def get_box_of_coord(ls, row, col):
    row, col = coord_to_box_origin(row, col)
    for i in range(row, row + 3):
        for j in range(col, col + 3):
            yield ls[i][j]


moves = set(range(1, 9 + 1))


def possible_for_coord(ls, row_idx, col_idx):
    row = set((num for num in get_row(ls, row_idx) if num != 0))
    col = set((num for num in get_col(ls, col_idx) if num != 0))
    box = set((num for num in get_box_of_coord(ls, row_idx, col_idx) if num != 0))
    ret = moves - row - col - box
    assert len(ret) > 0, "Coord: %s %s" % (row_idx, col_idx)
    return ret


def in_same_row_or_col_or_box(row_idx1, col_idx1, row_idx2, col_idx2):
    if row_idx1 == row_idx2:
        return True
    if col_idx1 == col_idx2:
        return True
    return coord_to_box_origin(row_idx1, col_idx1) == coord_to_box_origin(
        row_idx2, col_idx2
    )


def get_possible_for_empty(ls):
    possible_solutions = dict()
    for row in range(len(ls)):
        for col in range(len(ls[0])):
            num = ls[row][col]
            if num == 0:
                possible_solutions[(row, col)] = possible_for_coord(ls, row, col)
    return possible_solutions


def is_within_constraint(coord, num, solution, constraints):
    for coord2 in constraints[coord]:
        if coord2 in solution and num == solution[coord2]:
            return False
    return True


def generate_constraints(possible):
    cannot_equal = defaultdict(list)
    coords = list(possible.keys())
    for i, coord1 in enumerate(coords):
        for j in range(i + 1, len(coords)):
            coord2 = coords[j]
            num1, num2 = possible[coord1], possible[coord2]
            if in_same_row_or_col_or_box(*coord1, *coord2):
                cannot_equal[coord1].append(coord2)
                cannot_equal[coord2].append(coord1)
    return cannot_equal


def dfs(possible, solution, constraints):
    for coord in possible:
        if coord not in solution:
            found = False
            for num in possible[coord]:
                solution[coord] = num
                if is_within_constraint(coord, num, solution, constraints):
                    found = dfs(possible, solution, constraints)
                    if found:
                        break
            if not found:
                del solution[coord]
                return False
    return True


def top_left_corner(ls, solution):
    ret = 0
    for i, coord in enumerate([(0, 2), (0, 1), (0, 0)]):
        num = solution[coord] if coord in solution else ls[coord[0]][coord[1]]
        ret += num * 10 ** i
    return ret


def solve(ls):
    possible_solutions = get_possible_for_empty(ls)
    constraints = generate_constraints(possible_solutions)
    solution = dict()
    assert dfs(possible_solutions, solution, constraints)
    return top_left_corner(ls, solution)


ans = 0

with open("p096_sudoku.txt") as f:
    ls = []
    for i, line in enumerate(f.readlines()):
        if i % 10 == 0:
            # Skip the "Grid xx"
            continue
        row = line.rstrip()
        ls.append(list(map(int, row)))
        if len(ls) == 9:
            ans += solve(ls)
            ls = []

print("Answer:", ans)  # 24702
print("Took:", round((time.time() - start) * 1000, 3), "ms")  # 4.3-4.4s
