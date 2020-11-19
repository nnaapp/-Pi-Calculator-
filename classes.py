import pygame

class Floor:
    def __init__(self, y, screenW, screenH):
        self.sprite = pygame.Rect(0, y, screenW, screenH)
    
    def display(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.sprite, width=0)

class Square:
    def __init__(self, x, y, width, mass, vel=0):
        self.x = x
        y = y - width
        self.y = y
        self.width = width
        self.sprite = pygame.Rect(x, y, width, width)
        self.vel = vel
        self.mass = mass

    def collision(self, other):
        return not self.x + self.width < other.x or self.x > other.x + other.width

    def hit(self, other):
        newVel = ((self.mass - other.mass) / (self.mass + other.mass) * self.vel) + ((2 * other.mass) / (self.mass + other.mass) * other.vel)
        return newVel

    def bounce(self, bound):
        return self.x <= bound

    def update(self):
        self.x = self.x + self.vel

    def display(self, screen, bound=-1):
        if self.x > bound:
            self.sprite.x = self.x
        else:
            self.sprite.x = bound
        pygame.draw.rect(screen, (100, 151, 213), self.sprite, width=0)

class Count:
    def __init__(self, font, fontsize, x, y, color=(0, 0, 0)):
        self.count = 0
        self.font = pygame.font.Font(font, fontsize)
        self.text = self.font.render("Digits of pi (no decimal) : " + str(self.count), True, color)
        self.Rect = self.text.get_rect()
        self.Rect.x = x
        self.Rect.y = y
    
    def increment(self):
        self.count = self.count + 1

    def display(self, screen):
        self.text = self.font.render("Digits of pi (no decimal) : " + str(self.count), True, (0, 0, 0))
        screen.blit(self.text, self.Rect)

class Text:
    def __init__(self, text, font, fontsize, x, y, color=(0, 0, 0)):
        self.font = pygame.font.Font(font, fontsize)
        self.text = self.font.render(text, True, color)
        self.Rect = self.text.get_rect()
        self.Rect.center = (x, y)

    def display(self, screen):
        screen.blit(self.text, self.Rect)

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

    def checkClick(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.box.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

    def checkInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return int(self.string)
                elif event.key == pygame.K_BACKSPACE:
                    self.string = self.string[:-1]
                elif len(self.string) < 2:
                    self.string = self.string + event.unicode   

        return 0    

    def display(self, screen):
        self.text = self.font.render(self.string, True, self.color)
        screen.blit(self.text, self.textRect)
        pygame.draw.rect(screen, self.color, self.box, width=2)

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

    def checkClick(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.sprite.collidepoint(event.pos):
                    return True