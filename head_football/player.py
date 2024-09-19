import os

# Constants for the game
LEFT = 37
RIGHT = 39
UP = 38

# Path to resources
path = os.getcwd()

class Player:
    def __init__(self, x, y, r, g, n):
        """
        Initialize a Player object.

        :param x: Initial x position of the player
        :param y: Initial y position of the player
        :param r: Radius of the player
        :param g: Ground level
        :param n: Player number (1 or 2)
        """
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.n = n
        self.vx = 0
        self.vy = 0
        self.goal = False
        self.img_n_prv = -1
        self.img_n = 0
        self.img_x1 = 0
        self.img_x2 = 100
        self.key_handler = {LEFT: False, RIGHT: False, UP: False, 'Kick': False}
        self.left = True
        self.right = True
        self.up = True
        self.kick = True

        # Load player image based on player number
        self.img = loadImage(path + "/images/" + f"head{n}.png")

    def gravity(self):
        """Apply gravity to the player."""
        if self.y + self.r < self.g:
            if self.vy < 0:
                self.vy += 0.24
            elif self.vy > 0:
                self.vy += 0.4
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        else:
            self.vy = 0

    def player_player(self, player):
        """
        Handle interactions between this player and another player.

        :param player: The other player object
        """
        dx = (self.x + player.x) / 2
        dy = (self.y + player.y) / 2

        # Handle collision when players are on the ground
        if (dx - self.x)**2 + (dy - self.y)**2 < self.r**2 and self.vy == 0 and player.vy == 0:
            if self.x < player.x:
                self.x = dx - self.r
                player.x = dx + self.r
                self.vx, player.vx = player.vx, self.vx
                self.kick, player.kick = False, False
                self.right, player.left = False, False
            else:
                self.x = dx + self.r
                player.x = dx - self.r
                self.vx, player.vx = player.vx, self.vx
                self.kick, player.kick = False, False
                self.left, player.right = False, False

        # Handle collision when players are jumping
        elif (dx - self.x)**2 + (dy - self.y)**2 < self.r**2 and self.vy != 0:
            if dx < player.x:
                self.vx = -2 - player.vx
                self.vx = -self.vx if self.vx > 0 else self.vx
                self.vy = 1
                self.motion_v, self.motion_h = True, True
                self.right, player.left = False, False
                self.up, player.up = False, False
                self.key_handler[UP], player.key_handler[UP] = False, False
            else:
                self.vx = 2 + player.vx if player.vx > 0 else 2 - player.vx
                self.vx = -self.vx if self.vx < 0 else self.vx
                self.vy = 1
                self.motion_v, self.motion_h = True, True
                self.left, player.right = False, False
                self.key_handler[UP], player.key_handler[UP] = False, False

        # Reset movement permissions
        self.kick = self.left = self.right = self.up = True
        player.kick = player.left = player.right = player.up = True

    def update(self):
        """Update player position and handle interactions."""
        self.gravity()

        # Handle interactions with the other player
        if self.n == 1:
            self.player_player(game.player2)
        elif self.n == 2:
            self.player_player(game.player1)

        # Movement based on key presses
        if self.key_handler[LEFT] and self.left:
            self.vx = -2.5
        elif self.key_handler[RIGHT] and self.right:
            self.vx = 2.5
        else:
            self.vx = 0 if self.vx == 0 else self.vx - 0.1 if self.vx > 0 else self.vx + 0.1

        if self.key_handler[UP] and self.y + self.r == self.g and self.up:
            self.vy = -7

        # Update position
        self.y += self.vy
        self.x += self.vx

        # Boundary checks
        self.y = min(self.g - self.r, self.y)
        self.x = max(self.r, min(1200 - self.r, self.x))

    def display(self):
        """Display the player with animations."""
        self.update()
        
        # Determine kicking animation based on the state
        limit_img = 300 if not self.kick else 600
        if self.key_handler['Kick']:
            if frameCount % 3 == 0:
                self.img_x1 += 100
                self.img_x2 += 100
                if self.img_x1 >= limit_img:
                    self.img_x1, self.img_x2 = limit_img - 100, limit_img
        elif self.img_n > 0:
            if frameCount % 3 == 0:
                self.img_x1 -= 100
                self.img_x2 -= 100
                self.img_n -= 1
        else:
            self.img_x1, self.img_x2 = 0, 100

        # Display the player image
        if self.n == 1:
            image(self.img, self.x - self.r - 20, self.y - self.r, 100, 80, self.img_x1, 0, self.img_x2, 80)
        elif self.n == 2:
            image(self.img, self.x - self.r - 20, self.y - self.r, 100, 80, self.img_x2, 0, self.img_x1, 80)
