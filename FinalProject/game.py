from customer import Customer
from order import Order
from textbox import TextBox
import random
import pygame

class Game:
    FLAVORS = ["Mango", "Peach", "Strawberry", None]
    TEAS = ["Black", "Oolong", "Green"]
    MILKS = ["Whole Milk", "Skim Milk", None]
    SWEET_LEVELS = [0.25, 0.50, 0.75, 1]
    ICE_LVELS = [0.25, 0.50, 0.75, 1]
    TOPPINGS = ["Boba", "Lychee Jelly", "Crystal Boba", "Grass Jelly", None]
    def __init__(self):
        # Initialize Screen
        pygame.init()
        self.width, self.height = 800, 600
        self.window = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load("Images/bobashop.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.customer_image = pygame.image.load("Images/customer.png")
        self.running = True
        # Initialize font
        self.font = pygame.font.Font(None, 36)
        self.textbox_width = 500
        self.textbox_height = 90
        # Initialize time
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.customers = []
        self.customer_line = []
        for flavor in self.FLAVORS:
            for tea in self.TEAS:
                for milk in self.MILKS:
                    for sweet in self.SWEET_LEVELS:
                        for ice in self.ICE_LVELS:
                            for topping in self.TOPPINGS:
                                customer = Customer(Order(flavor, tea, milk, sweet, ice, topping), self.customer_image)
                                self.customers.append(customer)
        for i in range(10):
            index = random.randint(0, len(self.customers) - 1)
            self.customer_line.append(self.customers[index])

        self.current_customer = self.customer_line[0]

        self.new_customer_box = TextBox(100, 100, 200, 50, "GET CUSTOMER")
        self.make_order_box = TextBox(500, 100, 200, 50, "MAKE ORDER")

    def run(self):
        self.draw() 
        while self.running:
            self.handle_events()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button click
                    mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                    if self.current_customer.rect.collidepoint(mouse_pos):
                        print("clicked")
                    elif self.new_customer_box.rect.collidepoint(mouse_pos):
                        text_y = 150  # Starting position for displaying text
                        if len(self.customer_line) != 0:
                            text = self.current_customer.make_order()
                            text_1 = ""
                            text_2 = ""
                            if len(text) > 35:
                                new_text = text[35:]
                                index = new_text.index(" ") + 35
                                text_1 = text[:index]
                                text_2 = text[index + 1:]
                            text_1 = f"{text_1}"
                            text_2 = f"{text_2}"
                            textbox = pygame.Rect(100, text_y, self.textbox_width, self.textbox_height)
                            pygame.draw.rect(self.window, (0, 0, 0), textbox, 6)  # Draw a black text box
                            inner_box = pygame.Rect(105, text_y+5, self.textbox_width - 10, self.textbox_height - 10)
                            pygame.draw.rect(self.window, (255, 255, 255), inner_box)
                            text_surface1= self.font.render(text_1, True, (0, 0, 0))  # Render text in black
                            text_surface2 = self.font.render(text_2, True, (0, 0, 0))  # Render text in black
                            self.window.blit(text_surface1, (113.5, text_y + 5))  # Adjust position for text within the box
                            self.window.blit(text_surface2, (113.5, text_y + 35))  # Adjust position for text within the box
                            self.current_customer.draw(self.window)
                            pygame.display.flip()
                    click_x, click_y = mouse_pos
                    print(f"Clicked at X: {click_x}, Y: {click_y}")

    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.new_customer_box.draw(self.window)
        

if __name__ == "__main__":
    game = Game()
    game.run()