import pygame
from classes import Square, Floor, Count, Text, InputBox, Button
pygame.init() # Starts pygame
pygame.display.set_caption('\"Pi Calculator\"?') # Sets the text at the top of the window

# Screen dimensions/pygame screen creation
dimensions = screenW, screenH = 1024, 576
screen = pygame.display.set_mode(dimensions)

# Global for timesteps/frame
timesteps = 15000

# Text/button objects
prompt = Text("Digits of pi to calculate: ", "Prototype.ttf", 32, screenW / 3, screenH / 2)
textbox = InputBox(screenW / 3 * 2, screenH / 2, 180, 40, "Prototype.ttf", 32)
prompt2 = Text("Press ENTER to start", "Prototype.ttf", 16, textbox.box.x + textbox.box.width / 2, textbox.box.y + 50)
menuButton = Button(screenW - 80, 5, 75, 30, "Menu", "Prototype.ttf", 16)
quitButton = Button(screenW / 2 - 75 / 2, 5, 75, 30, "Quit", "Prototype.ttf", 16)
count = Count("Prototype.ttf", 32, 5, 5)

# "Props"
floor = Floor(screenH - 50, screenW, screenH)
small = Square(x=screenW / 5, y=screenH - 50, width=50, mass=1)
large = Square(x=screenW / 2, y=screenH - 50, width=100, mass=1, vel=-1 / timesteps)

# Displays the main menu, where the game doesn't update and the user picks how many digits of pi to find
def menu():
    while True:
        screen.fill((180, 180, 180))
        
        # Check for quitting the game, button clicks, and keyboard input
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            if quitButton.checkClick(event):
                quit()
            textbox.checkClick(event)
            if textbox.active:
                count.digits = textbox.checkInput(event)

        # If digits is above 0 (aka updated by the textbox), setup/start the game
        # Running the game is equivalent to a sub-loop that the user chooses when to end
        if count.digits > 0:
            print(count.digits)
            textbox.active = False
            textbox.string = ""
            setup(count.digits, timesteps)
            loop()

        # Draw the elements of the menu
        drawMenu(screen)

# Game loop, plays out the square physics to calculate n digits of pi
def loop():
    while True:
        screen.fill((180, 180, 180))

        # Check for quitting the game and returning to the menu
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            if menuButton.checkClick(event):
                textbox.active = True
                count.digits = 0 # Reset the digits and count to 0, in preparation for the user to play again
                count.count = 0
                return

        # Do the following timesteps times, which is done to do things in incredibly small increments very fast
        for i in range(0, timesteps):
            # Update the square's positions
            small.update()
            large.update()
            # Check for collision between the squares, change velocities and increment count if there is one
            if small.collision(large):
                calcVelocity()
                count.increment()
            # If the small square has hit the wall, invert the velocity (wall has "infinite mass")
            if small.bounce(bound=-1):
                small.vel = -small.vel
                count.increment()

        # Draw the elements of the game
        draw(screen)

# Takes a screen variable and draws all the relevant game objects to that screen
def draw(s):
    floor.display(s)
    small.display(s)
    large.display(s, 0 + small.width)

    count.display(s)
    menuButton.display(s)

    pygame.display.flip()

# Takes a screen variable and draws all the relevant menu objects to that screen
def drawMenu(s):
    prompt.display(s)
    prompt2.display(s)
    textbox.display(s)
    quitButton.display(s)

    pygame.display.flip()

# Runs if a collision was found, calculates the new velocities of the squares
def calcVelocity():
    newVel1 = small.hit(large)
    newVel2 = large.hit(small)
    small.vel = newVel1
    large.vel = newVel2

# Runs at game start, calculates the mass of the large square based on the number of digits of pi required, sets the velocity to -1, sets the square's positions on the screen, and resets the count
def setup(n, t):
    large.mass = pow(100, n - 1) * small.mass
    large.x = screenW / 2
    large.vel = -1 / t
    small.x = screenW / 5
    small.vel = 0
    count.count = 0
    textbox.active = True

menu()