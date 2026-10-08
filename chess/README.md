##CHESS PROJECT

A terminal application where you can play both singleplayer and local multiplayer.
Multiplayer mode succesfully implemented.
Singleplayer mode, working on implementing and optimizing minimax, at the moment, you can still play against the computer who will play random moves.

#chess.py: main file to execute to run the application
#utils.py: omly contains 2 functions: int_input to manage convertions to int of user input; clear_terminal self explanatory
#pieces.py: contains pieces classes, which contains pieces logic of movement and generate_move method
#board.py: contains the Board class, which contains the logic of the whole game, looks for checks, stalls, draws and wins, calculate legal moves
