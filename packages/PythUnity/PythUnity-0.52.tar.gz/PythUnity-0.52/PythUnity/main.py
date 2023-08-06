import pygame
import copy 
from PythUnity import Classes
from PythUnity import Variables
from PythUnity import Functions
from datetime import datetime
def init():
  pygame.init()
  #Screen######
  global screen
  screen = pygame.display.set_mode(Variables.screenRect)
  #############

  #FUNCTIONS##################
  def Touching(rect, pos):
    return rect.left+rect.width > pos[0] > rect.left and rect.top+rect.height > pos[1] > rect.top
  ############################
  for i in Variables.starts:
    i()#run start
  ###VARIABLES##########
  mousePressed = (False, "")
  mouseScrolling = (False, 0)
  mouseUp = ""
  global clicked
  clicked = []
  #########################################

  #MAIN FUNCTION###########################
  def MainFunction(i, offset):
    #SET RECT##############################
      rect = None
      if(not(i.text is None)):
        font = pygame.font.Font(i.text.font + ".ttf", i.text.fontSize) 
        text = font.render(i.text.text, True, i.text.fontColor, i.text.backgroundColor)
        rect = font.size((i.text.text))
        rect = pygame.Rect(i.rect[0] + offset[0], i.rect[1] + offset[1], rect[0], rect[1])
        #print(rect)
        screen.blit(text, rect)
      elif(not(i.image is None)):
        rect = copy.deepcopy(i.rect)
        rect.left = rect.left + offset[0]
        rect.top = rect.top + offset[1]
        ratio = i.image.get_size()
        ratio = (int(ratio[0] / 1000.0 * rect.width), int(ratio[1] / 1000.0 * rect.height))
        image = pygame.transform.scale(i.image, ratio)
        screen.blit(image, rect)
      else:
        rect = copy.deepcopy(i.rect)
        rect.left = rect.left + offset[0]
        rect.top = rect.top + offset[1]
        if(len(i.color) == 3):
          pygame.draw.rect(screen, i.color, rect)
        elif(len(i.color) == 4):
          s = pygame.Surface((i.rect.width, i.rect.height))
          s.set_alpha(i.color[3])
          s.fill((i.color[0], i.color[1], i.color[2]))
          screen.blit(s, (i.rect.left, i.rect.top))
        elif(len(i.color) != 0):
          raise ValueError("Object has invalid color can be in formats: RGB and RGBA, or as ()")
      ########################################
      #RUN BUTTON PRESSES#####################
      hovering = Touching(rect, Variables.mousePosition)
      if(hovering):
        clicked.insert(0, i)
      if i.button != None:
        touching = mousePressed[0] and hovering
        if(touching):
          if(i.button.onClick != None):
            i.button.onClick(i, mousePressed[1])
          i.button.dragging = True
        elif(mouseScrolling[0] and not i.button.dragging and hovering):
            if(i.button.onScroll != None):
                i.button.onScroll(i, mouseScrolling[1])
        elif(i.button.dragging and (hovering or i.button.enableDragOff) and Variables.mouseDragging):
          if(i.button.onDrag != None):
            i.button.onDrag(i)
        elif((not hovering and not i.button.enableDragOff) or not Variables.mouseDragging):
          if(i.button.onClickOff != None and i.button.dragging == True):
            i.button.onClickOff(i, mouseUp)
          i.button.dragging = False
      ########################################

      #RUN COMPONENT Updates#########################
      for iComp in i.components:
        if(iComp[1] != None):
          iComp[1](i)
      for iChild in i.children:
        MainFunction(iChild, (rect.left, rect.top))
      i.rect.left = i.rect.left + i.velocity[0] * Variables.deltaTime
      i.rect.top = i.rect.top + i.velocity[1] * Variables.deltaTime
      ########################################
  #########################################

  while True:
    startTime = datetime.now()#Set Start Time
    #GetMousePos##############################
    mousePressed = (False, "")
    mouseScrolling = (False, 0)
    mouseUp = ""
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN: 
        if event.button == 1:
            Variables.mousePosition = pygame.mouse.get_pos()
            mousePressed = (True, "Left")
            Variables.mouseDragging = True
        elif event.button == 3:
            Variables.mousePosition = pygame.mouse.get_pos()
            mousePressed = (True, "Right")
            Variables.mouseDragging = True
        elif event.button == 2:
            Variables.mousePosition = pygame.mouse.get_pos()
            mousePressed = (True, "Middle")
            Variables.mouseDragging = True
        elif event.button == 5:
            mouseScrolling = (True, mouseScrolling[1] + 1)
        elif event.button == 4:
            mouseScrolling = (True, mouseScrolling[1] - 1)
      elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            mouseUp = "Left"
        elif event.button == 3:
            mouseUp = "Right"
        elif event.button == 2:
            mouseUp = "Middle"
        Variables.mouseDragging = False
      elif event.type == pygame.MOUSEMOTION:
        Variables.oldMousePosition = Variables.mousePosition
        Variables.mousePosition = event.pos
    ##########################################
    screen.fill(Variables.backgroundColor)
    for i in Variables.parts:
      MainFunction(i, (0, 0))
    Variables.deltaTime = (datetime.now()-startTime).total_seconds()#Set DeltaTime
    pygame.display.flip()
  #################