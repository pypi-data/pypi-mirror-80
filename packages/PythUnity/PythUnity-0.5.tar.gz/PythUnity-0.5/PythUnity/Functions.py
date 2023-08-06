from PythUnity import Variables
import pygame
def AddObject(image):
  Variables.parts.append(image)
  index = len(Variables.parts) - 1
  Variables.parts[index].index = index
  return index

#def AddObjects(images):
#  indexes = []
#  for i in images:
#    indexes.append(AddObject(i))
#  return indexes

def AddPrefab(name, obj):
  newObj = obj.Copy()
  newObj.Destroy() #need to remove prefab from child list
  newObj.destroyed = False #so prefab doesnt load destroyed
  newObj.parent = None
  Variables.prefabs[name] = newObj
def GetPrefab(name):
  newObj = Variables.prefabs[name].Copy()
  newObj.Move(len(newObj.GetParentChildren()))
  return newObj
def PrintFonts():
  fonts = pygame.font.get_fonts() 
  for i in fonts:
    print(i)

