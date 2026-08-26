grades = [60, 95, 32, 85, 70, 43, 50]

passing_grades = list(filter(lambda grades: grades>=60, grades))

print(passing_grades)

