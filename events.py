import cocos
from cocos.director import director

class KeyDisplay(cocos.layer.Layer):
    # If you want that your layer receives director.window events
    # you must set this variable to 'True'
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

# This class defines a key_pressed set, which should be the set of keys pressed at any time. However, this code as it is still does nothing. We need to tell this layer to update this set when a key is pressed or released. In other words, we need to add event handlers to the layer. Adding event handlers to a layer is just a matter of adding methods to it called on_<event name>. The two events that interest us now are on_key_press and on_key_release:

def on_key_press (self, key, modifiers):
    """This function is called when a key is pressed.
    'key' is a constant indicating which key was pressed.
    'modifiers' is a bitwise or of several constants indicating which
        modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
    """
    self.keys_pressed.add(key)
    self.update_text()

def on_key_release (self, key, modifiers):
    """This function is called when a key is released.

    'key' is a constant indicating which key was pressed.
    'modifiers' is a bitwise or of several constants indicating which
        modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

    Constants are the ones from pyglet.window.key
    """

    self.keys_pressed.remove (key)
    self.update_text()

def update_text(self):
    key_names = [pyglet.window.key.symbol_string (k) for k in self.keys_pressed]
    text = 'Keys: '+','.join (key_names)
    # Update self.text
    self.text.element.text = text

# With that code, the layer is now fully working. You can press and release keys or key combinations, and you will se how the display is updated telling you which keys are pressed at any time.

# Handling mouse input is similar. You have three events of interest: on_mouse_press, on_mouse_motion and on_mouse_drag. With that, we can define our layer:

class MouseDisplay(cocos.layer.Layer):

    is_event_handler = True     #: enable director.window events

    def __init__(self):
        super( MouseDisplay, self ).__init__()

        self.posx = 100
        self.posy = 240
        self.text = cocos.text.Label('No mouse events yet', font_size=18, x=self.posx, y=self.posy )
        self.add( self.text )

    def update_text (self, x, y):
        text = 'Mouse @ %d,%d' % (x, y)
        self.text.element.text = text
        self.text.element.x = self.posx
        self.text.element.y = self.posy

# And then add event handlers to update the text when the mouse is moved, and change the text position when any button is clicked:

def on_mouse_motion (self, x, y, dx, dy):
    """Called when the mouse moves over the app window with no button pressed

    (x, y) are the physical coordinates of the mouse
    (dx, dy) is the distance vector covered by the mouse pointer since the
      last call.
    """
    self.update_text (x, y)

def on_mouse_drag (self, x, y, dx, dy, buttons, modifiers):
    """Called when the mouse moves over the app window with some button(s) pressed

    (x, y) are the physical coordinates of the mouse
    (dx, dy) is the distance vector covered by the mouse pointer since the
      last call.
    'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
    'modifiers' is a bitwise or of pyglet.window.key modifier constants
       (values like 'SHIFT', 'OPTION', 'ALT')
    """
    self.update_text (x, y)

def on_mouse_press (self, x, y, buttons, modifiers):
    """This function is called when any mouse button is pressed

    (x, y) are the physical coordinates of the mouse
    'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
    'modifiers' is a bitwise or of pyglet.window.key modifier constants
       (values like 'SHIFT', 'OPTION', 'ALT')
    """
    self.posx, self.posy = director.get_virtual_coordinates (x, y)
    self.update_text (x,y)

director.init(resizable=True)
# Run a scene with our event displayers:
director.run(cocos.scene.Scene(KeyDisplay(), MouseDisplay()))
