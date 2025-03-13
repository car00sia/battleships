import os
import random
import dictpl
import dictang

AMOUNT_OF_SHIPS = 5
playing_with_computer = False

language = input("Choose language, write 'eng' or 'pl': ")
if language == "eng":
    translation = dictang.translations
elif language == "pl":
    translation = dictpl.translations
else:
    print("Not found, the language has been automatically set to English.")
    translation = dictang.translations

computer = input(translation["play_with_computer"])
if computer == "yes" or computer == "tak":
    playing_with_computer = True

class Board:
    def __init__(self):
        self.board_list = []
        for i in range(10):
            self.board_list.append([" "] * 10)

    def display_board(self):
        print("  1 2 3 4 5 6 7 8 9 10")
        for i in range(10):
            row_number = i
            print(f"{chr(row_number + 65)} " + " ".join(self.board_list[i]))

class ShipBoard(Board):
    def __init__(self):
        super().__init__()
        self.remaining_ships = AMOUNT_OF_SHIPS
        self.all_ships = []

    def place_ships(self, is_computer=False):
        if is_computer:
            self.auto_place_ships()
        else:
            self.manual_place_ships()

    def pass_cords(self):
        try:
            print(translation["remaining_ships"].format(self.remaining_ships))
            coordinates = input(translation["enter_coordinates"])
            coordinates = coordinates.split()
            if len(coordinates) != 2:
                raise ValueError(translation["error_coordinates"])

            coord1 = coordinates[0]
            coord2 = coordinates[1]

            row1 = ord(coord1[0].upper()) - ord('A')
            col1 = int(coord1[1:]) - 1
            row2 = ord(coord2[0].upper()) - ord('A')
            col2 = int(coord2[1:]) - 1

            if not (0 <= row1 < 10 and 0 <= col1 < 10):
                raise ValueError(translation["error_invalid_coordinates"])
            if not (0 <= row2 < 10 and 0 <= col2 < 10):
                raise ValueError(translation["error_invalid_coordinates"])
            if not (coord1[0].isalpha() and coord1[1:].isdigit()):
                raise ValueError(translation["error_invalid_coordinates"])
            if not (coord2[0].isalpha() and coord2[1:].isdigit()):
                raise ValueError(translation["error_invalid_coordinates"])
            if not (row1 == row2 or col1 == col2):
                print(translation["error_ship_must_be_straight"])
                raise ValueError(translation["error_ship_must_be_straight"])

            for ship in self.all_ships:
                for segment in ship:
                    if [row1, col1] == segment or [row2, col2] == segment:
                        print(translation["ship_already_added"])
                        self.display_board()
                        raise ValueError(translation["ship_already_added"])

            return row1, col1, row2, col2

        except Exception as e:
            raise e

    def manual_place_ships(self):
        self.display_board()

        while self.remaining_ships > 0:
            try:
                cords = self.pass_cords()
                row1, col1, row2, col2 = cords
                ship = []

                for i in range(min(row1, row2), max(row1, row2) + 1):
                    for j in range(min(col1, col2), max(col1, col2) + 1):
                        self.board_list[i][j] = "o"
                        ship.append([i, j])

                self.all_ships.append(ship)
                self.remaining_ships -= len(ship)
                self.display_board()

            except (ValueError, IndexError) as e:
                print(f"Error: {e}")

    def auto_place_ships(self):
        while self.remaining_ships > 0:
            orientation = random.choice(['h', 'v'])
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if orientation == 'h':
                max_length = 10 - col
                length = random.randint(1, min(self.remaining_ships, max_length))
                conflict = False
                for j in range(col, col + length):
                    if self.board_list[row][j] == "o":
                        conflict = True
                        break
                if conflict:
                    continue
                ship = []
                for j in range(col, col + length):
                    self.board_list[row][j] = "o"
                    ship.append([row, j])
                self.all_ships.append(ship)
                self.remaining_ships -= length
            else:
                max_length = 10 - row
                length = random.randint(1, min(self.remaining_ships, max_length))
                conflict = False
                for i in range(row, row + length):
                    if self.board_list[i][col] == "o":
                        conflict = True
                        break
                if conflict:
                    continue
                ship = []
                for i in range(row, row + length):
                    self.board_list[i][col] = "o"
                    ship.append([i, col])
                self.all_ships.append(ship)
                self.remaining_ships -= length

