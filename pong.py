import cocos
import pyglet
from cocos.director import director
from cocos.actions.interval_actions import MoveBy, MoveTo, Repeat

PADDLE_SPEED = 20
TIME_TICK = 0.1
TIME_PER_FRAME = 1.0 / 60

move_up   = Repeat(MoveBy((0, PADDLE_SPEED),  TIME_TICK))
move_down = Repeat(MoveBy((0,- PADDLE_SPEED), TIME_TICK))

#initial_ball_velocity = Repeat(MoveBy((PADDLE_SPEED, PADDLE_SPEED), TIME_TICK))

MIN_X = 0
MAX_X = 600
MIN_Y = 0
MAX_Y = 600

BALL_SIZE = (48, 48)
PADDLE_SIZE = (20, 80)
INITIAL_BALL_VELOCITY = (5,0)

def axis_overlapping(min_a, max_a, min_b, max_b):
    if max_b > min_a and min_b < min_a:
        return True
    elif max_a > min_b and max_b > max_a:
        return True
    elif max_a > min_b > min_a:
        return True
    elif max_b > min_a > min_b:
        return True
    else:
        return False

def colliding(a, b):
    if axis_overlapping(a.position[0] - (a.size[0] / 2), a.position[0] + (a.size[0] / 2), b.position[0] - (b.size[0] / 2), b.position[0] + (b.size[0] / 2)) and axis_overlapping(a.position[1] - (a.size[1] / 2), a.position[1] + (a.size[1] / 2), b.position[1] - (b.size[1] / 2), b.position[1] + (b.size[1] / 2)):
        return True
    else:
        return False

def bounce(ball, paddle):
    ball.velocity = (-ball.velocity[0], -ball.velocity[1])

class Collidable:
    def __init__(self):
        self.position = (0,0)
        self.size = (0,0)

class BallLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super(BallLayer, self ).__init__()

        self.elapsed = 0

        self.ball = cocos.sprite.Sprite("images/pokeball.png")
        self.ball.size = BALL_SIZE
        #self.ball.velocity = (5,2)
        self.ball.velocity = INITIAL_BALL_VELOCITY

        self.paddle_a = cocos.sprite.Sprite("images/paddle_a.png")
        self.paddle_b = cocos.sprite.Sprite("images/paddle_b.png")

        self.add(self.ball)
        self.add(self.paddle_a)
        self.add(self.paddle_b)

        self.ball.position = (200, 200)
        #self.ball.do(initial_ball.velocity)
        self.paddle_a.position = (10, 200)
        self.paddle_b.position = (600, 200)
        self.paddle_a.size = PADDLE_SIZE
        self.paddle_b.size = PADDLE_SIZE

        self.schedule( self.step )

    def step(self, delta_time):
        self.elapsed += delta_time
        if self.elapsed > time_per_frame:
            print("step")
            self.elapsed = 0
            self.ball.position = (self.ball.position[0] + self.ball.velocity[0], self.ball.position[1] + self.ball.velocity[1])

            if colliding(self.ball, self.paddle_a):
                bounce(self.ball, self.paddle_a)
            if colliding(self.ball, self.paddle_b):
                bounce(self.ball, self.paddle_a)

            # TODO: add a point for player A
            if self.ball.position[0] > max_x or self.ball.position[0] < min_x:
                # self.ball.velocity = (-self.ball.velocity[0], self.ball.velocity[1])
                self.ball.position = (100,200)
            # TODO: add a point for player B
            if self.ball.position[1] > max_y or self.ball.position[1] < min_y:
                self.ball.velocity = (self.ball.velocity[0], -self.ball.velocity[1])

            #

        else:
            print("%s was less than %s" % (self.elapsed, time_per_frame))

    def on_key_press (self, key, modifiers):
        if key == 65362:
            self.current_action = self.paddle_a.do(move_up)
        elif key == 65364:
            self.current_action = self.paddle_a.do(move_down)
        else:
            print("(ball) unknown key pressed:", key)

    def on_key_release (self, key, modifiers):
        print("(ball) released:", key)
        self.paddle_a.remove_action(self.current_action)


class KeyDisplay(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super( KeyDisplay, self ).__init__()

        self.text = cocos.text.Label("", x=100, y=280 )

        # To keep track of which keys are pressed:
        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string (k) for k in self.keys_pressed]
        text = 'Keys: '+','.join (key_names)
        # Update self.text
        self.text.element.text = text

    def on_key_press (self, key, modifiers):
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release (self, key, modifiers):
        self.keys_pressed.remove (key)
        self.update_text()

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string (k) for k in self.keys_pressed]
        text = 'Keys: '+','.join (key_names)
        self.text.element.text = text

if __name__ == '__main__':
    director.init(resizable=True)
    # Run a scene with our event displayers:
    director.run(cocos.scene.Scene(KeyDisplay(), BallLayer()))
