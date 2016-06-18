import cocos
from cocos.actions import *

class HelloWorld(cocos.layer.ColorLayer):
    def __init__(self):
        # blueish color
        super( HelloWorld, self ).__init__( 64,64,224,255)

        label = cocos.text.Label('Hello, World!',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center')

        # set the label in the center of the screen
        label.position = 320,240
        self.add( label )

        sprite = cocos.sprite.Sprite('images/dk.jpg')

        sprite.position = 320,240

        sprite.scale = 3

        self.add( sprite, z=1 )

        scale = ScaleBy(3, duration=2)


# Notice that the ‘+’ operator is the Sequence action:

        label.do( Repeat( scale + Reverse( scale) ) )

# And we tell the sprite to do the same actions but starting with the ‘scale back’ action:

        sprite.do( Repeat( Reverse(scale) + scale ) )

cocos.director.director.init()
hello_layer = HelloWorld ()

# And... we tell the Layer (yes, all CocosNode objects can execute actions) to execute a RotateBy action of 360 degrees in 10 seconds:

hello_layer.do( RotateBy(360, duration=10) )

# A scene that contains the layer hello_layer
main_scene = cocos.scene.Scene (hello_layer)

# And now, start the application, starting with main_scene
cocos.director.director.run (main_scene)


