# Battleship Game

This is a simple version of the classic Battleship game that you can play on your computer. You can play against another player or against the computer. The game involves placing ships on a 10x10 grid and taking turns shooting at the opponent's ships. The first player to sink all of the opponent's ships wins.

## Requirements

- Python 3.x
- Required dependencies:
    - `dictpl` (for Polish translations)
    - `dictang` (for English translations)
    - `os` (for clearing the terminal)

## How to Play

1. **Start the Game**:  
   When you start the game, you'll be asked to choose the language. Type `eng` for English or `pl` for Polish.

2. **Game Mode**:  
   After choosing the language, you'll be asked if you want to play against the computer. Type `yes` (in English) or `tak` (in Polish) to play against the computer, or `no` (in English) or `nie` (in Polish) to play with another player.

3. **Place Ships**:  
   Each player (or the computer) will need to place their ships on the 10x10 grid. Each ship has a length of 1, and you'll be asked to provide the coordinates for each placement. Ships must be placed either horizontally or vertically.

4. **Taking Turns**:  
   After both players have placed their ships, the game proceeds in turns. On each turn, you will shoot at the opponent's grid by entering coordinates. The result will be displayed (hit, miss, or sunk).

5. **Winning the Game**:  
   The game ends when one player sinks all of the opponent's ships. The winner will be announced at the end of the game.

## Class Overview

### 1. **Board Class**
   - Represents a 10x10 game board.
   - Contains methods to display the board.

### 2. **ShipBoard Class (Inherits from Board)**
   - Inherits from `Board` and allows for placing and managing ships.
   - Ships are added by specifying coordinates, and the board is updated accordingly.

### 3. **ShootingBoard Class (Inherits from Board)**
   - Inherits from `Board` and keeps track of shots fired and their results (hit or miss).
   - Displays the updated shooting board after each turn.

### 4. **Player Class**
   - Contains a `ShipBoard` and a `ShootingBoard` for a player.
   - Handles the action of shooting at the opponent's board and placing ships.

### 5. **ComputerPlayer Class (Inherits from Player)**
   - A subclass of `Player` that automatically places its ships and randomly shoots at the opponent's grid.

## Gameplay

1. **Language Selection**:  
   After starting the game, you will choose a language by typing `eng` for English or `pl` for Polish.

2. **Game Mode**:  
   You will decide whether you want to play against the computer or another player. If you choose to play against the computer, the computer will automatically place its ships and shoot randomly at your grid.

3. **Ship Placement**:  
   The game will prompt you to enter the coordinates where you'd like to place your ships. Remember, ships must be placed horizontally or vertically.

4. **Taking Shots**:  
   On each turn, you will enter coordinates to shoot at your opponent's grid. The game will show you whether you hit or missed. Your shooting board will be updated with the results.

5. **Game End**:  
   The game ends when one player sinks all of the opponent's ships. The winner will be announced.
