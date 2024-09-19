# Import necessary components and modules
from head_football.game import Game
from head_football.game_control import keyPressed, keyReleased, mouseClicked
from head_football.player import Player
from head_football.ball import Ball
from head_football.net import Net

# Define the screen dimensions and ground level
WIDTH = 1200
HEIGHT = 800
GROUND = 675

# Initialize the game with the screen dimensions and ground level
game = Game(WIDTH, HEIGHT, GROUND)

def setup():
    """Setup the Processing window and initialize the game."""
    size(WIDTH, HEIGHT)  # Set the size of the game window
    background(119, 198, 110)  # Set the background color for the field

def draw():
    """Draw the game elements and handle game logic."""
    game.background_sound.play()  # Play the background music
    game.display()  # Display the game elements (players, ball, nets, etc.)

def mouseClicked():
    """Handle mouse click events to reset the game if necessary."""
    # Call the game control's mouseClicked function to handle the event
    mouseClicked()

def keyPressed():
    """Handle key press events for player controls."""
    # Call the game control's keyPressed function to handle the event
    keyPressed()

def keyReleased():
    """Handle key release events for stopping player movements."""
    # Call the game control's keyReleased function to handle the event
    keyReleased()
