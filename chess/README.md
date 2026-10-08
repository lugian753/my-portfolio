# CHESS PROJECT

A terminal application where you can play both singleplayer and local multiplayer.
Multiplayer mode succesfully implemented.
Working on implementing and optimizing minimax, at the moment, you can still play against the computer who will just play random moves.

### chess.py
Main file to execute to run the application

### utils.py
Omly contains 2 functions: int_input to manage convertions to int of user input; clear_terminal self explanatory.

### pieces.py
Contains pieces classes, which contains pieces logic of movement and generate_move method.

### board.py
Contains the Board class, which contains the logic of the whole game, looks for checks, stalls, draws and wins, calculate legal moves.

### players.py
Contains the Player abstract class, User and Computer classes. methods to get player move either from user input or calculated. Here in the Computer class the minimax algorithm is going to be implemented. As a temporary solution in order to still be able to play singleplayer, i've made it choose a random move.
