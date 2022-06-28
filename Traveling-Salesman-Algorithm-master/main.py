import pygame
import time
from point import *
from manager import *
from random import randint
from UI.setup import *
from utils import SumDistance


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
        manager.DrawShortestPath()
    elif selectedIndex == 1:
        if (allowAlgoNextStep):
            manager.GeneticAlgorithm()
        manager.DrawShortestPath()
    else:
        if (allowAlgoNextStep):
            manager.AntColonyOptimization()
            manager.antColony.Draw(manager)
        else :
            manager.DrawShortestPath()
    
    # Updating telemetry
    if (allowAlgoNextStep):
        manager.counter+=1
        manager.timePassed+=time.time() - timeLastCheck
    timeLastCheck = time.time()

    manager.DrawPoints()
    manager.ShowText(selectedIndex, started,slider.value/1000)
    manager.Percentage()

    # UI
    panel.Render(manager.screen)
    AlgorithmChoice.Render(manager.screen, rightMouseClicked)
    if pause != PauseButton.state:
        PauseButton.state = pause

    PauseButton.Render(manager.screen, rightMouseClicked)
    ResetButton.Render(manager.screen, rightMouseClicked)
    RandomButton.Render(manager.screen, rightMouseClicked)
    slider.Render(manager.screen)

    pause = PauseButton.state
    reset = ResetButton.state

    if reset == True:
        reset = False
        ResetButton.state = False
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
pygame.quit()
