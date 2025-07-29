class Student:                                                              
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []
   
 
    def average(self):
        return sum(self.marks) / len(self.marks)


class WorkingStudent(Student):
    def __init__(self, name, school, salary):
        super().__init__(name, school)
        self.salary = salary


    @property
    def weekly_salary(self):
        return self.salary * 30


rolf = WorkingStudent('Rolf', 'MIT', 15.55)
print(rolf.salary) 
rolf.marks.append(78)
rolf.marks.append(98)

"""
prints weekly_salary method as property
(only for methods with self as parameter)
"""
print(rolf.weekly_salary)





