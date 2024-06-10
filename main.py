import random


def initiation():
    while True:
        stock = []

        for i in range(0, 7):
            for j in range(0, 7):
                if i <= j:
                    stock.append([i, j])

        random.shuffle(stock)
        computer = [stock.pop(i) for i in range(7)]
        player = [stock.pop(i) for i in range(7)]

        snake_comp = list(filter(lambda x: x[0] == x[1], computer))
        if snake_comp:
            snake_comp = max(snake_comp, key=lambda x: x[0])

        snake_player = list(filter(lambda x: x[0] == x[1], player))
        if snake_player:
            snake_player = max(snake_player, key=lambda x: x[0])

        if not snake_comp and not snake_player:
            continue
        elif snake_comp > snake_player:
            status = "player"  # grę zaczyna przeciwnik
            domino_snake = [computer.pop(computer.index(snake_comp))]
        else:
            status = "computer"
            domino_snake = [player.pop(player.index(snake_player))]

        return {"stock": stock, "computer": computer, "player": player, "domino": domino_snake, "status": status}


def print_player_pieces(pieces):
    pieces_to_print = ""
    for index, val in enumerate(pieces, 1):
        pieces_to_print += f"{index}:{val}\n"
    return pieces_to_print


def print_domino(dominos):
    if len(dominos) > 6:
        return f"{str(dominos[:3])[1:-1]}...{str(dominos[-3:])[1:-1]}"
    else:
        return str(dominos)[1:-1]


def calc_draw(dominos):
    dominos = str(dominos)
    for i in range(0, 7):
        if dominos.count(str(i)) >= 8:
            return "Status: The game is over. It's a draw!"
    return None


def calc_winner(computer, player, dominos):
    if len(player) == 0:
        return "Status: The game is over. You won!"
    elif len(computer) == 0:
        return "Status: The game is over. The computer won!"
    else:
        return calc_draw(dominos)


def is_integer(text):
    try:
        integer = int(text)
        return integer
    except ValueError:
        return None


def input_test(input_to_test, status):
    input_to_test = is_integer(input_to_test)
    if input_to_test in range(- len(game[status]), len(game[status]) + 1):
        return input_to_test
    else:
        return None


def check_legality_left(input_to_test, status):
    input_abs = abs(input_to_test) - 1
    if game[status][input_abs][0] == game["domino"][0][0]:
        game[status][input_abs].reverse()                   # reverse the domino
        return input_to_test
    elif game[status][input_abs][1] == game["domino"][0][0]:
        return input_to_test
    else:
        return None


def check_legality_right(input_to_test, status):
    input_abs = input_to_test - 1
    if game[status][input_abs][1] == game["domino"][-1][1]:
        game[status][input_abs].reverse()
        return input_to_test
    elif game[status][input_abs][0] == game["domino"][-1][1]:
        return input_to_test
    else:
        return None


def input_test_legality(input_to_test, status):
    if input_to_test == 0:
        return input_to_test
    elif input_to_test < 0:
        return check_legality_left(input_to_test, status)
    elif input_to_test > 0:
        return check_legality_right(input_to_test, status)
    else:
        return None


def move(move, status):
    if move == 0 and len(game["stock"]) != 0:
        game[status].append(game["stock"].pop())
    elif move > 0:
        game["domino"].append(game[status].pop(move - 1))
    elif move < 0:
        game["domino"].insert(0, game[status].pop(abs(move) - 1))


def artificial_intel(status, dominos):
    rates = {}

    for d in range(0, 7):
        rate = 0
        for piece in game[status] + dominos:
            if d in piece:
                rate += 1
        rates[d] = rate

    for piece in game[status]:
        score = rates[piece[0]] + rates[piece[1]]
        piece.append(score)

    game[status].sort(key=lambda x: x[2], reverse=True)
    game[status] = [x[:2] for x in game[status]]

    return game[status]


game = initiation()

while True:

    game["status"] = calc_winner(game["computer"], game["player"], game["domino"]) or game["status"]

    print(f"""{'=' * 70}
Stock size: {len(game['stock'])}
Computer pieces: {len(game['computer'])}

{print_domino(game["domino"])}

Your pieces:
{print_player_pieces(game["player"])}""")

    if game["status"] == "player":
        choice = input("Status: It's your turn to make a move. Enter your command.")
        if choice == "q":
            break

        while True:
            choice = input_test(choice, game["status"])
            if choice is None:
                choice = input("Invalid input. Please try again.\n")
                continue

            choice = input_test_legality(choice, game["status"])
            if choice is None:
                choice = input("Illegal move. Please try again.\n")
                continue
            break

        move(choice, game["status"])

        game["status"] = "computer"

    elif game["status"] == "computer":
        choice = input("Status: Computer is about to make a move. Press Enter to continue...")

        order = artificial_intel(game["status"], game["domino"])

        for i in range(1, len(order) + 1):

            if input_test_legality(i, game["status"]):
                choice = input_test_legality(i, game["status"])
                break
            elif input_test_legality(- i, game["status"]):
                choice = input_test_legality(- i, game["status"])
                break
            elif i == len(order):
                choice = 0

        move(choice, game["status"])

        game["status"] = "player"

    else:
        print(game["status"])
        break
