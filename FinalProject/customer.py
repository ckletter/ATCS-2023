import pygame
"Class for each customer, methods to update customer's order"
class Customer(pygame.sprite.Sprite):
    def __init__(self, order, image):
        # sets customer order
        self.order = order
        self.width = 120
        self.height = 160
        # initializes customer image
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = 270
        self.rect.y = 220
        self.drink = [None, None, None, None, None, None]
    def make_order(self):
        "returns user order"
        return self.order.return_order()
    def draw(self, screen):
        "draws customer on the screen"
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def add_flavor(self, flavor):
        "Adds flavor chosen to the customer order"
        self.drink[0] = flavor
    def add_topping(self, topping):
        "Adds topping to the customer's order"
        self.drink[5] = topping
    def add_milk(self, milk):
        "Adds milk chosen to the customer's order"
        self.drink[2] = milk
    def add_sweet(self, sweet):
        "adds sweet chosen to the customer's order"
        self.drink[3] = sweet
    def add_tea(self, tea):
        "add tea chosen to the customer's order"
        self.drink[1] = tea
    def add_ice(self, ice):
        self.drink[4] = ice
    def order_matches(self):
        "If the order made matches the order that the customer placed, returns True; else returns False"
        for i in range(len(self.order.order_list)):
            if self.order.order_list[i] != self.drink[i]:
                return False
        print(0)
        return True
