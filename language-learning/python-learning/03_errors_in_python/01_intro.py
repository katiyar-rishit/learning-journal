class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model


    def __repr__(self):
        return f"<Car {self.make} {self.model}>"


class Garage:
    def __init__(self):
        self.cars = []


    def __len__(self):
        return len(self.cars)


    def add_car(self, car):
        if not isinstance(car, Car):
            raise TypeError(f"Tried to add {car.__class__.__name__} but only type Car can be added.")
        raise NotImplementedError("This feature is not implemented yet.")



ford = Garage()
car1 = Car('Ford', 'Fiesta')

ford.add_car(car1)





