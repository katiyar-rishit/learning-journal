from datetime import datetime


class Employee:
    def __init__(self, name, company, salary):
        self.name = name
        self.company = company
        self._salary = salary

    @classmethod
    def from_string(cls, str_data):
        name, company, salary = str_data.split("-")
        return cls(name, company, int(salary))

    @staticmethod
    def is_workday(day):
        return day.weekday() < 5

    def __repr__(self):
        return f"Employee(name={self.name!r},company={self.company!r},salary={self.salary})"

    def __str__(self):
        return "Employee with name,company,salary"

    def __eq__(self, another):
        if not isinstance(another, Employee):
            return NotImplemented

        return self.salary == another.salary

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if not isinstance(value, (int, float)):
            return TypeError
        if value < 0:
            raise ValueError("Balance cannot be negative.")
        self._salary = value


# main code
today = datetime.today()
print(Employee.is_workday(today))

Mathew = Employee.from_string("Mathew-OGeneral-54345")
print(Mathew.salary)
