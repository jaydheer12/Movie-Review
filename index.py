movies = [
    "Baahubali",
    "RRR",
    "Salaar",
    "Kalki 2898 AD",
    "Magadheera"
]
movie_ratings = {movie: [] for movie in movies}
students_count = 15
for i in range(students_count):
    print(f"\n--- Student {i+1} ---")
    
    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")
    print("\nTelugu Movies List:")
    for idx, movie in enumerate(movies, start=1):
        print(f"{idx}. {movie}")
    choice = int(input("Select a movie number you like: "))
    selected_movie = movies[choice - 1]
    review = input(f"Enter your review for {selected_movie}: ")
    rating = float(input("Give rating (1 to 5): "))
    movie_ratings[selected_movie].append(rating)
    print("\nThank you for your review!")
print("\n========== Overall Review Summary ==========")
for movie, ratings in movie_ratings.items():
    if ratings:
        avg_rating = sum(ratings) / len(ratings)
        print(f"{movie}: Average Rating = {avg_rating:.2f} ({len(ratings)} reviews)")
    else:
        print(f"{movie}: No reviews")
