average = lambda sequence: sum(sequence) / len(sequence)
top = lambda sequence: max(sequence)
total = lambda sequence: sum(sequence)

students = [
    {"name": "Mathew", "grades": [50, 67, 87, 45, 97]},
    {"name": "Andrew", "grades": [87, 87, 67, 74, 93]},
    {"name": "Emily", "grades": [82, 98, 75, 96, 59]},
]

user = input("Enter your name: ")

operations = {"average": average, "top": top, "total": total}

for student in students:
    if user == student["name"]:
        action = input("Enter operation ('average', 'top', 'total'):").lower()
        grades = student["grades"]
        for operation in operations:
            if action == operation:
                print(f"{operation}: ", operations[operation](grades))
