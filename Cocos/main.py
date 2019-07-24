import cocos
#Subclass a Layer and define the logic of you program here:
class HelloWorld(cocos.layer.Layer):
  #Always call super in the constructor:
  def __init__(self):
    super(HelloWorld, self).__init__()
  #After defining the HelloWorld class, we need to initialize and create a window. To do this, we initialize the Director:
  cocos.director.director.init()
  #To display the text, we'll create a Label. Keyword arguments are used to set the font, position and alignment of the label:
  label = cocos.text.Label(
    'Hello, world',
    font_name='Times New Roman',
    font_size=32,
    anchor_x='center', anchor_y='center'
  )
  #The label position will be the center of the screen:
  label.position = 320, 240
  #Since Label is a subclass of CocosNode it can be added as a child. All CocosNode objects know how to render itself, perform actions and transformations. To add it as a layer's child, use the CocosNode.add method:
  self.add(label)
#Then we create a HelloWorld instance:
hello_layer = HelloWorld()
#Then we create an Scene that contains the HelloWorld layer as a child:
main_scene = cocos.scene.Scene (hello_layer)
#And finally we run the scene:
cocos.director.director.run(main_scene)
#A shorter way to write the last 3 statements is this:
#cocos.director.director.run(cocos.scene.Scene(HelloWorld()))