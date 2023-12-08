import pygame

class Customer(pygame.sprite.Sprite):
    def __init__(self, order, image):
        self.order = order
        self.width = 120
        self.height = 160
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = 270
        self.rect.y = 220

    def make_order(self):
        return self.order.return_order()
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))