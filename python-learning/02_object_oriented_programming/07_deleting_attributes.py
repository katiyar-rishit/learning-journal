class Person:
    def __init__(self, new_name, new_job, new_salary):
        self.name = new_name
        self.job = new_job
        self.salary = new_salary

    def greet(self):
        print(f"Hello {self.name},I heard you work as a {self.job} now.")


Mathew = Person("Mathew", "Astronaut", 9860860)

print(Mathew.job)

del Mathew.job

print(Mathew.job)  # this gives error now
