movies = (
    "Baahubali",
    "RRR",
    "Salaar",
    "Kalki 2898 AD",
    "Magadheera"
)
students_data = []   # list to store tuples
students_count = 1
for i in range(students_count):
    print(f"\n--- Student {i+1} ---")
    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")
    print("\nTelugu Movies List:")
    for index, movie in enumerate(movies, start=1):
        print(f"{index}. {movie}")
    choice = int(input("Select movie number: "))
    selected_movie = movies[choice - 1]
    review = input("Enter your review: ")
    rating = float(input("Enter rating (1 to 5): "))
    student_record = (name, roll_no, selected_movie, review, rating)
    students_data.append(student_record)
    print("Review saved successfully!")
print("\n========== OVERALL REVIEW SUMMARY ==========")
for movie in movies:
    total_rating = 0
    count = 0
    for record in students_data:
        if record[2] == movie:   # record[2] = movie name
            total_rating += record[4]  # record[4] = rating
            count += 1
    if count > 0:
        avg = total_rating / count
        print(f"{movie}: Average Rating = {avg:.2f} ({count} reviews)")
    else:
        print(f"{movie}: No reviews")
print("\n========== ALL STUDENT DATA ==========")
for data in students_data:
    print(data)
