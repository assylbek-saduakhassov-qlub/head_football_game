import os
from minim import Minim

# Constants
BALL_MAX_SPEED = 25

# Path to resources
path = os.getcwd()
player = Minim(this)

class Ball:
    def __init__(self, x, y, r, g):
        """
        Initialize a Ball object.

        :param x: Initial x position of the ball
        :param y: Initial y position of the ball
        :param r: Radius of the ball
        :param g: Ground level
        """
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vx = -0.3
        self.vy = 0
        self.motion_v = True
        self.motion_h = False
        self.img_n = 5
        self.img = loadImage(path + "/images/" + "ball" + str(self.img_n) + ".png")

        # Load sounds
        self.leg_kick = player.loadFile(path + "/sounds/leg_kick.mp3")
        self.head_kick = player.loadFile(path + "/sounds/head_kick.mp3")

    def gravity(self):
        """Apply gravity and natural deceleration to the ball."""
        # Vertical motion logic
        if self.y + self.r < self.g and self.vy >= 0 and self.motion_v:
            self.vy += 0.2
            if self.y + self.r + self.vy >= self.g:
                time.sleep(0.015)
                self.y = self.g - self.r
                if self.vy < 2.5:
                    self.vy = 0
                    self.motion_v = False
                else:
                    self.vy = -self.vy
        elif self.y + self.r <= self.g and self.vy <= 0 and self.motion_v:
            self.vy += 0.6
            if self.vy >= 0:
                self.vy = self.vy

        # Horizontal motion logic
        if self.vx > 0 and self.y + self.r == self.g and self.motion_h:
            self.vx -= 1
            if self.vx < 0:
                self.vx = 0
                self.motion_h = False
        elif self.vx < 0 and self.y + self.r == self.g and self.motion_h:
            self.vx += 1
            if self.vx > 0:
                self.vx = 0
                self.motion_h = False

        # Speed limitations
        self.vx = max(-BALL_MAX_SPEED, min(BALL_MAX_SPEED, self.vx))
        self.vy = max(-BALL_MAX_SPEED, min(BALL_MAX_SPEED, self.vy))

    def net_ball(self):
        """Handle interactions between the ball and the goal nets."""
        if 0 < self.x < 134 and self.y + self.r <= 490:
            self.g = 485
            if self.vy == 0:
                self.vx = 2
        elif 1072 < self.x < 1200 and self.y + self.r <= 490:
            self.g = 485
            if self.vy == 0:
                self.vx = -2
        elif self.y + self.r < 674:
            self.g = 675
            self.motion_v = True
            self.motion_h = True

    def player_ball_kick(self, player):
        """
        Handle interactions between the player and the ball when kicking.

        :param player: The player object interacting with the ball
        """
        leg_position = player.img_n
        prev_leg_position = player.img_n_prv

        # Adjust ball velocity and play sound based on leg position and interaction point
        if leg_position in [0, 1, 2, 3, 4, 5]:
            leg_x1 = player.x - player.r - 20 if player.n == 1 else player.x + player.r + 20
            leg_x2 = leg_x1 + 28
            leg_y1 = player.y + player.r - 17
            leg_y2 = leg_y1 + 23

            if leg_position > prev_leg_position and (leg_x1 - self.x)**2 + (leg_y1 - self.y)**2 < self.r**2:
                self.leg_kick.rewind()
                self.leg_kick.play()
                self.vx = -self.vx - 10 if self.vx > 0 else self.vx - 10
                self.vy = -self.vy - 15 if self.vy > 0 else self.vy - 15
            elif leg_position == 5:
                if (leg_x1 - self.x)**2 + (leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.vx = -self.vx if self.vx > 0 else self.vx
                    self.vy = -self.vy if self.vy > 0 else self.vy

    def player_ball(self, player):
        """
        Handle interactions between the player and the ball with head hits.

        :param player: The player object interacting with the ball
        """
        dx = (self.x + 2 * player.x) / 3
        dy = (self.y + 2 * player.y) / 3

        if (dx - player.x)**2 + (dy - player.y)**2 <= self.r**2:
            self.head_kick.rewind()
            self.head_kick.play()
            if not self.motion_v and player.vx == 0 and self.vx != 0 and self.vy == 0:
                self.vx = -self.vx + 1 if self.vx < 0 else -self.vx - 1
            elif not self.motion_v:
                self.vx = player.vx
                self.motion_h = True
            elif self.motion_v and self.vx == 0 and player.vx == 0:
                self.vy = -self.vy if self.vy > 0 else self.vy
            else:
                self.vx = player.vx
                if self.y + self.r < self.g and self.x <= player.x:
                    self.vx = -6 + player.vx
                    self.vy = -self.vy - 5 if self.player.vy != 0 else self.vy - 5
                if self.y + self.r < self.g and self.x > player.x:
                    self.vx = 6 + player.vx
                    self.vy = -self.vy - 5 if self.player.vy != 0 else self.vy - 5
                if self.y - self.r <= player.y + player.r and player.y + player.r != self.g:
                    if self.x >= player.x:
                        self.x += player.r / 2
                        self.vx = 5
                    else:
                        self.x -= player.r / 2
                        self.vx = -5

    def player_over_ball(self, player):
        """
        Handle interactions when the player stands over the ball.

        :param player: The player object standing over the ball
        """
        dx = (self.x + 2 * player.x) / 3
        dy = (self.y + 2 * player.y) / 3

        if (dx - player.x)**2 + (dy - player.y)**2 <= self.r**2 and self.y - self.r <= player.y + player.r and player.y + player.r != player.g:
            if self.x > player.x:
                self.vx = 3
                self.motion_h = True
                self.x = player.x + player.r + self.r / 2
            else:
                self.vx = -3
                self.motion_h = True
                self.x = player.x - player.r - self.r / 2

    def update(self):
        """Update the ball's position and handle interactions."""
        self.gravity()
        self.net_ball()
        self.player_over_ball(game.player1)
        self.player_over_ball(game.player2)
        self.player_ball(game.player1)
        self.player_ball(game.player2)
        self.player_ball_kick(game.player1)
        self.player_ball_kick(game.player2)

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Boundary checks
        if self.x - self.r < 0:
            self.vx = -self.vx
        if self.x + self.r > 1200:
            self.vx = -self.vx
        if self.y - self.r < 0:
            self.vy = -self.vy

    def display(self):
        """Display the ball with animations."""
        self.update()

        # Scroll ball image based on horizontal movement
        if self.vx > 0:
            self.img_n = 1 if self.img_n >= 5 else self.img_n + 1
        elif self.vx < 0:
            self.img_n = 5 if self.img_n <= 1 else self.img_n - 1
        self.img = loadImage(path + "/images/" + "ball" + str(self.img_n) + ".png")

        # Display the ball
        image(self.img, self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)
