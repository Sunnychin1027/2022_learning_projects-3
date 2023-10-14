"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

This game include bricks, paddle and ball, once mouseclick the ball will start
moving, user will move the paddle to bounce the ball back and remove bricks.
The game will stop when the ball drop lower than the paddle, three chances
are included.
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    lives = NUM_LIVES
    # graphics.score_label()
    # Add the animation loop here!
    while True:
        pause(FRAME_RATE)
        if lives < 0:
            break
        elif graphics.num_bricks == 0:
            break
        else:
            if graphics.moving and lives >= 1:
                graphics.ball.move(graphics.get__dx(), graphics.get__dy())
                graphics.wall()
                graphics.check_n_remove()
            if graphics.ball.y >= graphics.window.height - graphics.ball.height:
                lives -= 1
                graphics.ball.x = (graphics.window.width - graphics.ball.width) / 2
                graphics.ball.y = (graphics.window.height - graphics.ball.height) / 2
                graphics.moving = False


if __name__ == '__main__':
    main()
