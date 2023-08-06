from PythUnity import Variables
from PythUnity import Functions
import copy
import pygame
import types
class Object:
  def __init__(self, rect, image, onClick = None, onDrag = None, onClickOff = None, onScroll = None, enableDragOff = False, clickGroup = 0):
    self.__destroyed = False
    self.__parent = None
    self.__children = []
    self.variables = {}
    self.__image = None
    self.text = None
    self.color = None
    self.__components = []
    self.clickGroup = clickGroup#not implemented yet
    self.velocity = (0, 0)
    if(type(image) is tuple):
      self.color = image
    elif(type(image) is String):
      self.text = copy.deepcopy(image)
    else:
      self.image = image
    self.rect = rect
    if onClick != None or onDrag != None or onScroll != None:
      self.button = Button(onClick, onDrag, onClickOff, onScroll, enableDragOff)
    else:
      self.button = None
    Functions.AddObject(self)
    for att in dir(self):
        print(att)
    print("////////////")
  #####
  @property
  def image(self):
    return self.__image
  @image.setter
  def image(self, value):
    self.__image = value
    ratio = self.__image.get_size()
    max = ratio[0]
    if(max < ratio[1]):
        max = ratio[1]
    ratio = (int(1000.0 * ratio[0] / max), int(1000.0 * ratio[1] / max))
    self.__image = pygame.transform.scale(self.__image, ratio)
  @property
  def destroyed(self):
    return self.__destroyed
  @destroyed.setter
  def destroyed(self, value):
    Err("Cant set Object.destroyed")
  @property
  def parent(self):
    return self.__parent
  @parent.setter
  def parent(self, value):
    Err("Cant set Object.parent")
  @property
  def children(self):
    return self.__children
  @children.setter
  def children(self, value):
    Err("Cant set Object.children")
  @property
  def components(self):
    return self.__components
  @components.setter
  def components(self, value):
    Err("Cant set Object.components, use Object.AddComp or Object.DelComp")
  #####
  def __getitem__(self, i):
    self.Throw("children.getitem")
    return self.__children[i]
  def __len__(self):
    self.Throw("children.len")
    return len(self.__children)
  #####
  def Decendants(self):
    self.Throw("Object.Decendants")
    indexes = []
    for i in self.__children:
      indexes.append(i)
      indexes.extend(Variables.parts[i].Decendants())
    return indexes
  def Move(self, newIndex):#components can have their update function skipped on accident if ran in another comp.update
    self.Throw("Object.Move")
    children = self.GetParentChildren()
    if(newIndex < 0):
        Err("Object.Move failed, index less than 0")
    elif(newIndex > len(children)):
        Warn("Object.Move incorrect, index is greater than parent.children count")
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
    self.Throw("Object.SetParent")
    children = self.GetParentChildren()
    self.Move(len(children))#make it so other children have their indexes fixed
    del children[self.index]
    self.__parent = newParent
    self.__parent.children.append(self)
    self.index = len(self.__parent.children) - 1
  def GetParentChildren(self):
    self.Throw("Object.GetParentChildren")
    children = None
    if(self.__parent != None):
      children = self.__parent.children
    else:
      children = Variables.parts
    return children
  def Copy(self):
    self.Throw("Object.Copy")
    CopyHelp(self)
    parChildren = self.GetParentChildren()
    copied = copy.deepcopy(self)
    copied.index = len(parChildren)
    parChildren.append(copied)
    copied.__parent = self.__parent
    copied.Move(self.index + 1)
    CopyUnHelp(self)
    CopyUnHelp(copied)
    CopyHelp2(copied)
    return copied
  def Destroy(self):
    self.Throw("Object.Destroy")
    children = self.GetParentChildren()
    self.Move(len(children))
    del children[self.index]
    self.index = -1 #will cause error if used incorrectly, did this on purpous
    self.__destroyed = True
    for i in self.__children:
      i.Destroy()
  def AddComp(self, comp):
    self.Throw("Object.AddComp")
    self.__components.append(comp)
    if(comp[0] != None):
        comp[0](self)
  def DelComp(self, index):
      self.Throw("Object.DelComp")
      if(len(self.__components) > index):
          del self.__components[index]
      else:
          Err("Object.DelComp failed, index greater than comp index")
  def Throw(self, action = ""):
    if(self.__destroyed):
      if(action == ""):
        Err("Object was destroyed")
      else:
        Err("Object was destroyed while " + action + "() was happening")
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
    self._Object__image = (pygame.image.tostring(self._Object__image, 'RGBA'), self._Object__image.get_size())
  for i in self.children:
    CopyHelp(i)

def CopyUnHelp(self):
  if(self._Object__image != None):
    self._Object__image = pygame.image.fromstring(self._Object__image[0], self._Object__image[1], 'RGBA')
  for i in self.children:
    CopyUnHelp(i)
def CopyHelp2(self):
  for att in dir(self):
    attObj = getattr(self, att)
    if(att[0] != "_" or att[1] == "O"):#if its a _Object__ atribute still copy
        attType = type(attObj)
        if(attType is not types.MethodType and attType is not list and attType is not type(None) and attType is not Object and attType is not pygame.Surface):
            attObj = copy.deepcopy(attObj)
  for i in self.children:
    CopyHelp2(i)

def Err(text):
    raise Exception("PythUnity: " + text)
def Warn(text):
    raise RuntimeWarning("PythUnity: " + text)