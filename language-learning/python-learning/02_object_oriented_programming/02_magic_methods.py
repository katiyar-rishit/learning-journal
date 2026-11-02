class Student:
    def __init__(self, name):
        self.name = name


movies = ["Matrix", "Batman"]

# everything in python is a object
print(movies.__class__)


class Garage:
    def __init__(self):
        self.cars = []

    def __len__(self):
        return len(self.cars)

    def __getitem__(self, i):
        return self.cars[i]

    def __repr__(self):
        return f"<Garage {self.cars}>"

    def __str__(self):
        return f"Garage with {len(self)} cars."


ford = Garage()
ford.cars.append("Fiesta")
ford.cars.append("Forus")

print(ford.cars)

print(len(ford))  # Garage.__len__(ford)

print(ford[0])  # Garage.__getitem__(ford, 0)

for cars in ford:
    print(cars)

print(ford)  # __str__ gets used here
