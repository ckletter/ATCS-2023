import pygame

class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text=None, fontSize = 32):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.fontSize = fontSize
        self.text = text  # Placeholder for the text in the box

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)  # Drawing the outline of the box
        inner_box = pygame.Rect(self.rect.x+2, self.rect.y+2, self.width - 4, self.height - 4)
        pygame.draw.rect(screen, (255, 255, 255), inner_box)
        font = pygame.font.Font(None, self.fontSize)  # You can change the font and size here
        text_surface = font.render(self.text, True, (0, 0, 0))  # Render the text surface
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  # Display the text within the box