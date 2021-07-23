import pygame

class Button():
    def __init__(self, x, y, width, height, color, textcolor, text=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.textcolor = textcolor
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        if self.text:
            font = pygame.font.SysFont("comicsans", 35)
            text = font.render(self.text, 1, self.textcolor)
            win.blit(text, (self.x+(self.width-text.get_width())/2, self.y+(self.height-text.get_height())/2))

    def clicked(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False



