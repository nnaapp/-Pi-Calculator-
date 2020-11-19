import pygame

# Floor class, takes a y value and screen dimensions, fills the from the y value down on the screen with white
class Floor:
    def __init__(self, y, screenW, screenH):
        self.sprite = pygame.Rect(0, y, screenW, screenH)
    
    def display(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.sprite, width=0)

# Square class, does most of the visual/collision work
# Takes x, y, width, mass, and velocity values
class Square:
    def __init__(self, x, y, width, mass=1, vel=0):
        self.x = x
        y = y - width
        self.y = y
        self.width = width
        self.sprite = pygame.Rect(x, y, width, width)
        self.vel = vel
        self.mass = mass

    # Works since they will never go up or down, if the squares overlap at all return True
    def collision(self, other):
        return not self.x + self.width < other.x or self.x > other.x + other.width

    # Calculate the change in velocity for this square, works since the perfectly elastic equation is the same thing twice but with the subscript switched
    def hit(self, other):
        newVel = ((self.mass - other.mass) / (self.mass + other.mass) * self.vel) + ((2 * other.mass) / (self.mass + other.mass) * other.vel)
        return newVel

    # Bounce off the "wall", invert the velocity as its conceptual mass is infinite
    def bounce(self, bound):
        return self.x <= bound

    # Change the x based on the current velocity
    def update(self):
        self.x = self.x + self.vel

    # Display the sprite within the bounds set for it
    def display(self, screen, bound=-1):
        if self.x > bound:
            self.sprite.x = self.x
        else:
            self.sprite.x = bound
        pygame.draw.rect(screen, (100, 151, 213), self.sprite, width=0)

# Displays a labelled count of the number of collisions, aka the digits of pi
# Takes a font, fontsize, x, y, and optional color defaulting to black
class Count:
    def __init__(self, font, fontsize, x, y, digits=0, color=(0, 0, 0)):
        self.count = 0
        self.digits = digits
        self.font = pygame.font.Font(font, fontsize)
        self.text = self.font.render("Digits of pi (no decimal) : " + str(self.count), True, color)
        self.Rect = self.text.get_rect()
        self.Rect.x = x
        self.Rect.y = y
    
    # Add 1 to the count
    def increment(self):
        self.count = self.count + 1

    # Render the text after updating it to reflect the current count
    def display(self, screen):
        self.text = self.font.render("Digits of pi (no decimal) : " + str(self.count), True, (0, 0, 0))
        screen.blit(self.text, self.Rect)

# Display static colored text, with a font, at the given x and y values
class Text:
    def __init__(self, text, font, fontsize, x, y, color=(0, 0, 0)):
        self.font = pygame.font.Font(font, fontsize)
        self.text = self.font.render(text, True, color)
        self.Rect = self.text.get_rect()
        self.Rect.center = (x, y)

    def display(self, screen):
        screen.blit(self.text, self.Rect)

# Text input box, takes an x, y, width, height, font, fontsize, and optional color
# Starts "active", meaning any key the user presses will be added to the text, if the user clicks off it or starts the game, it will be "inactive"
# Limited to 2 characters to save the user from themself
class InputBox:
    def __init__(self, x, y, width, height, font, fontsize, color=(0, 0, 0)):
        self.box = pygame.Rect(0, 0, width, height)
        self.box.center = (x, y)
        self.color = color
        self.active = True

        self.font = pygame.font.Font(font, fontsize)
        self.string = ""
        self.text = self.font.render(self.string, True, color)
        self.textRect = pygame.Rect(self.box.left + self.box.width / 2 - fontsize, self.box.top, self.box.width, self.box.height)

    # If any event in the given list of events is MOUSEBUTTONDOWN, set the state of the textbox according to mouse position (checking overlap)
    def checkClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

    # If any event in the given list of events is a key press, perform the associated action
    # Continue/delete one/type a number
    def checkInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return int(self.string)
            elif event.key == pygame.K_BACKSPACE:
                self.string = self.string[:-1]
            elif len(self.string) < 2 and event.unicode.isdigit():
                self.string = self.string + event.unicode   

        return 0    

    # Update the text and display both it and the rectangle
    def display(self, screen):
        self.text = self.font.render(self.string, True, self.color)
        screen.blit(self.text, self.textRect)
        pygame.draw.rect(screen, self.color, self.box, width=2)

# Simple button, takes x, y, width, height, text, font, fontsize, and an optional color value
# Creates a rectangle with text based on the inputs, returns true if there was a click event and the mouse overlaps the rectangle
class Button:
    def __init__(self, x, y, width, height, text, font, fontsize, color=(0, 0, 0)):
        self.sprite = pygame.Rect(x, y, width, height)
        self.color = color

        self.font = pygame.font.Font(font, fontsize)
        self.text = self.font.render(text, True, color)
        self.textRect = self.text.get_rect()
        self.textRect.center = self.sprite.center

    def display(self, screen):
        pygame.draw.rect(screen, self.color, self.sprite, width=2)
        screen.blit(self.text, self.textRect)

    # Checks for click events, return true if the mouse overlaps the rectangle
    def checkClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.sprite.collidepoint(event.pos):
                return True