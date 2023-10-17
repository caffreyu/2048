from typing import Dict, Union, List
from random import random, choice
import os

BOARD_TYPE = Dict[int, Union[str, int]]
LIST_TYPE = List[List[Union[int, str]]]
TOTAL = 100
PROB = 0.2
SIZE = 4

# fmt: off
UP = {0: [], 1: [], 2: [], 3: [], 4: [0], 5: [1], 6: [2], 7: [3], 8: [4], 9: [5], 10: [6], 11: [7], 12: [8], 13: [9], 14: [10], 15: [11],}
DOWN = {0: [4], 1: [5], 2: [6], 3: [7], 4: [8], 5: [9], 6: [10], 7: [11], 8: [12], 9: [13], 10: [14], 11: [15], 12: [], 13: [], 14: [], 15: [],}
RIGHT = {0: [1], 1: [2], 2: [3], 3: [], 4: [5], 5: [6], 6: [7], 7: [], 8: [9], 9: [10], 10: [11], 11: [], 12: [13], 13: [14], 14: [15], 15: [],}
LEFT = {0: [], 1: [0], 2: [1], 3: [2], 4: [], 5: [4], 6: [5], 7: [6], 8: [], 9: [8], 10: [9], 11: [10], 12: [], 13: [12], 14: [13], 15: [14],}
TABLE = {"w": UP, "s": DOWN, "a": LEFT, "d": RIGHT,}

COLUMNS = [[0, 4, 8, 12,], [1, 5, 9, 13,], [2, 6, 10, 14,], [3, 7, 11, 15,]]
ROWS = [[0, 1, 2, 3,], [4, 5, 6, 7,], [8, 9, 10, 11,], [12, 13, 14, 15,]]

# fmt: on


def check_win(board: BOARD_TYPE) -> bool:
    return 2048 in board.values()


def check_fail(
    board: BOARD_TYPE,
    occupied: List[int],
) -> bool:
    result = True
    directions = list(TABLE.keys())
    print(directions)

    for direction in directions:
        judge = check_movable(board=board, user_input=direction, occupied=occupied)
        if judge:
            result = False
            break

    return result


def check_movable(
    board: BOARD_TYPE,
    user_input: str,
    occupied: List[int],
) -> bool:
    result = False
    reference = TABLE[user_input]

    for ele in occupied:
        if result:
            break
        candidates = reference[ele]
        if len(candidates) == 0:
            continue
        for candidate in candidates:
            if result:
                break
            if isinstance(board[candidate], str):
                result = True
            else:
                result = board[candidate] == board[ele]

    return result


def generate_lists(board: BOARD_TYPE) -> List[List[int]]:
    vacants, occupied = [], []
    for k, v in board.items():
        if isinstance(v, str):
            vacants.append(k)
        else:
            occupied.append(k)
    return vacants, occupied


def add_blanks(s: str, cell_length=5) -> str:
    return s + " " * (cell_length - len(s))


def display(board: BOARD_TYPE) -> None:
    os.system("clear")
    for i in range(4):
        for j in range(4 * i, 4 * i + 4):
            print(add_blanks(str(board[j])), end="")
        print("\n\n")


def generate(board: BOARD_TYPE, vacants: List[int]) -> None:
    rand_num = random() * (TOTAL - 1)
    gen_num = 4 if rand_num < PROB * TOTAL else 2
    rand_pos = choice(vacants)
    board[rand_pos] = gen_num


def get_columns(board: BOARD_TYPE) -> LIST_TYPE:
    results = []
    for i in range(4):
        curr = []
        for j in range(4):
            curr.append(board[i + 4 * j])
        results.append(curr)
    return results


def get_rows(board: BOARD_TYPE) -> LIST_TYPE:
    results = []
    for i in range(4):
        curr = []
        for j in range(4):
            curr.append(board[4 * i + j])
        results.append(curr)
    return results


def set_columns(board: BOARD_TYPE, board_list: LIST_TYPE) -> None:
    for i in range(4):
        for j in range(4):
            board[COLUMNS[i][j]] = board_list[i][j]


