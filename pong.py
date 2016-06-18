import cocos
import pyglet
from cocos.director import director
from cocos.actions.interval_actions import MoveBy, MoveTo, Repeat

PADDLE_SPEED = 20

move_up   = Repeat(MoveBy((0, PADDLE_SPEED),  0.1))
move_down = Repeat(MoveBy((0,- PADDLE_SPEED), 0.1))

class BallLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super(BallLayer, self ).__init__()
        # self.text = cocos.text.Label("Ball Layer", x=200, y=380 )
        # self.add(self.text)

        self.ball = cocos.sprite.Sprite("images/pokeball.png")

        self.paddle_a = cocos.sprite.Sprite("images/paddle_a.png")
        self.paddle_b = cocos.sprite.Sprite("images/paddle_b.png")

        self.add(self.ball)
        self.add(self.paddle_a)
        self.add(self.paddle_b)

        move = MoveBy((500,500), 5)
        #self.ball.do(move)

        self.ball.position = (200, 200)
        self.paddle_a.position = (10, 200)
        self.paddle_b.position = (600, 200)

    def on_key_press (self, key, modifiers):
        if key == 65362:
            self.current_action = self.paddle_a.do(move_up)
        elif key == 65364:
            self.current_action = self.paddle_a.do(move_down)
        else:
            print("(ball) unknown key pressed:", key)

    def on_key_release (self, key, modifiers):
        print("(ball) released:", key)
        #self.current_action.stop()
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