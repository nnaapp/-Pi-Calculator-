import pygame
from classes import Square, Floor, Count, Text, InputBox, Button
pygame.init()
pygame.display.set_caption('\"Pi Calculator\"?')

dimensions = screenW, screenH = 1024, 576
screen = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()

digits = 0
timesteps = 15000

prompt = Text("Digits of pi to calculate: ", "Prototype.ttf", 32, screenW / 3, screenH / 2)
textbox = InputBox(screenW / 3 * 2, screenH / 2, 180, 40, "Prototype.ttf", 32)
menuButton = Button(screenW - 80, 5, 75, 30, "Menu", "Prototype.ttf", 16)
quitButton = Button(screenW / 2 - 80, 5, 75, 30, "Quit", "Prototype.ttf", 16)

floor = Floor(screenH - 50, screenW, screenH)
small = Square(x=screenW / 5, y=screenH - 50, width=50, mass=1)
large = Square(x=screenW / 2, y=screenH - 50, width=100, mass=1, vel=-1 / timesteps)
count = Count("Prototype.ttf", 32, 5, 5)

def menu():
    while True:
        screen.fill((180, 180, 180))
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
        
        if quitButton.checkClick(events):
            quit()
        
        textbox.checkClick(events)
        if textbox.active:
            digits = textbox.checkInput(events)

        if digits > 0:
            textbox.active = False
            textbox.string = ""
            setup(digits, timesteps)
            loop()

        drawMenu(screen)


def loop():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
        
        if menuButton.checkClick(events):
            digits = 0
            count.count = 0
            break

        screen.fill((180, 180, 180))

        for i in range(0, timesteps):
            small.update()
            large.update()
            if small.collision(large):
                calcVelocity()
                count.increment()

            if small.bounce(bound=-1):
                small.vel = -small.vel
                count.increment()

        draw(screen)

def draw(s):
    floor.display(s)
    small.display(s)
    large.display(s, 0 + small.width)

    count.display(s)
    menuButton.display(s)

    pygame.display.flip()

def drawMenu(s):
    prompt.display(s)
    textbox.display(s)
    quitButton.display(s)

    pygame.display.flip()

def calcVelocity():
    newVel1 = small.hit(large)
    newVel2 = large.hit(small)
    small.vel = newVel1
    large.vel = newVel2

def setup(n, t):
    large.mass = pow(100, n - 1) * small.mass
    large.x = screenW / 2
    large.vel = -1 / t
    small.x = screenW / 5
    small.vel = 0
    count.count = 0
    textbox.active = True


menu()