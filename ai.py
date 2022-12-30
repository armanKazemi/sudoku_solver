import json
import math


# *** you can change everything except the name of the class, the act function and the problem_data ***


class AI:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        pass

    # the solve function takes a json string as input
    # and outputs the solved version as json
    def solve(self, problem):
        # ^^^ DO NOT change the solve function above ***

        problem_data = json.loads(problem)
        # ^^^ DO NOT change the problem_data above ***

        # TODO implement your code here
        if not self.is_valid(problem_data["sudoku"]):
            return False

        result, possible_sudoku_result = self.brute_force(problem_data["sudoku"])
        if self.is_solved(result):
            return result

        result = self.backtracking(result, possible_sudoku_result)
        if result:
            # finished is the solved version
            return result

        return False

    def validate_existence_elements(self, sudoku, i, j):
        element = sudoku[i][j]
        # check horizontal and vertical issues
        for p in range(9):
            if p != i and element == sudoku[p][j]:
                return False
            if p != j and element == sudoku[i][p]:
                return False
        # check box issues
        i_box, j_box = self.get_box_start_coordinate(i, j)
        issued_elements_of_box = [(i, j) for p in range(i_box, i_box + 3) for q in range(j_box, j_box + 3)
                                  if (p, q) != (i, j) and element == sudoku[p][q]]
        if len(issued_elements_of_box):
            return False
        return True

    def is_solved(self, sudoku):
        for i, row in enumerate(sudoku):
            for j, col_element in enumerate(row):
                if col_element == 0:
                    return False
                if not self.validate_existence_elements(sudoku, i, j):
                    return False
        # sudoku is solved
        return True

    def is_valid(self, sudoku):
        for i, row in enumerate(sudoku):
            for j, col_element in enumerate(row):
                if col_element != 0:
                    if not self.validate_existence_elements(sudoku, i, j):
                        return False
        # sudoku is valid
        return True

    def get_box_start_coordinate(self, x, y):
        return 3 * int(math.floor(x / 3)), 3 * int(math.floor(y / 3))

    def get_used_elements(self, sudoku, x, y):
        i_box, j_box = self.get_box_start_coordinate(x, y)
        existing = [sudoku[i][j] for i in range(i_box, i_box + 3) for j in range(j_box, j_box + 3) if sudoku[i][j] > 0]
        existing += [sudoku[x][i] for i in range(9) if sudoku[x][i] > 0]
        existing += [sudoku[i][y] for i in range(9) if sudoku[i][y] > 0]
        return existing

    def simplify_double_pairs_horizontal(self, i, j, sudoku, possible_sudoku):
        temp_pair = possible_sudoku[i][j]
        for p in (p for p in range(j + 1, 9) if
                  len(possible_sudoku[i][p]) == 2 and len(set(possible_sudoku[i][p]) & set(temp_pair)) == 2):
            for q in (q for q in range(9) if q != j and q != p):
                possible_sudoku[i][q] = list(set(possible_sudoku[i][q]) - set(temp_pair))
                if len(possible_sudoku[i][q]) == 1:
                    sudoku[i][q] = possible_sudoku[i][q].pop()
                    return [sudoku, possible_sudoku]
        return []

    def simplify_double_pairs_vertical(self, i, j, sudoku, possible_sudoku):
        temp_pair = possible_sudoku[i][j]
        for p in (p for p in range(i + 1, 9) if
                  len(possible_sudoku[p][j]) == 2 and len(set(possible_sudoku[p][j]) & set(temp_pair)) == 2):
            for q in (q for q in range(9) if q != i and p != q):
                possible_sudoku[q][j] = list(set(possible_sudoku[q][j]) - set(temp_pair))
                if len(possible_sudoku[q][j]) == 1:
                    sudoku[q][j] = possible_sudoku[q][j].pop()
                    return [sudoku, possible_sudoku]
        return []

    def simplify_double_pairs_box(self, i, j, sudoku, possible_sudoku):
        temp_pair = possible_sudoku[i][j]
        i_box, j_box = self.get_box_start_coordinate(i, j)
        for (a, b) in [(a, b) for a in range(i_box, i_box + 3) for b in range(j_box, j_box + 3)
                       if (a, b) != (i, j) and len(possible_sudoku[a][b]) == 2 and len(
                set(possible_sudoku[a][b]) & set(temp_pair)) == 2]:
            for (c, d) in [(c, d) for c in range(i_box, i_box + 3) for d in range(j_box, j_box + 3)
                           if (c, d) != (a, b) and (c, d) != (i, j)]:
                possible_sudoku[c][d] = list(set(possible_sudoku[c][d]) - set(temp_pair))
                if len(possible_sudoku[c][d]) == 1:
                    sudoku[c][d] = possible_sudoku[c][d].pop()
                    return [sudoku, possible_sudoku]
        return []

    def simplify_double_pairs(self, sudoku, possible_sudoku):
        for (i, j) in [(i, j) for i in range(9) for j in range(9) if len(possible_sudoku[i][j]) == 2]:
            result = self.simplify_double_pairs_horizontal(i, j, sudoku, possible_sudoku)
            if len(result) > 0:
                return result
            result = self.simplify_double_pairs_vertical(i, j, sudoku, possible_sudoku)
            if len(result) > 0:
                return result
            result = self.simplify_double_pairs_box(i, j, sudoku, possible_sudoku)
            if len(result) > 0:
                return result
        return []

    def update_unique_horizontal(self, x, y, sudoku, possible_sudoku):
        element = possible_sudoku[x][y]
        for i in (i for i in range(9) if i != y):
            element = list(set(element) - set(possible_sudoku[x][i]))
        if len(element) == 1:
            sudoku[x][y] = element.pop()
            return [sudoku, possible_sudoku]
        return []

    def update_unique_vertical(self, x, y, sudoku, possible_sudoku):
        element = possible_sudoku[x][y]
        for i in (i for i in range(9) if i != x):
            element = list(set(element) - set(possible_sudoku[i][y]))
        if len(element) == 1:
            sudoku[x][y] = element.pop()
            return [sudoku, possible_sudoku]
        return []

    def update_unique_box(self, x, y, sudoku, possible_sudoku):
        element = possible_sudoku[x][y]
        i_box, j_box = self.get_box_start_coordinate(x, y)
        for (i, j) in [(i, j) for i in range(i_box, i_box + 3) for j in range(j_box, j_box + 3) if (i, j) != (x, y)]:
            element = list(set(element) - set(possible_sudoku[i][j]))
        if len(element) == 1:
            sudoku[x][y] = element.pop()
            return [sudoku, possible_sudoku]
        return []

    def find_and_place_possibles(self, sudoku):
        possible_sudoku = [[[] for col in row] for row in sudoku]
        empty_elements = [(i, j) for i in range(9) for j in range(9) if sudoku[i][j] == 0]
        for (i, j) in empty_elements:
            possible_amounts = list(set(range(1, 10)) - set(self.get_used_elements(sudoku, i, j)))
            # there is just one possible amount so we fill it
            if len(possible_amounts) == 1:
                sudoku[i][j] = possible_amounts.pop()
            else:
                # fill sudoku element with all possible amounts
                possible_sudoku[i][j] = possible_amounts
        return possible_sudoku

    def find_and_remove_uniques(self, sudoku, possible_sudoku):
        for (i, j) in [(i, j) for i in range(9) for j in range(9) if sudoku[i][j] == 0]:
            result = self.update_unique_horizontal(i, j, sudoku, possible_sudoku)
            if len(result) > 0:
                return result
            result = self.update_unique_vertical(i, j, sudoku, possible_sudoku)
            if len(result) > 0:
                return result
            result = self.update_unique_box(i, j, sudoku, possible_sudoku)
            if len(result) > 0:
                return result
        return []

    def brute_force(self, sudoku):
        while True:
            possible_sudoku = self.find_and_place_possibles(sudoku)
            result = self.simplify_double_pairs(sudoku, possible_sudoku)
            if len(result) > 0:
                continue
            result = self.find_and_remove_uniques(sudoku, possible_sudoku)
            if len(result) > 0:
                continue
            return sudoku, possible_sudoku

    def get_first_unsolved_element(self, possible_sudoku):
        for i, row in enumerate(possible_sudoku):
            for j, col_element in enumerate(row):
                if len(col_element) > 0:
                    return i, j

    def deep_copy(self, sudoku):
        return [i[:] for i in sudoku]

    def backtracking(self, sudoku, possible_sudoku):
        try:
            u_i, u_j = self.get_first_unsolved_element(possible_sudoku)
            u_element_cases = possible_sudoku[u_i][u_j]
        except:
            return False

        for case in u_element_cases:
            child_sudoku = self.deep_copy(sudoku)
            child_sudoku[u_i][u_j] = case
            child_sudoku, new_possible_sudoku = self.brute_force(child_sudoku)
            if self.is_solved(child_sudoku):
                return child_sudoku
            else:
                child_sudoku = self.backtracking(child_sudoku, new_possible_sudoku)
                if child_sudoku:
                    return child_sudoku
        return False
