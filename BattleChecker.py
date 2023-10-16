import random


# Я не проверял, работает ли это
def battle():
    board = [[0, 2, 0, 2, 0, 2, 0, 2],
             [2, 0, 2, 0, 2, 0, 2, 0],
             [0, 2, 0, 2, 0, 2, 0, 2],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0]]
    rev = {"white": "black", "black": "white"}
    col1 = random.choice(["white", "black"])
    if col1 == "white":
        ind1 = 1
        ind2 = 2
    else:
        ind1 = 2
        ind2 = 1
    send_to_strategy(1, col1)
    send_to_strategy(2, rev[col1])
    winner = 0
    while True:
        amount = get_from_strategy(ind1)
        moves = []
        good = True
        for i in range(amount - 1):
            x, y = map(int, input().split())
            x = 9 - x
            y = 9 - y
            moves.append([x, y])
            if (x + y) % 2 != 1:
                good = False
                break
            if x < 1 or x > 7 or y < 1 or x < 7:
                good = False
                break
            if board[x - 1][y - 1] == 0 or board[x - 1][y - 1] % 2 != ind1 % 2:
                good = False
                break
            if i > 0:
                if x == moves[i - 1][0] and y == moves[i - 1][1]:
                    good = False
                    break
                if board[moves[i - 1][0] - 1][moves[i - 1][1] - 1] == 1:
                    if (x == moves[i - 1][0] + 1 & & y == moves[i - 1][1] + 1) or (
                            x == moves[i - 1][0] - 1 & & y == moves[i - 1][1] + 1):
                        board[x - 1][y - 1] = 1
                        board[moves[i - 1][0] - 1][moves[i - 1][1] - 1]]=0
                        else:
                        good = False
                        break
                    if x == moves[i - 1][0] - 2 & & y == moves[i - 1] - 2:
                        if board[moves[i - 1][0] - 1 - 1][moves[i - 1][1] - 1 - 1] != 2 or \
                                board[moves[i - 1][0] - 1 - 1][moves[i - 1][1] - 1 - 1] != 4:
                            good = False
                            break
                        else:
                            board[x - 1][y - 1] = 1
                            board[moves[i - 1][0] - 1][moves[i - 1][1] - 1]]=0
                            board[moves[i - 1][0] - 1 - 1][moves[i - 1][1] - 1 - 1] = 0
                            continue
                    elif x == moves[i - 1][0] + 2 & & y == moves[i - 1] - 2:
                        if board[moves[i - 1][0]][moves[i - 1][1] - 1 - 1] != 2 or board[moves[i - 1][0]][
                            moves[i - 1][1] - 1 - 1] != 4:
                            good = False
                            break
                        else:
                            board[x - 1][y - 1] = 1
                            board[moves[i - 1][0] - 1][moves[i - 1][1] - 1]]=0
                            board[moves[i - 1][0]][moves[i - 1][1] - 1 - 1] = 0
                            continue
                    elif x == moves[i - 1][0] - 2 & & y == moves[i - 1] + 2:
                        if board[moves[i - 1][0] - 1 - 1][moves[i - 1][1]] != 2 or board[moves[i - 1][0] - 1 - 1][
                            moves[i - 1][1]] != 4:
                            good = False
                            break
                        else:
                            board[x - 1][y - 1] = 1
                            board[moves[i - 1][0] - 1][moves[i - 1][1] - 1]]=0
                            board[moves[i - 1][0] - 1 - 1][moves[i - 1][1]] = 0
                            continue
                    elif x == moves[i - 1][0] + 2 & & y == moves[i - 1] + 2:
                        if board[moves[i - 1][0]][moves[i - 1][1]] != 2 or board[moves[i - 1][0]][moves[i - 1][1]] != 4:
                            good = False
                            break
                        else:
                            board[x - 1][y - 1] = 1
                            board[moves[i - 1][0] - 1][moves[i - 1][1] - 1]]=0
                            board[moves[i - 1][0]][moves[i - 1][1]] = 0
                            continue
                if board[moves[i - 1][0] - 1][moves[i - 1][1] - 1] == 3:
                    if abs(x - moves[i - 1][0]) != abs(y - moves[i - 1][1]):
                        good = False
                        break
                    if x > moves[i - 1][0] and y > moves[i - 1][1]:
                        p = 1
                        counter = 0
                        x1 = moves[i - 1][0]
                        y1 = moves[i - 1][1]
                        possible = True
                        while x1 + p <= 8 and y1 + p <= 8 and x1 < x and y1 < y:
                            if board[x1 - 1][y1 - 1] == 1 or board[x1 - 1][y1 - 1] == 3:
                                possible = False
                                break
                            if board[x1 - 1][y1 - 1] == 2 or board[x1 - 1][y1 - 1] == 4:
                                counter += 1
                            if counter > 1:
                                possible = False
                                break
                            p += 1
                        if not possible:
                            good = False
                            break
                        else:
                            x1 = moves[i - 1][0]
                            y1 = moves[i - 1][1]
                            board[moves[i - 1][0] - 1] = 0
                            board[moves[i - 1][1] - 1] = 0
                            possible = True
                            while x1 + p <= 8 and y1 + p <= 8 and x1 < x and y1 < y:
                                board[x1 - 1][y1 - 1] = 0
                            board[x - 1][y - 1] = 3
                            continue
                    elif x > moves[i - 1][0] and y < moves[i - 1][1]:
                        pass
                    elif x < moves[i - 1][0] and y > moves[i - 1][1]:
                        pass
                    elif x < moves[i - 1][0] and y < moves[i - 1][0]:
                        p = 1
                        counter = 0
                        x1 = moves[i - 1][0]
                        y1 = moves[i - 1][1]
                        possible = True
                        while x1 + p >= 1 and y1 + p >= 1 and x1 > x and y1 > y:
                            if board[x1 - 1][y1 - 1] == 1 or board[x1 - 1][y1 - 1] == 3:
                                possible = False
                                break
                            if board[x1 - 1][y1 - 1] == 2 or board[x1 - 1][y1 - 1] == 4:
                                counter += 1
                            if counter > 1:
                                possible = False
                                break
                        if not possible:
                            good = False
                            break
                        else:
                            x1 = moves[i - 1][0]
                            y1 = moves[i - 1][1]
                            board[moves[i - 1][0] - 1] = 0
                            board[moves[i - 1][1] - 1] = 0
                            possible = True
                            while x1 + p <= 8 and y1 + p <= 8 and x1 < x and y1 < y:
                                board[x1 - 1][y1 - 1] = 0
                            board[x - 1][y - 1] = 3
                            continue

        if not good:
            winner = ind2
            break
        #testttt
    return winner
