class Student:
    def __init__(self, new_name, new_grades):
        self.name = new_name
        self.grades = new_grades


    def average(self):
        return sum(self.grades) / len(self.grades)


student_one = Student('Joshua Matthews',[70,87,90,93,89])

print(student_one.name)

print(student_one.average())
#this is happening in background of above line
print(Student.average(student_one))
