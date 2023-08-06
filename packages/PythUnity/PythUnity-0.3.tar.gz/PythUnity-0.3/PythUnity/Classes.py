import Variables
import copy
import pygame
class Object:
  def __init__(self, rect, image, onClick = None, onDrag = None, onClickOff = None, enableDragOff = False):
    self.destroyed = False
    self.parent = None
    self.children = []
    self.image = None
    self.text = None
    self.color = None
    self.components = []
    if(type(image) is tuple):
      self.color = image
    elif(type(image) is String):
      self.text = image
    else:
      self.image = image 
      ratio = image.get_size()
      min = ratio[0]
      if(min > ratio[1]):
        min = ratio[1]
      ratio = (int(rect.width / ratio[1] * min), int(rect.height / ratio[0] * min))
      print(ratio)
      self.image = pygame.transform.scale(self.image, ratio)
    self.rect = rect
    if onClick != None or onDrag != None:
      self.button = Button(onClick, onDrag, onClickOff, enableDragOff)
    else:
      self.button = None
  #####
  def Decendants(self):
    Throw(self)
    indexes = []
    for i in self.children:
      indexes.append(i)
      indexes.extend(Variables.parts[i].Decendants())
    return indexes
  def Move(self, newIndex):#components can have their update function skipped on accident if ran in another comp.update
    Throw(self)
    children = self.GetParentChildren()
    oldIndex = self.index
    self.index = newIndex
    del children[oldIndex]
    children.insert(newIndex, self)
    i = oldIndex
    if(newIndex > oldIndex):
      while(i < newIndex):
        children[i].index = i
        i = i + 1
    elif(newIndex < oldIndex):
      while(i >= newIndex):
        children[i].index = i
        i = i - 1
  def SetParent(self, newParent):
    Throw(self)
    children = self.GetParentChildren()
    self.Move(len(children))#make it so other children have their indexes fixed
    del children[self.index]
    self.parent = newParent
    self.parent.children.append(self)
    self.index = len(self.parent.children) - 1
  def GetParentChildren(self):
    Throw(self)
    children = None
    if(self.parent != None):
      children = self.parent.children
    else:
      children = Variables.parts
    return children
  def Copy(self):
    Throw(self)
    CopyHelp(self)

    parChildren = self.GetParentChildren()
    copied = copy.deepcopy(self)
    
    copied.index = len(parChildren) - 1
    parChildren.append(copied)
    copied.Move(self.index + 1)
    CopyUnHelp(self)
    CopyUnHelp(copied)
    return copied
  def Destroy(self):
    Throw(self)
    children = self.GetParentChildren()
    self.Move(len(children))
    del children[self.index]
    self.index = -1 #will cause error if used incorrectly, did this on purpous
    self.destroyed = True
    for i in self.children:
      i.Destroy()
  def AddComp(self, comp):
    self.components.append(comp)
    if(comp[0] != None):
        comp[0](self)
class Button:
  def __init__(self, onClick, onDrag, onClickOff, enableDragOff):
    self.onClick = onClick
    self.onClickOff = onClickOff
    self.onDrag = onDrag
    self.dragging = False
    self.enableDragOff = enableDragOff
class String:
  def __init__(self, text, fontSize, font, fontColor, backgroundColor):
    self.fontSize = fontSize
    self.text = text
    self.font = font
    self.fontColor = fontColor
    self.backgroundColor = backgroundColor

def CopyHelp(self):
  if(self.image != None):
    self.image = pygame.image.tostring(self.image, 'RGBA')
  for i in self.children:
    CopyHelp(i)

def CopyUnHelp(self):
  if(self.image != None):
    self.image = pygame.image.fromstring(self.image, self.rect.size, 'RGBA')
  for i in self.children:
    CopyUnHelp(i)
def Throw(self):
  if(self.destroyed):
    raise Exception("Object was destroyed")