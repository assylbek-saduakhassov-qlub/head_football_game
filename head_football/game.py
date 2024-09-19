import os
import random
import time
from head_football.player import Player
from head_football.ball import Ball
from head_football.net import Net
from minim import Minim

# Constants for the game
path = os.getcwd()
player = Minim(this)

class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.seconds = 0
        self.stop = 0
        self.stadium_shaking = 0
        self.player1 = Player(1000, g - 30, 30, g, 1)
        self.player2 = Player(200, g - 30, 30, g, 2)
        self.ball = Ball(30, 0, 15, g)
        self.net1 = Net(1)
        self.net2 = Net(2)

        # Load sounds and images
        self.background_sound = player.loadFile(path + "/sounds/background.mp3")
        self.net_sound = player.loadFile(path + "/sounds/net_goal.mp3")
        self.goal_sound = player.loadFile(path + "/sounds/SUIII.mp3")
        self.field_img = loadImage(path + "/images/" + "field.png")
        self.stadium_img = loadImage(path + "/images/" + "stadium.png")
        self.table_img = loadImage(path + "/images/" + "table.png")

    def player_ball_player(self, player_l, player_r):
        """Handles complex interactions between two players and the ball."""
        dx_p1 = (self.ball.x + 2 * player_l.x) / 3
        dy_p1 = (self.ball.y + 2 * player_l.y) / 3
        dx_p2 = (self.ball.x + 2 * player_r.x) / 3
        dy_p2 = (self.ball.y + 2 * player_r.y) / 3

        dx = (player_r.x + player_l.x) / 2
        dy = (player_r.y + player_l.y) / 2

        if player_l.x < self.ball.x < player_r.x and self.ball.vy == 0:
            if (dx_p1 - player_l.x)**2 + (dy_p1 - player_l.y)**2 <= self.ball.r**2 and (dx_p2 - player_r.x)**2 + (dy_p2 - player_r.y)**2 <= self.ball.r**2:
                choice = random.randint(1, 2)
                if choice == 1:
                    self.ball.x = dx
                    player_r.x = self.ball.x + 45
                    player_l.x = self.ball.x - 45
                    player_l.vy = -7
                    player_l.vx = 7
                elif choice == 2:
                    self.ball.x = dx
                    player_r.x = self.ball.x + 45
                    player_l.x = self.ball.x - 45
                    player_r.vy = -7
                    player_r.vx = -7

    def display(self):
        """Displays the game elements on the screen."""
        image(self.stadium_img, 0, -100)
        image(self.field_img, 0, 595)
        image(self.table_img, 185, 710, 827, 90)

        # Display players, ball, and nets
        self.player1.display()
        self.player2.display()
        self.ball.display()
        self.net1.display()
        self.net2.display()
        self.player_ball_player(self.player2, self.player1)

        # Display score
        textSize(25)
        fill(255, 255, 255)
        text(f"{self.net1.score} - ", 570, 750)
        text(f"{self.net2.score}", 615, 750)

        # Handle goal events and game over conditions
        if self.player1.goal or self.player2.goal:
            self.handle_goal()
        elif self.net1.score > 6:
            self.display_winner("Real Madrid")
        elif self.net2.score > 6:
            self.display_winner("Manchester United")

    def handle_goal(self):
        """Handles goal events, animations, and score updates."""
        fill(0, 0, 0)
        strokeWeight(0)
        rect(0, 0, self.w, self.h)
        if self.stadium_shaking == 0 and frameCount % 6 == 0:
            image(self.stadium_img, -15, -115)
            self.stadium_shaking = 1
        elif frameCount % 6 == 0:
            image(self.stadium_img, 15, -85)
            self.stadium_shaking = 0
        image(self.field_img, 0, 595)
        if frameCount % 4 == 0:
            textSize(60)
            fill(255, 0, 0)
            text("GOAAAAAAAAL!!!", 355, 780)
            self.stadium_shaking = 1
        elif frameCount % 4 == 0:
            textSize(60)
            fill(255, 0, 0)
            text("GOAAAAAAAAL!!!", 355, 780)
            self.stadium_shaking = 0

        # Show scoring player and ball
        if self.player1.goal:
            self.player1.display()
        elif self.player2.goal:
            self.player2.display()

        self.ball.display()
        self.net1.display()
        self.net2.display()

        # Reset after 3 seconds of celebration
        if time.time() - self.seconds > 3:
            self.reset_after_goal()

    def reset_after_goal(self):
        """Resets the game state after a goal has been scored."""
        if self.player1.goal:
            self.net2.score += 1
        elif self.player2.goal:
            self.net1.score += 1

        self.player1.goal = False
        self.player2.goal = False
        self.ball = Ball(30, 0, 15, self.g)
        self.player1 = Player(1000, self.g - 30, 30, self.g, 1)
        self.player2 = Player(200, self.g - 30, 30, self.g, 2)

    def display_winner(self, winner):
        """Displays the winning team and prompts to restart the game."""
        image(self.stadium_img, 0, -100)
        image(self.field_img, 0, 595)
        image(self.table_img, 185, 710, 827, 90)
        self.player1.display()
        self.player2.display()
        self.net1.display()
        self.net2.display()
        textSize(60)
        fill(255, 0, 0)
        text(f"{winner} won!!!", 350, 200)
        text(f"{self.net1.score} - {self.net2.score}", 530, 300)
        textSize(30)
        fill(255, 0, 0)
        text("Press the mouse to restart the game", 450, 400)
