#first class function

avg = lambda sequence: sum(sequence) / len(sequence)
total = lambda sequence: sum(sequence)
top = lambda sequence: max(sequence)

students = [
        {"name":"Andrew","grades":(96,84,92,87,82)},
        {"name":"Sasha","grades":(90,81,88,49,58)}, 
        {"name":"Rick","grades":(97,64,32,67,82)} 
 ]

operations = {
    "average": avg,
    "sum": total,
    "max": top
        }

for student in students:
    name = student["name"]
    grades = student["grades"]
    print(f"Hello {name}")
    operation = input("Enter 'average', 'sum', 'max': ").lower().strip()
    try:
        operations_function = operations[operation]
        print(operations_function(grades))
    except KeyError:
        print("Not a valid operation")
