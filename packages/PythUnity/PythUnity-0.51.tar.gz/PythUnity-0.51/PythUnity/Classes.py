from PythUnity import Variables
from PythUnity import Functions
import copy
import pygame
import types
class Object:
  def __init__(self, rect, image, onClick = None, onDrag = None, onClickOff = None, onScroll = None, enableDragOff = False, clickGroup = 0):
    self.destroyed = False
    self.parent = None
    self.children = []
    self.variables = {}
    self.image = None
    self.text = None
    self.color = None
    self.components = []
    self.clickGroup = clickGroup#not implemented yet
    self.velocity = (0, 0)
    if(type(image) is tuple):
      self.color = image
    elif(type(image) is String):
      self.text = copy.deepcopy(image)
    else:
      self.image = image 
      self.ImageUp()
    self.rect = rect
    if onClick != None or onDrag != None or onScroll != None:
      self.button = Button(onClick, onDrag, onClickOff, onScroll, enableDragOff)
    else:
      self.button = None
    Functions.AddObject(self)
  #####
  def __getitem__(self, i):
    return self.children[i]
  def __len__(self):
    return len(self.children)
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
    copied.index = len(parChildren)
    parChildren.append(copied)
    copied.parent = self.parent
    copied.Move(self.index + 1)
    CopyUnHelp(self)
    CopyUnHelp(copied)
    CopyHelp2(copied)
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
  def ImageUp(self):
    ratio = self.image.get_size()
    max = ratio[0]
    if(max < ratio[1]):
        max = ratio[1]
    ratio = (int(1000.0 * ratio[0] / max), int(1000.0 * ratio[1] / max))
    self.image = pygame.transform.scale(self.image, ratio)
class Button:
  def __init__(self, onClick, onDrag, onClickOff, onScroll, enableDragOff):
    self.onClick = onClick
    self.onClickOff = onClickOff
    self.onDrag = onDrag
    self.onScroll = onScroll
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
    self.image = (pygame.image.tostring(self.image, 'RGBA'), self.image.get_size())
  for i in self.children:
    CopyHelp(i)

def CopyUnHelp(self):
  if(self.image != None):
    self.image = pygame.image.fromstring(self.image[0], self.image[1], 'RGBA')
  for i in self.children:
    CopyUnHelp(i)
def CopyHelp2(self):
  for att in dir(self):
    attObj = getattr(self, att)
    if(att[0] != "_"):
        attType = type(attObj)
        if(attType is not types.MethodType and attType is not list and attType is not type(None) and attType is not Object and attType is not pygame.Surface):
            attObj = copy.deepcopy(attObj)
  for i in self.children:
    CopyHelp2(i)
def Throw(self):
  if(self.destroyed):
    raise Exception("Object was destroyed")

