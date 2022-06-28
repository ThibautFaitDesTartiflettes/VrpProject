from UI.ui import *
from manager import width, height

panel = Panel()

PauseButton = Button("Pause", (width - 270, 180), 150, 50, 0, (10, 10, 30), (255, 255, 255))
ResetButton = Button("Reset", (width - 270, 240), 150, 50, 0, (10, 10, 30), (255, 255, 255))
RandomButton = Button("Generate", (width - 270, 300), 150, 50, 0, (10, 10, 30), (255, 255, 255))
slider = Slider(width - 270-200, 50, 500, 0, 1, 200, 25,1000)

AlgorithmChoice = DropDownButton("Select", (width - 350, 400), 300, 50, 4, 2, (10, 10, 30), (255, 255, 255))
AlgorithmChoice.childs[0].text = "Brute Force"
AlgorithmChoice.childs[1].text = "Genetic Algorithm"
AlgorithmChoice.childs[2].text = "Ant Colony Algorithm"
AlgorithmChoice.childs[3].text = "!Shortest Neighbourg!"
AlgorithmChoice.currentIndex = 0
