import cocos
import pyglet
from cocos.director import director
from cocos.actions.interval_actions import MoveBy, MoveTo, Repeat

PADDLE_SPEED = 20
TIME_TICK = 0.1
time_per_frame = 1.0 / 60

move_up   = Repeat(MoveBy((0, PADDLE_SPEED),  TIME_TICK))
move_down = Repeat(MoveBy((0,- PADDLE_SPEED), TIME_TICK))

initial_ball_movement = Repeat(MoveBy((PADDLE_SPEED, PADDLE_SPEED), TIME_TICK))

min_x = 0
max_x = 600
min_y = 0
max_y = 600

class BallLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super(BallLayer, self ).__init__()
        # self.text = cocos.text.Label("Ball Layer", x=200, y=380 )
        # self.add(self.text)

        self.ball_movement = (5,2)

        self.elapsed = 0

        self.ball = cocos.sprite.Sprite("images/pokeball.png")

        self.paddle_a = cocos.sprite.Sprite("images/paddle_a.png")
        self.paddle_b = cocos.sprite.Sprite("images/paddle_b.png")

        self.add(self.ball)
        self.add(self.paddle_a)
        self.add(self.paddle_b)

        self.ball.position = (200, 200)
        #self.ball.do(initial_ball_movement)
        self.paddle_a.position = (10, 200)
        self.paddle_b.position = (600, 200)

        self.schedule( self.step )

    def step(self, delta_time):
        self.elapsed += delta_time
        if self.elapsed > time_per_frame:
            print("step")
            self.elapsed = 0
            self.ball.position = (self.ball.position[0] + self.ball_movement[0], self.ball.position[1] + self.ball_movement[1])

            if self.ball.position[0] > max_x or self.ball.position[0] < min_x:
                self.ball_movement = (-self.ball_movement[0], self.ball_movement[1])
            if self.ball.position[1] > max_y or self.ball.position[1] < min_y:
                self.ball_movement = (self.ball_movement[0], -self.ball_movement[1])


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


director.init(resizable=True)
# Run a scene with our event displayers:
director.run(cocos.scene.Scene(KeyDisplay(), BallLayer()))