def set_rows(board: BOARD_TYPE, board_list: LIST_TYPE) -> None:
    for i in range(4):
        for j in range(4):
            board[ROWS[i][j]] = board_list[i][j]


def move_up(board: BOARD_TYPE) -> None:
    board_list = get_columns(board=board)
    updated_lists = []
    for i in range(len(board_list)):
        curr = [ele for ele in board_list[i] if isinstance(ele, int)]
        updated_list = []
        judge = True
        if len(curr) == 0:
            updated_list.extend(["x"] * SIZE)
        elif len(curr) == 1:
            updated_list = curr
        else:
            updated_list = [curr[0]]
            for i in range(1, len(curr)):
                if not judge:
                    updated_list.append(curr[i])
                    judge = True
                elif curr[i] == curr[i - 1] and judge:
                    updated_list[-1] += curr[i]
                    judge = False
                else:
                    updated_list.append(curr[i])
        updated_list.extend(["x"] * (SIZE - len(updated_list)))
        updated_lists.append(updated_list)
    set_columns(board=board, board_list=updated_lists)


def move_down(board: BOARD_TYPE) -> None:
    board_list = get_columns(board=board)
    updated_lists = []
    for i in range(len(board_list)):
        curr = [ele for ele in board_list[i][::-1] if isinstance(ele, int)]
        updated_list = []
        judge = True
        if len(curr) == 0:
            updated_list.extend(["x"] * SIZE)
        elif len(curr) == 1:
            updated_list = curr
        else:
            updated_list = [curr[0]]
            for i in range(1, len(curr)):
                if not judge:
                    updated_list.append(curr[i])
                    judge = True
                elif curr[i] == curr[i - 1] and judge:
                    updated_list[-1] += curr[i]
                    judge = False
                else:
                    updated_list.append(curr[i])
        updated_list.extend(["x"] * (SIZE - len(updated_list)))
        updated_lists.append(updated_list[::-1])
    set_columns(board=board, board_list=updated_lists)


def move_left(board: BOARD_TYPE) -> None:
    board_list = get_rows(board=board)
    updated_lists = []
    for i in range(len(board_list)):
        curr = [ele for ele in board_list[i] if isinstance(ele, int)]
        updated_list = []
        judge = True
        if len(curr) == 0:
            updated_list.extend(["x"] * SIZE)
        elif len(curr) == 1:
            updated_list = curr
        else:
            updated_list = [curr[0]]
            for i in range(1, len(curr)):
                if not judge:
                    updated_list.append(curr[i])
                    judge = True
                elif curr[i] == curr[i - 1] and judge:
                    updated_list[-1] += curr[i]
                    judge = False
                else:
                    updated_list.append(curr[i])
        updated_list.extend(["x"] * (SIZE - len(updated_list)))
        updated_lists.append(updated_list)
    set_rows(board=board, board_list=updated_lists)


def move_right(board: BOARD_TYPE) -> None:
    board_list = get_rows(board=board)
    updated_lists = []
    for i in range(len(board_list)):
        curr = [ele for ele in board_list[i][::-1] if isinstance(ele, int)]
        updated_list = []
        judge = True
        if len(curr) == 0:
            updated_list.extend(["x"] * SIZE)
        elif len(curr) == 1:
            updated_list = curr
        else:
            updated_list = [curr[0]]
            for i in range(1, len(curr)):
                if not judge:
                    updated_list.append(curr[i])
                    judge = True
                elif curr[i] == curr[i - 1] and judge:
                    updated_list[-1] += curr[i]
                    judge = False
                else:
                    updated_list.append(curr[i])
        updated_list.extend(["x"] * (SIZE - len(updated_list)))
        updated_lists.append(updated_list[::-1])
    set_rows(board=board, board_list=updated_lists)


def move(board: BOARD_TYPE, user_input: str) -> None:
    if user_input == "w":
        move_up(board=board)
    elif user_input == "a":
        move_left(board=board)
    elif user_input == "s":
        move_down(board=board)
    elif user_input == "d":
        move_right(board=board)
    else:
        raise ValueError("[ERROR] User input is not valid.")


def clear():
    os.system("clear")