class ShootingBoard(Board):
    def __init__(self):
        super().__init__()
        self.shots_fired = []
        self.hits = 0
        self.hit_last_turn = False

    def shoot(self, opponent_board):
        try:
            coordinate = input(translation["enter_shot"])
            if not (coordinate and coordinate[0].isalpha() and coordinate[1:].isdigit()):
                raise ValueError(translation["error_invalid_coordinates"])

            row = ord(coordinate[0].upper()) - ord('A')
            col = int(coordinate[1:]) - 1

            if not (0 <= row < 10 and 0 <= col < 10):
                raise ValueError(translation["error_invalid_coordinates"])

            if [row, col] in self.shots_fired:
                print(translation["already_shot"])
                return

            self.shots_fired.append([row, col])

            if [row, col] in [segment for ship in opponent_board.all_ships for segment in ship]:
                print(translation["hit"])
                self.hit_last_turn = True
                self.board_list[row][col] = "x"
                self.hits += 1

                for ship in opponent_board.all_ships:
                    if [row, col] in ship:
                        ship.remove([row, col])
                        if not ship:
                            opponent_board.all_ships.remove(ship)
                            print(translation["sunk"])
                        break
            else:
                print(translation["miss"])
                self.board_list[row][col] = "n"
                self.hit_last_turn = False

            self.display_board()
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")

class Player:
    def __init__(self, is_computer=False):
        self.ship_board = ShipBoard()
        self.shooting_board = ShootingBoard()
        self.is_computer = is_computer

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__(is_computer=True)
        self.available_shots = [f"{chr(65 + i)}{j+1}" for i in range(10) for j in range(10)]
        self.ship_board.auto_place_ships()

    def shoot(self, opponent):
        try:
            coordinate = random.choice(self.available_shots)
            self.available_shots.remove(coordinate)

            row = ord(coordinate[0].upper()) - ord('A')
            col = int(coordinate[1:]) - 1

            self.shooting_board.shots_fired.append([row, col])

            if [row, col] in [segment for ship in opponent.ship_board.all_ships for segment in ship]:
                print(translation["hit"])
                self.shooting_board.hit_last_turn = True
                self.shooting_board.board_list[row][col] = "x"
                self.shooting_board.hits += 1

                for ship in opponent.ship_board.all_ships:
                    if [row, col] in ship:
                        ship.remove([row, col])
                        if not ship:
                            opponent.ship_board.all_ships.remove(ship)
                            print(translation["sunk"])
                        break
            else:
                print(translation["miss"])
                self.shooting_board.board_list[row][col] = "n"
                self.shooting_board.hit_last_turn = False

            self.shooting_board.display_board()

        except (ValueError, IndexError) as e:
            print(f"Error: {e}")

is_game_running = True
if playing_with_computer:
    player1 = Player()
    player2 = ComputerPlayer()
else:
    player1 = Player()
    player2 = Player()

print(translation["place_ships"].format(1))
player1.ship_board.place_ships(player1.is_computer)
os.system('clear')

if playing_with_computer:
    print(translation["computer_placing"])
    os.system('clear')
else:
    print(translation["place_ships"].format(2))
    player2.ship_board.place_ships(player2.is_computer)
    os.system('clear')

turn_counter = 1
while is_game_running:
    if turn_counter % 2 == 1:
        current_player = player1
        opponent = player2
        print(translation["turn"].format(1))
    else:
        current_player = player2
        opponent = player1
        print(translation["turn"].format(2))

    if current_player.is_computer:
        current_player.shoot(opponent)
    else:
        current_player.shooting_board.shoot(opponent.ship_board)

    if current_player.shooting_board.hits == AMOUNT_OF_SHIPS:
        print(translation["win"].format(1 if turn_counter % 2 == 1 else 2))
        is_game_running = False

    if not current_player.shooting_board.hit_last_turn:
        turn_counter += 1
