def main_menu():
    while True:
        print("\nConference Management")
        print("----------------------")
        print("1 - View Speakers & Sessions")
        print("2 - View Attendees by Company")
        print("3 - Add New Attendee")
        print("4 - View Connected Attendees")
        print("5 - Add Attendee Connection")
        print("6 - View Rooms")
        print("x - Exit")

        choice = input("Choice: ")

        if choice == "1":
            print("Option 1 selected")
        elif choice == "2":
            print("Option 2 selected")
        elif choice == "3":
            print("Option 3 selected")
        elif choice == "4":
            print("Option 4 selected")
        elif choice == "5":
            print("Option 5 selected")
        elif choice == "6":
            print("Option 6 selected")
        elif choice.lower() == "x":
            print("Exiting Application...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main_menu()