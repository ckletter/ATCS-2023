from customer import Customer
from order import Order

class Game:
    def __init__(self):
        self.customers = []
        self.customers.append(Customer(Order("Mango", "Black", "Whole Milk", 0.25, 0.25 , "Boba")))
        self.current_customer = self.customers[0]

    def run(self):
        while len(self.customers) != 0:
            print(self.current_customer.make_order())
            self.customers.pop(0)


if __name__ == "__main__":
    g = Game()
    g.run()