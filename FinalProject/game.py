from customer import Customer
from order import Order
from textbox import TextBox
import random
import pygame
from fsm import FSM

class Game:
    # Constants for customizations
    FLAVORS = ["Mango", "Peach", "Strawberry", None]
    TEAS = ["Black", "Oolong", "Green"]
    MILKS = ["Whole Milk", "Skim Milk", None]
    SWEET_LEVELS = ["25%", "50%", "75%", "100%"]
    ICE_LEVELS = ["25%", "50%", "75%", "100%"]
    TOPPINGS = ["Boba", None]
    # Constants for states
    NO_ORDER, ORDER_PLACED, MAKE_ORDER, CHOOSE_FLAVOR, CHOOSE_MILK, CHOOSE_SWEET, CHOOSE_ICE, CHOOSE_TEA, ORDER_SHOWN = range(9)
    # Constants for all user inputs (mouse clicks on text boxes)
    NEW_CUSTOMER, NEW_FLAVOR, CHOOSE_SEE_ORDER, NEW_MILK, NEW_ICE, NEW_SWEET, NEW_TEA, NEW_TOPPING, WHOLE_MILK_CHOSEN, SKIM_MILK_CHOSEN, NO_MILK_CHOSEN = "nc", "nf", "cso", "nm", "ni", "ns", "ntea", "nt", "wmc", "smc", "nmc"
    LIGHT_SWEET_CHOSEN, HALF_SWEET_CHOSEN, LESS_SWEET_CHOSEN, FULL_SWEET_CHOSEN, STRAWBERRY_CHOSEN, MANGO_CHOSEN, PEACH_CHOSEN = "lsc", "hsc", "lesc", "fsc", "sc", "mc", "pc"
    OOLONG_CHOSEN, BLACK_CHOSEN, GREEN_CHOSEN, LIGHT_ICE_CHOSEN, HALF_ICE_CHOSEN, LESS_ICE_CHOSEN, FULL_ICE_CHOSEN = "oc", "bc", "gc", "lic", "hic", "leic", "fic"
    def __init__(self):
        # Initialize Screen - Generated by ChatGPT
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
        self.textbox_height = 95
        self.customer_line = []
        # Generate 10 random customers
        for i in range(5):
            flavor_index = random.randint(0, len(self.FLAVORS) - 1)
            tea_index = random.randint(0, len(self.TEAS) - 1)
            milk_index = random.randint(0, len(self.MILKS) - 1)
            sweet_index = random.randint(0, len(self.SWEET_LEVELS) - 1)
            ice_index = random.randint(0, len(self.ICE_LEVELS) - 1)
            topping_index = random.randint(0, len(self.TOPPINGS) - 1)
            customer = Customer(Order(self.FLAVORS[flavor_index], self.TEAS[tea_index], self.MILKS[milk_index], self.SWEET_LEVELS[sweet_index], self.ICE_LEVELS[ice_index], self.TOPPINGS[topping_index]), self.customer_image)
            self.customer_line.append(customer)
        self.current_customer = self.customer_line[0]
        self.order = self.current_customer.make_order()
        self.orders_completed = 0
        # Initialize Text Boxes
        self.new_customer_box = TextBox(25, 50, 300, 45, "NEW CUSTOMER", 50)
        self.make_order_box = TextBox(500, 100, 200, 50, "MAKE ORDER")
        self.boba_box = TextBox(680, 400, 120, 45, "ADD BOBA", 30)
        self.flavor_box = TextBox(600, 200, 180, 45, "CHOOSE FLAVOR", 30)
        self.milk_box = TextBox(100, 400, 160, 45, "CHOOSE MILK", 30)
        self.sweet_box = TextBox(480, 400, 180, 45, "CHOOSE SWEET", 30)
        self.ice_box = TextBox(280, 400, 180, 45, "CHOOSE ICE", 30)
        self.tea_box = TextBox(50, 300, 160, 45, "CHOOSE TEA", 30)
        # Initialize Customization Text Boxes
        self.mango = TextBox(25, 100, 200, 55, "MANGO", 50)
        self.peach = TextBox(275, 100, 200, 55, "PEACH", 50)
        self.strawberry = TextBox(525, 100, 245, 55, "STRAWBERRY", 50)
        self.whole_milk = TextBox(50, 100, 230, 55, "WHOLE MILK", 50)
        self.skim_milk = TextBox(300, 100, 190, 55, "SKIM MILK", 50)
        self.no_milk = TextBox(520, 100, 150, 55, "NO MILK", 50)
        self.black = TextBox(25, 100, 200, 55, "BLACK", 50)
        self.green = TextBox(275, 100, 200, 55, "GREEN", 50)
        self.oolong = TextBox(525, 100, 245, 55, "OOLONG", 50)
        self.light_sweet = TextBox(50, 100, 75, 55, "25%", 50)
        self.half_sweet = TextBox(150, 100, 75, 55, "50%", 50)
        self.less_sweet = TextBox(250, 100, 75, 55, "75%", 50)
        self.full_sweet = TextBox(350, 100, 90, 55, "100%", 50)
        self.light_ice = TextBox(50, 100, 75, 55, "25%", 50)
        self.half_ice = TextBox(150, 100, 75, 55, "50%", 50)
        self.less_ice = TextBox(250, 100, 75, 55, "75%", 50)
        self.full_ice = TextBox(350, 100, 75, 55, "100%", 50)
        self.see_order = TextBox(25, 50, 230, 45, "SEE ORDER", 50)
        # Initialize the game's FSM
        self.fsm = FSM(self.NO_ORDER)
        self.init_fsm()
    def init_fsm(self):
        # Choose customizations from order placed screen
        self.fsm.add_transition(self.NEW_TOPPING, self.ORDER_PLACED, self.add_boba, None)
        self.fsm.add_transition(self.NEW_CUSTOMER, self.NO_ORDER, self.display_new_customer, self.ORDER_PLACED)
        self.fsm.add_transition(self.NEW_SWEET, self.ORDER_PLACED, self.display_sweet_selections, self.CHOOSE_SWEET)
        self.fsm.add_transition(self.NEW_ICE, self.ORDER_PLACED, self.display_ice_selections, self.CHOOSE_ICE)
        self.fsm.add_transition(self.NEW_FLAVOR, self.ORDER_PLACED, self.display_flavor_selections, self.CHOOSE_FLAVOR)
        self.fsm.add_transition(self.NEW_TEA, self.ORDER_PLACED, self.display_tea_selections, self.CHOOSE_TEA)
        self.fsm.add_transition(self.NEW_MILK, self.ORDER_PLACED, self.display_milk_selections, self.CHOOSE_MILK)
        # Choose milk options from choose milk screen
        self.fsm.add_transition(self.WHOLE_MILK_CHOSEN, self.CHOOSE_MILK, self.choose_whole_milk, self.ORDER_PLACED)
        self.fsm.add_transition(self.SKIM_MILK_CHOSEN, self.CHOOSE_MILK, self.choose_skim_milk, self.ORDER_PLACED)
        self.fsm.add_transition(self.NO_MILK_CHOSEN, self.CHOOSE_MILK, self.choose_no_milk, self.ORDER_PLACED)
        # Choose flavor options from choose flavor screen
        self.fsm.add_transition(self.STRAWBERRY_CHOSEN, self.CHOOSE_FLAVOR, self.choose_strawberry, self.ORDER_PLACED)
        self.fsm.add_transition(self.PEACH_CHOSEN, self.CHOOSE_FLAVOR, self.choose_peach, self.ORDER_PLACED)
        self.fsm.add_transition(self.MANGO_CHOSEN, self.CHOOSE_FLAVOR, self.choose_mango, self.ORDER_PLACED)
        # Choose tea options from choose tea screen
        self.fsm.add_transition(self.BLACK_CHOSEN, self.CHOOSE_TEA, self.choose_black, self.ORDER_PLACED)
        self.fsm.add_transition(self.GREEN_CHOSEN, self.CHOOSE_TEA, self.choose_green, self.ORDER_PLACED)
        self.fsm.add_transition(self.OOLONG_CHOSEN, self.CHOOSE_TEA, self.choose_oolong, self.ORDER_PLACED)
        # Choose ice options from choose ice screen
        self.fsm.add_transition(self.LIGHT_ICE_CHOSEN, self.CHOOSE_ICE, self.choose_light_ice, self.ORDER_PLACED)
        self.fsm.add_transition(self.HALF_ICE_CHOSEN, self.CHOOSE_ICE, self.choose_half_ice, self.ORDER_PLACED)
        self.fsm.add_transition(self.LESS_ICE_CHOSEN, self.CHOOSE_ICE, self.choose_less_ice, self.ORDER_PLACED)
        self.fsm.add_transition(self.FULL_ICE_CHOSEN, self.CHOOSE_ICE, self.choose_full_ice, self.ORDER_PLACED)
        # Choose sweet options from choose sweet screen
        self.fsm.add_transition(self.LIGHT_SWEET_CHOSEN, self.CHOOSE_SWEET, self.choose_light_sweet, self.ORDER_PLACED)
        self.fsm.add_transition(self.HALF_SWEET_CHOSEN, self.CHOOSE_SWEET, self.choose_half_sweet, self.ORDER_PLACED)
        self.fsm.add_transition(self.LESS_SWEET_CHOSEN, self.CHOOSE_SWEET, self.choose_less_sweet, self.ORDER_PLACED)
        self.fsm.add_transition(self.FULL_SWEET_CHOSEN, self.CHOOSE_SWEET, self.choose_full_sweet, self.ORDER_PLACED)
        # Allow player to see the order placed again
        self.fsm.add_transition(self.CHOOSE_SEE_ORDER, self.ORDER_PLACED, self.see_order_again, self.ORDER_SHOWN)
        self.fsm.add_transition(self.CHOOSE_SEE_ORDER, self.ORDER_SHOWN, self.draw, self.ORDER_PLACED)
    
    def see_order_again(self):
        "Displays users order on the screen when the see order is pressed"
        self.draw_order()
        pygame.display.flip()
    def choose_light_sweet(self):
        "Adds 25% sweetness to customer's order and updates screen"
        self.current_customer.add_sweet("25%")
        self.draw()
    def choose_half_sweet(self):
        "Adds 50% sweetness to customer's order and updates screen"
        self.current_customer.add_sweet("50%")
        self.draw()
    def choose_less_sweet(self):
        "Adds 75% sweetness to customer's order and updates screen"
        self.current_customer.add_sweet("75%")
        self.draw()
    def choose_full_sweet(self):
        "Adds 100% sweetness to customer's order and updates screen"
        self.current_customer.add_sweet("100%")
        self.draw()
    def choose_light_ice(self):
        "Adds 25% ice to customer's order and updates screen"
        self.current_customer.add_ice("25%")
        self.draw()
    def choose_half_ice(self):
        "adds 50% ice to customer's order and updates screen"
        self.current_customer.add_ice("50%")
        self.draw()
    def choose_less_ice(self):
        "Adds 75% ice to customer's order and updates screen"
        self.current_customer.add_ice("75%")
        self.draw()
    def choose_full_ice(self):
        "Adds 100% ice to customer's order and updates screen"
        self.current_customer.add_ice("100%")
        self.draw()
    def choose_black(self):
        "adds black tea to customer's order and updates screen"
        self.current_customer.add_tea("Black")
        self.draw()
    def choose_green(self):
        "Adds green tea to customer's order and updates screen"
        self.current_customer.add_tea("Green")
        self.draw()
    def choose_oolong(self):
        "Adds oolong tea to customer's order and updates screen"
        self.current_customer.add_tea("Oolong")
        self.draw()
    def choose_peach(self):
        "adds peach flavor to customer's order and updates screen"
        self.current_customer.add_flavor("Peach")
        self.draw()
    def choose_mango(self):
        "Adds mango flavor to customer's order and updates screen"
        self.current_customer.add_flavor("Mango")
        self.draw()
    def choose_strawberry(self):
        "adds strawberry flavor to customer's order and updates screen"
        self.current_customer.add_flavor("Strawberry")
        self.draw()
    def choose_skim_milk(self):
        "adds skim milk to customer's order and updates screen"
        self.current_customer.add_milk("Skim Milk")
        self.draw()
    def choose_whole_milk(self):
        "adds whole milk to customer's order and updates screen"
        self.current_customer.add_milk("Whole Milk")
        self.draw()
    def choose_no_milk(self):
        "removes milk from customer's order and updates screen"
        self.current_customer.add_milk(None)
        self.draw()
    def display_milk_selections(self):
        "Displays milk selections on screen when button pressed"
        self.whole_milk.draw(self.window)
        self.skim_milk.draw(self.window)
        self.no_milk.draw(self.window)
    def display_tea_selections(self):
        "Displays tea selections on screen when button pressed"
        self.black.draw(self.window)
        self.green.draw(self.window)
        self.oolong.draw(self.window)
    def display_flavor_selections(self):
        "Displays flavor selections on screen when button pressed"
        self.mango.draw(self.window)
        self.peach.draw(self.window)
        self.strawberry.draw(self.window)
    def display_ice_selections(self):
        "Displays ice selections on screen when button pressed"
        self.light_ice.draw(self.window)
        self.less_ice.draw(self.window)
        self.half_ice.draw(self.window)
        self.full_ice.draw(self.window)
    def display_sweet_selections(self):
        "Displays sweet selections on screen when button pressed"
        self.light_sweet.draw(self.window)
        self.less_sweet.draw(self.window)
        self.half_sweet.draw(self.window)
        self.full_sweet.draw(self.window)
    def display_new_customer(self):
        "Displays new customer on screen and order when button pressed"
        self.draw_order()
        self.current_customer.draw(self.window)
        pygame.display.flip()
        pygame.time.wait(2000)
        self.draw()
        pygame.display.flip()
    def add_boba(self):
        "adds boba on screen when button pressed"
        self.current_customer.add_topping("Boba")
        self.draw()
    def run(self):
        "While the game is running, updates to new customer if the order is complete"
        self.draw() 
        while self.running:
            self.handle_events()
            pygame.display.flip()
            # Order matches customer order
            if self.current_customer.order_matches():
                # Updates completed orders
                self.orders_completed = self.orders_completed + 1
                print(0)
                self.customer_line.pop(0)
                self.current_customer = self.customer_line[0]
                self.fsm.current_state = self.NO_ORDER
                self.order = self.current_customer.make_order()
                self.draw()
        pygame.quit()
    def draw_order(self):
        "Draws the customer's order on the top left of the screen"
        text_y = 150  # Starting position for displaying text
        text_1 = ""
        text_2 = ""
        text_3 = ""
        # Splits up customer order when printing to 3 separate lines if text overflows
        if len(self.order) > 35:
            new_text = self.order[35:]
            index1 = new_text.index(" ") + 35
            text_1 = self.order[:index1]
            try:
                if len(self.order) > 70:
                    new_text = self.order[70:]
                    index2 = new_text.index(" ") + 70

                    text_2 = self.order[index1 + 1:index2]
                    text_3 = self.order[index2 + 1:]
                else:
                    text_2 = self.order[index1 + 1:]
            except ValueError:
                text_2 = self.order[index1 + 1:]
        text_1 = f"{text_1}"
        text_2 = f"{text_2}"
        text_3 = f"{text_3}"
        textbox = pygame.Rect(100, text_y, self.textbox_width, self.textbox_height)
        inner_box = pygame.Rect(105, text_y+5, self.textbox_width - 10, self.textbox_height - 10)
        text_surface1 = self.font.render(text_1, True, (0, 0, 0))  # Render text in black
        text_surface2 = self.font.render(text_2, True, (0, 0, 0))  # Render text in black
        text_surface3 = self.font.render(text_3, True, (0, 0, 0))  # Render text in black
        pygame.draw.rect(self.window, (0, 0, 0), textbox, 6)  # Draw a black text box
        pygame.draw.rect(self.window, (255, 255, 255), inner_box)
        self.window.blit(text_surface1, (113.5, text_y + 5))  # Adjust position for text within the box
        self.window.blit(text_surface2, (113.5, text_y + 35))  # Adjust position for text within the box
        self.window.blit(text_surface3, (113.5, text_y + 65))  # Adjust position for text within the box
    def handle_events(self):
        "Takes customer input and processes fsm based off the textbox the customer has made"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button click
                    mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                    # If customer clicked on new customer box while not making an order, process in fsm
                    if self.fsm.current_state == self.NO_ORDER and self.new_customer_box.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.NEW_CUSTOMER)
                    # if the user clicks on adding boba while making order, process in fsm
                    elif self.fsm.current_state == self.ORDER_PLACED and self.boba_box.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.NEW_TOPPING)
                    # If the user clicks on choosing a flavor while making order, process in fsm
                    elif self.fsm.current_state == self.ORDER_PLACED and self.flavor_box.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.NEW_FLAVOR)
                    # if user clicks on choosing mango while choosing a flavor, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_FLAVOR and self.mango.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.MANGO_CHOSEN)
                    # If user clicks on choosing strawberry while choosing flavor, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_FLAVOR and self.strawberry.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.STRAWBERRY_CHOSEN)
                    # If user clicks on choosing peach while choosing flavor, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_FLAVOR and self.peach.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.PEACH_CHOSEN)
                    # If user clicks on choose milk while making order, process in fsm
                    elif self.fsm.current_state == self.ORDER_PLACED and self.milk_box.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.NEW_MILK)
                    # If user clicks on whole milk while choosing milk, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_MILK and self.whole_milk.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.WHOLE_MILK_CHOSEN)
                    # If user clicks on skim milk while choosing milk, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_MILK and self.skim_milk.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.SKIM_MILK_CHOSEN)
                    # If user clicks on no milk while choosing milk, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_MILK and self.no_milk.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.NO_MILK_CHOSEN)
                    # If user clicks on choose sweet while making order, process in fsm
                    elif self.fsm.current_state == self.ORDER_PLACED and self.sweet_box.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.NEW_SWEET)
                    # If user clicks on choose ice while making order, process in fsm
                    elif self.fsm.current_state == self.ORDER_PLACED and self.ice_box.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.NEW_ICE)
                    # If user clicks on choose tea while making order, process in fsm
                    elif self.fsm.current_state == self.ORDER_PLACED and self.tea_box.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.NEW_TEA)
                    # If user clicks on light sweet while choosing sweet, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_SWEET and self.light_sweet.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.LIGHT_SWEET_CHOSEN)
                    # If user clicks on less sweet while choosing sweet, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_SWEET and self.less_sweet.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.LESS_SWEET_CHOSEN)
                    # If user clicks on half sweet while choosing sweet, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_SWEET and self.half_sweet.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.HALF_SWEET_CHOSEN)
                    # If user clicks on full sweet while choosing sweet, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_SWEET and self.full_sweet.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.FULL_SWEET_CHOSEN)
                    # If user clicks on light ice while choosing ice, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_ICE and self.light_ice.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.LIGHT_ICE_CHOSEN)
                    # If user clicks on less ice while choosing ice, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_ICE and self.less_ice.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.LESS_ICE_CHOSEN)
                    # If user clicks on half ice while choosing ice, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_ICE and self.half_ice.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.HALF_ICE_CHOSEN)
                    # If user clicks on half ice while choosing ice, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_ICE and self.full_ice.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.FULL_ICE_CHOSEN)
                    # If user clicks on black tea while choosing tea, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_TEA and self.black.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.BLACK_CHOSEN)
                    # If user clicks on green tea while choosing tea, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_TEA and self.green.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.GREEN_CHOSEN)
                    # If user clicks on oolong tea while choosing tea, process in fsm
                    elif self.fsm.current_state == self.CHOOSE_TEA and self.oolong.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.OOLONG_CHOSEN)
                    # If user clicks on see order while making order, process in fsm
                    elif self.fsm.current_state == self.ORDER_PLACED and self.see_order.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.CHOOSE_SEE_ORDER)
                    # If user clicks on see order while order is shown, process in fsm
                    elif self.fsm.current_state == self.ORDER_SHOWN and self.see_order.rect.collidepoint(mouse_pos):
                        self.fsm.process(self.CHOOSE_SEE_ORDER)



    def draw_barista_texts(self):
        "Draws all barista textbox choices on screen"
        self.boba_box.draw(self.window)
        self.flavor_box.draw(self.window)
        self.milk_box.draw(self.window)
        self.sweet_box.draw(self.window)
        self.tea_box.draw(self.window)
        self.ice_box.draw(self.window)
        self.see_order.draw(self.window)
    def draw_customer_box(self):
        "Draws the new customer box on the top left of screen"
        self.new_customer_box.draw(self.window)
    def draw(self):
        print(self.fsm.current_state)
        "Draws the background, and draws text box choices if in the state of making the order"
        self.window.blit(self.background, (0, 0))
        if self.fsm.current_state == self.NO_ORDER:
            self.draw_customer_box()
        elif self.fsm.current_state == self.ORDER_PLACED:
            self.current_customer.draw(self.window)
            self.draw_barista_texts()
            text = "DRINK: "
            # Displays user order on top left of screen
            for i in range(len(self.current_customer.drink)):
                customization = self.current_customer.drink[i]
                if customization != None:
                    text = text + customization + " "
                    if i == 1:
                        text = text + "Tea "
                    elif i == 3:
                        text = text + "Sweet "
                    elif i == 4:
                        text = text + "Ice "
                
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.window.blit(text_surface, (20, 20))
        # Displays completed orders on top right of screen
        text = "ORDERS COMPLETED: " + str(self.orders_completed)
        self.font = pygame.font.Font(None, 30)
        text_surface = self.font.render(text, True, (0, 0, 0))
        self.window.blit(text_surface, (10, 580))
        # Reset font
        self.font = pygame.font.Font(None, 36)
            
        
# Main method
if __name__ == "__main__":
    game = Game()
    game.run()