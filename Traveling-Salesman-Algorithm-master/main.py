import pygame
import time
from point import *
from manager import *
from random import randint
from UI.setup import *
from utils import SumDistance
from ant import *
import sys
import datetime


sys.setrecursionlimit(8192)


pygame.init()

manager = Manager()

selectedIndex = 2

pause = True
started = False
rightMouseClicked = False
GenerateToggle = False
reset = False
PauseButton.state = pause
ResetButton.state = reset
RandomButton.state = GenerateToggle
timeLastCheck = time.time()
timeIteration = []
fileWrited = False
showUI = True
run = True
selectedIndex = 0
manager.RandomPoints()
manager.ResetGraph()
while run:
    manager.Background()

    delta_time = manager.SetFps()
    manager.UpdateCaption()

    # handle Events
    for event in pygame.event.get():
        #end game
        if event.type == pygame.QUIT:
            run = False
        
        # key down
        if event.type == pygame.KEYDOWN:
            # end game
            if event.key == pygame.K_ESCAPE:
                run = False
            
            # play / pause
            if event.key == pygame.K_SPACE:
                pause = not pause
                started = True

        # mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rightMouseClicked = True

    allowAlgoNextStep = not(pause) and manager.counter < iterations

    #Algo selection
    if selectedIndex == 0:
        if (allowAlgoNextStep):
            manager.BruteForce()
        if (n <= 100):
            manager.DrawShortestPath()
    elif selectedIndex == 1:
        if (allowAlgoNextStep):
            manager.GeneticAlgorithm()
        
        if (n<=100):
            manager.DrawShortestPath()
    else:
        if (allowAlgoNextStep):
            manager.AntColonyOptimization()
            if (n <= 100):
                manager.antColony.Draw(manager)
        elif(n<=100) :
            manager.DrawShortestPath()
    
# Updating telemetry
    if (allowAlgoNextStep):
        manager.counter+=1
        t = time.time() - timeLastCheck
        manager.timePassed+=t
        timeIteration.append(t)
    timeLastCheck = time.time()

#Saving result
    if (manager.counter >= iterations and not(fileWrited)):
        WriteFile(manager,selectedIndex,slider.value/1000,timeIteration)
        fileWrited = True

    if (n <= 100):
        manager.DrawPoints()
    if (len(timeIteration)==0):
        manager.ShowText(selectedIndex, started,slider.value/1000,float("nan"))
    else:
        manager.ShowText(selectedIndex, started,slider.value/1000,sum(timeIteration)/len(timeIteration))
    manager.Percentage()

# UI
    panel.Render(manager.screen)
    AlgorithmChoice.Render(manager.screen, rightMouseClicked)
    if pause != PauseButton.state:
        PauseButton.state = pause

    PauseButton.Render(manager.screen, rightMouseClicked)
    ResetButton.Render(manager.screen, rightMouseClicked)
    RandomButton.Render(manager.screen, rightMouseClicked)

#Activ Constarinte
    if (IsConstraintBtn.state):
        IsConstraintBtn.color = (252,192,0)
        IsConstraintBtn.text = "OFF"
        manager.ResetAntColony(False)
    else:
        IsConstraintBtn.color = (75,87,95)
        IsConstraintBtn.text = "ON"
        slider.Render(manager.screen)
        manager.ResetAntColony(True)

    IsConstraintBtn.Render(manager.screen, rightMouseClicked)
    



    pause = PauseButton.state
    reset = ResetButton.state
    btnStateConstraint = IsConstraintBtn.state

#RESET Button
    if reset == True:
        reset = False
        ResetButton.state = False
        fileWrited = False
        timeIteration = []
        manager.ResetGraph()
    

    GenerateToggle = RandomButton.state
    if GenerateToggle == True:
        manager.RandomPoints()
        GenerateToggle = False
        RandomButton.state = False

    if pause == True:
        PauseButton.text = "Continue"
    else:
        PauseButton.text = "Pause"
        

    if rightMouseClicked:
        selectedIndex = AlgorithmChoice.currentIndex


    # point scale animation increment
    manager.scaler += 1
    if manager.scaler > manager.max_radius:
        manager.scaler = manager.max_radius

    pygame.display.flip()
    rightMouseClicked = False

#save file
WriteFile(manager,selectedIndex,slider.value/1000,timeIteration)
fileWrited = True

pygame.quit()
