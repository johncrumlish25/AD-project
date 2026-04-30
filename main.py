import mysql.connector

# test connection to MySQL database
def test_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="appdbproj"
        )

        if connection.is_connected():
            print("Connected to MySQL")

        connection.close()

    # print any errors
    except Exception as e:
        print("Error:", e)

def view_rooms():
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="appdbproj"
        )

        cursor = connection.cursor()

        # get all rooms
        query = "SELECT roomID, roomName, capacity FROM room"
        cursor.execute(query)

        results = cursor.fetchall()

        # Check if any rooms exist
        if results:
            print("\nRooms:")
            print("-----------------------------")
            for row in results:
                print(f"ID: {row[0]} | Name: {row[1]} | Capacity: {row[2]}")
        else:
            print("No rooms found.")

        # Close connection
        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)

# main menu display
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
            view_rooms()
            test_connection()
        elif choice.lower() == "x":
            print("Exiting application...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main_menu()