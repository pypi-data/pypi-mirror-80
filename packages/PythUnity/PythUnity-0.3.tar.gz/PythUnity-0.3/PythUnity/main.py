import pygame
import copy 
import Classes
import Variables
import Functions
from datetime import datetime
def init():
  pygame.init()
  #Screen######
  width, height = 800,  600
  global backgroundColor
  global screen
  backgroundColor = 255, 255, 255
  screen = pygame.display.set_mode((width, height))
  #############

  #FUNCTIONS##################
  def Touching(rect, pos):
    return rect.left+rect.width > pos[0] > rect.left and rect.top+rect.height > pos[1] > rect.top
  ############################
  for i in Variables.starts:
    i()#run start
  ###VARIABLES##########
  global mouse
  mouse = (0, 0)
  mousePressed = False
  mouseDragging = False
  #########################################

  #MAIN FUNCTION###########################
  def MainFunction(i, offset):
    #SET RECT##############################
      rect = None
      if(not(i.text is None)):
        font = pygame.font.Font(i.text.font + ".ttf", i.text.fontSize) 
        text = font.render(i.text.text, True, i.text.fontColor, i.text.backgroundColor)
        rect = font.size((i.text.text))
        rect = pygame.Rect(i.rect[0], i.rect[1], rect[0], rect[1])
        rect.left = rect.left + offset[0]
        rect.top = rect.top + offset[1]
        #print(rect)
        screen.blit(text, rect)
      elif(not(i.image is None)):
        rect = copy.deepcopy(i.rect)
        rect.left = rect.left + offset[0]
        rect.top = rect.top + offset[1]
        screen.blit(i.image, rect)
      else:
        rect = copy.deepcopy(i.rect)
        rect.left = rect.left + offset[0]
        rect.top = rect.top + offset[1]
        pygame.draw.rect(screen, i.color, rect)
      ########################################
      #RUN BUTTON PRESSES#####################
      if i.button != None:
        hovering = Touching(rect, mouse)
        touching = mousePressed and hovering
        if(touching):
          if(i.button.onClick != None):
            i.button.onClick(i)
          i.button.dragging = True
        elif(i.button.dragging and (hovering or i.button.enableDragOff) and mouseDragging):
          if(i.button.onDrag != None):
            i.button.onDrag(i)
        elif((not hovering and not i.button.enableDragOff) or not mouseDragging):
          if(i.button.onClickOff != None and i.button.dragging == True):
            i.button.onClickOff(i)
          i.button.dragging = False
      ########################################

      #RUN COMPONENT Updates#########################
      for iComp in i.components:
        if(iComp[1] != None):
          iComp[1](i)
      for iChild in i.children:
        MainFunction(iChild, (rect.left, rect.top))
      ########################################
  #########################################

  while True:
    startTime = datetime.now()#Set Start Time
    #GetMousePos##############################
    mousePressed = False
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN: 
        mouse = pygame.mouse.get_pos()
        mousePressed = True;
        mouseDragging = True
      elif event.type == pygame.MOUSEBUTTONUP:
        mouseDragging = False
    ##########################################
    screen.fill(backgroundColor)
    for i in Variables.parts:
      MainFunction(i, (0, 0))
    Variables.deltaTime = (datetime.now()-startTime).total_seconds()#Set DeltaTime
    pygame.display.flip()
  #################