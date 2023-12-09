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
        self.drink = [None, None, None, None, None, None]

    def make_order(self):
        return self.order.return_order()
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def add_flavor(self, flavor):
        self.drink[0] = flavor
    def add_topping(self, topping):
        self.drink[5] = topping
    def add_milk(self, milk):
        self.drink[2] = milk
    def add_sweet(self, sweet):
        self.drink[3] = sweet
    def add_tea(self, tea):
        self.drink[1] = tea
    def add_ice(self, ice):
        self.drink[4] = ice
    def order_matches(self):
        for i in range(len(self.order.order_list)):
            if self.order.order_list[i] != self.drink[i]:
                return False
        print(0)
        return True
