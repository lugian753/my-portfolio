# TICTACTOE PROJECT

## Description:
A Python terminal application where you can play tictactoe both singleplayer and local multiplayer. Position evaluation and a hint system have been implemented for 
improved user experience and gameplay. Singleplayer is unbeatable due to the Minimax algorithm, which calulates the best possible move in any given position.
For improved performace, minimax has been optimized with alpha-beta pruning, which allows to cut down branches from the moves tree if it already knows there was a
"better worst outcome" (after maximising himself and minimizing opponent) in the previous analysed moves. This will help significantly when applied to more complex
systems like chess.

## Architecture
The board is decleared as an istance of Board, which contains a 3x3 matrix (list of lists) containing spaces if the spot is empty or the character of the player 
(either X or O). The players are declared as instances of User and Computer or both User, depending on what gamemode has been choosen in the menu.
Inside User, a helper is declared as an istance of Computer, its purpose is to calculate the best possible move for the User and give it if requested (Hint System).
The GameManager class puts all the pieces together and allows the game to run, it has a main menu where users can choose which game mode they want to play, it handles
the flow of the game calling methods of players and board when needed. before the game start, a judge is declared as istance of Computer, its purpose is to give an
evaluation of the position after every move, it will tell the user if there is a forced win for one of the players or if its a draw with good play (Evaluation Bar).
The minimax algorithm is implemented as a method of Computer, it is used for the Hint System, the Evaluation Bar and to choose its own moves when playing singleplayer.

## Files
### tictactoe3.py
Contains all the classes (the whole game)

### utils.py
Contains 2 functions, int_input to smoothly manage int convertions of user input and clear_terminal, self explenatory
