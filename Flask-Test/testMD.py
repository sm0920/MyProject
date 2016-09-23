# Module Test

class Fridge:
    isOpened = False
    foods = []

    def open_ (self):
        self.isOpened = True
        print 'Open the door'
        
    def put_(self, thing):
        if self.isOpened:
            self.foods.append(thing)
            print 'Put food!'
        else:
            print 'Can not'

    def close_(self):
        self.isOpened = False
        print 'Close the door'

class Food:
    pass
