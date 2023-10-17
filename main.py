# from collections import defaultdict
from typing import List, Dict, Union
import getch

from utils import *

victory = False
directions = [
    "w",
    "a",
    "s",
    "d",
]

board: Dict[str, Union[str, int]] = {}  # = defaultdict(lambda: "x")
for i in range(16):
    board[i] = "x"
vacants, occupied = generate_lists(board=board)
generate(board=board, vacants=vacants)
assert len(board) == 16, "[ERROR] Board was initialized in"

vacants, occupied = generate_lists(board=board)
display(board=board)

# for i in range(4):
#    if not check_fail(board=board, occupied=occupied):
#        generate(board=board, vacants=vacants)
#        vacants, occupied = generate_lists(board=board)
#        display(board=board)

# display(board=board)

while not check_fail(board=board, occupied=occupied):
    user_input = getch.getch()
    while user_input not in directions:
        user_input = getch.getch(f"[ERROR] Input needs to be in {directions}\n")
    print(user_input)
    if check_movable(board=board, user_input=user_input, occupied=occupied):
        move(board=board, user_input=user_input)
        vacants, occupied = generate_lists(board=board)
        generate(board=board, vacants=vacants)
        if check_win(board=board):
            victory = True
            break
        display(board=board)
        vacants, occupied = generate_lists(board=board)
    else:
        display(board=board)

# if __name__ == "__main__":
