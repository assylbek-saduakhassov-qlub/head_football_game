import os

# Path to resources
path = os.getcwd()

class Net:
    def __init__(self, n):
        """
        Initialize a Net object.

        :param n: Net number (1 or 2), representing the team
        """
        self.w = 128  # Net width
        self.h = 200  # Net height
        self.netnumber = n  # Net number (1 for left net, 2 for right net)
        self.score = 0  # Score for the net
        self.img = loadImage(path + "/images/" + f"net{self.netnumber}.png")  # Load the net image

    def goal(self):
        """
        Check if the ball has entered the goal and update the score.
        """
        ball = game.ball  # Reference to the game's ball object

        # Check if ball enters the left net (netnumber 2)
        if self.netnumber == 2 and 0 < ball.x < 134 and ball.y > 485 and not game.player1.goal and not game.player2.goal:
            game.goal_sound.rewind()
            game.goal_sound.play()
            game.net_sound.rewind()
            game.net_sound.play()
            game.player1.goal = True
            game.seconds = time.time()  # Record the time of the goal

        # Check if ball enters the right net (netnumber 1)
        elif self.netnumber == 1 and ball.x > 1070 and ball.y > 485 and not game.player1.goal and not game.player2.goal:
            game.goal_sound.rewind()
            game.goal_sound.play()
            game.net_sound.rewind()
            game.net_sound.play()
            game.player2.goal = True
            game.seconds = time.time()  # Record the time of the goal

    def display(self):
        """
        Display the net on the screen and check for goals.
        """
        self.goal()  # Check if a goal has been scored

        # Draw the net image on the left or right side of the field
        if self.netnumber == 2:
            image(self.img, 0, 480, self.w, self.h)  # Left net
        elif self.netnumber == 1:
            image(self.img, 1072, 480, self.w, self.h)  # Right net
