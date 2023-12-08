class Order:
    def __init__(self, flavor, tea, milk_preference = None, sweetness = 1, ice_level = 1, topping = None):
        self.flavor = flavor
        self.tea = tea
        self.milk_preference = milk_preference
        self.sweetness = sweetness
        self.ice_level = ice_level
        self.topping = topping

    def return_order(self):
        
        response = "I would like to order a"
        if self.flavor != None:
            response = response + " " + self.flavor
        response = response + " " + self.tea + " Tea"
        if self.milk_preference != None:
            response = response + " with " + self.milk_preference
        if self.topping != None:
            response = response + " and " + self.topping
        return response