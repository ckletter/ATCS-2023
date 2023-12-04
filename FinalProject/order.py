class Order:
    def __init__(self, flavor, tea, milk_preference = None, sweetness = 1, ice_level = 1, topping = None):
        self.flavor = flavor
        self.tea = tea
        self.milk_preference = milk_preference
        self.sweetness = sweetness
        self.ice_level = ice_level
        self.topping = topping

    def __repr__(self):
        
        response = "I would like to order a " + self.flavor + " " + self.tea + " tea with "
        if self.milk_preference == None:
            response = response + "no milk "
        else:
            response = response + self.milk_preference
        if self.topping != None:
            response = response + " and " + self.topping
        return response