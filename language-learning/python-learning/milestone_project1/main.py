#movie collection
def menu():
    print("""
    What would you like to do?
        1.Add a movie
        2.List all movies
        3.Find a movie
        4.Quit(q)
            """)


def user_input():
    a = input(">").strip().lower()
    if a not in user_choice:
        print("Invalid input")
    return a

def add_movie():
    title = input("Enter movie title: ")
    director = input("Enter movie director: ")
    try:
        year = int(input("Enter year: "))
    except ValueError:
        print("Invalid movie year")
        return

    movies.append({
        "title":title,
        "director":director,
        "year":year
        })
    print(f"{title} added sucessfully")


def list_movie():
    print(movies)


def find_movie():
    search = input("Enter title of movie: ").strip().lower()
    for movie in movies:
        if movie["title"].lower() == search:
            print(movie)
        else:
            continue


def quit_program():
    print("Session ended")
    exit()


movies = []
user_choice = {
    '1':add_movie,
    '2':list_movie,
    '3':find_movie,
    '4':quit_program,
    'q':quit_program
        }

def main():
    while True:
        menu()
        choice = user_input()
        action = user_choice.get(choice)
        if action:
            action()


if __name__ == "__main__":
    main()

print("Session ended.")






