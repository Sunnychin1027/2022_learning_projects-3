"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

This program will be import into breakout.py,
it include bricks, paddle and ball, once mouseclick the ball will start
moving, user will move the paddle to bounce the ball back and remove bricks.
The game will stop when the ball drop lower than the paddle, three chances
are included.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Height of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        # self.window.add(self.paddle, x=(self.window.width - self.paddle.width) / 2, y=window_height - paddle_offset)
        onmousemoved(self.move)

        # Center a filled ball in the graphical window
        self.ball = GOval(2*ball_radius, 2*ball_radius, x=(window_width-ball_radius)/2, y=(window_height-ball_radius)/2)
        self.ball.filled = True
        self.window.add(self.ball)

        # Default initial velocity for the ball
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx
        # Set switch
        self.moving = False
        onmouseclicked(self.click)

        # Initialize our mouse listeners
        # Draw bricks
        self.brick = GRect(brick_width, brick_height)
        self.brick.filled = True
        x = 0
        y = brick_offset
        for i in range(brick_rows):
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                self.window.add(self.brick, x, y)
                if x % 2 == 0:
                    self.brick.fill_color = 'pink'
                else:
                    self.brick.fill_color = 'orange'
                x += (brick_width + brick_spacing)
            y += (brick_height + brick_spacing)
            x = 0
        self.num_bricks = BRICK_COLS * BRICK_ROWS
        self.count = 0

        # Score label
        # self.score_label = GLabel('Score : ' + str(self.score))
        # self.score_label.font = '-20'
        # self.score_label.text = 'Score：' + str(self.score)
        # self.window.add(self.score_label, x=0, y=self.window.height)

    # Set paddle and mouse position, paddle have to be above paddle offset
    def move(self, event):
        self.paddle.x = event.x - self.paddle.width / 2
        self.paddle.y = self.window.height - PADDLE_OFFSET - self.paddle.width/2
        if self.paddle.x < 0:
            self.paddle.x = 0
        elif self.paddle.x + self.paddle.width >= self.window.width:
            self.paddle.x = self.window.width - self.paddle.width
        self.window.add(self.paddle, x=self.paddle.x, y=self.paddle.y)

    # Once mouse clicked, turn on switch and start moving
    def click(self, event):
        if not self.moving:
            self.moving = True
            self.__dx = random.randint(1, MAX_X_SPEED)
            self.__dy = INITIAL_Y_SPEED
            if random.random() > 0.5:
                self.__dx = -self.__dx

    def get__dx(self):
        return self.__dx

    def get__dy(self):
        return self.__dy

    # Set the velocity when the ball hits window wall
    def wall(self):
        if self.ball.x <= 0 or self.ball.x >= self.window.width - self.ball.width:
            self.set_vx()
            self.count = 0
        if self.ball.y <= 0 or self.ball.y + self.ball.height >= self.window.height:
            self.set_vy()
            self.count = 0

    # While moving, check if the 4 corner of ball bump into sth, if it is brick, remove, else it's paddle
    def check_n_remove(self):
        maybe_object1 = self.window.get_object_at(self.ball.x, self.ball.y)
        maybe_object2 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        maybe_object3 = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        maybe_object4 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)

        if self.ball.y + self.ball.height < self.paddle.y:
            # Bricks
            if maybe_object1 is not None:
                self.window.remove(maybe_object1)
                self.num_bricks -= 1
                self.set_vy()
                self.count = 0
            elif maybe_object2 is not None:
                self.window.remove(maybe_object2)
                self.num_bricks -= 1
                self.set_vy()
                self.count = 0
            elif maybe_object3 is not None:
                self.window.remove(maybe_object3)
                self.num_bricks -= 1
                self.set_vy()
                self.count = 0
            elif maybe_object4 is not None:
                self.window.remove(maybe_object4)
                self.num_bricks -= 1
                self.set_vy()
                self.count = 0

        # For detecting paddle
        elif self.ball.y + self.ball.height >= self.paddle.y:
            # count for avoid vibration
            if maybe_object1 is not None:
                self.count += 1
                if self.count == 1:
                    self.set_vy()
                # else:
                #     self.__dy = self.__dy
                #     self.count = 0
            elif maybe_object2 is not None:
                self.count += 1
                if self.count == 1:
                    self.set_vy()
                # else:
                #     self.__dy = self.__dy
                #     self.count = 0
            elif maybe_object3 is not None:
                self.count += 1
                if self.count == 1:
                    self.set_vy()
                # else:
                #     self.__dy = self.__dy
                #     self.count = 0
            elif maybe_object4 is not None:
                self.count += 1
                if self.count == 1:
                    self.set_vy()
                # else:
                #     self.__dy = self.__dy
                #     self.count = 0

    def set_vx(self):
        self.__dx = -self.__dx

    def set_vy(self):
        self.__dy = -self.__dy



