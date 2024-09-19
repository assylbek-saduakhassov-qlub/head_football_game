from head_football.game import game
from head_football.player import LEFT, RIGHT, UP

def keyPressed():
    """Handle key press events for controlling the players."""
    # Controls for Player 1
    if keyCode == LEFT:
        if game.player1.left:
            game.player1.key_handler[LEFT] = True
            game.player1.key_handler[RIGHT] = False
    elif keyCode == RIGHT:
        if game.player1.right:
            game.player1.key_handler[LEFT] = False
            game.player1.key_handler[RIGHT] = True
    elif keyCode == UP:
        if game.player1.up:
            game.player1.key_handler[UP] = True
    if key == 'p' or key == 'P':
        if game.player1.kick:
            game.player1.key_handler['Kick'] = True

    # Controls for Player 2
    if key == 'a' or key == 'A':
        if game.player2.left:
            game.player2.key_handler[LEFT] = True
            game.player2.key_handler[RIGHT] = False
    elif key == 'd' or key == 'D':
        if game.player2.right:
            game.player2.key_handler[LEFT] = False
            game.player2.key_handler[RIGHT] = True
    elif key == 'w' or key == 'W':
        if game.player2.up:
            game.player2.key_handler[UP] = True
    if key == 'c' or key == 'C':
        if game.player2.kick:
            game.player2.key_handler['Kick'] = True

def keyReleased():
    """Handle key release events for stopping player movements."""
    # Controls for Player 1
    if keyCode == LEFT:
        game.player1.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.player1.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.player1.key_handler[UP] = False
    if key == 'p' or key == 'P':
        game.player1.key_handler['Kick'] = False

    # Controls for Player 2
    if key == 'a' or key == 'A':
        game.player2.key_handler[LEFT] = False
    elif key == 'd' or key == 'D':
        game.player2.key_handler[RIGHT] = False
    elif key == 'w' or key == 'W':
        game.player2.key_handler[UP] = False
    if key == 'c' or key == 'C':
        game.player2.key_handler['Kick'] = False

def mouseClicked():
    """Handle mouse click events to restart the game after a player wins."""
    if game.net1.score > 6 or game.net2.score > 6:
        # Reset game state if a player has won
        game.seconds = 0
        game.stop = 0
        game.stadium_shaking = 0
        game.player1 = Player(1000, game.g - game.player1.r, game.player1.r, game.g, 1)
        game.player2 = Player(200, game.g - game.player2.r, game.player2.r, game.g, 2)
        game.ball = Ball(30, 0, game.ball.r, game.g)
        game.net1 = Net(1)
        game.net2 = Net(2)
        game.net1.score = 0
        game.net2.score = 0
