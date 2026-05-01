import mysql.connector
from neo4j import GraphDatabase

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

# option 1: speakers & sessions
def view_speakers_sessions():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="appdbproj"
        )

        cursor = connection.cursor()

        # Get user input
        search = input("Enter speaker name: ")

        # SQL query with JOINs
        query = """
        SELECT se.speakerName, se.sessionTitle, r.roomName
        FROM session se
        JOIN room r ON se.roomID = r.roomID
        WHERE se.speakerName LIKE %s
        """

        cursor.execute(query, ("%" + search + "%",))
        results = cursor.fetchall()

        if results:
            print("\nResults:")
            print("-----------------------------")
            for row in results:
                print(f"Speaker: {row[0]} | Session: {row[1]} | Room: {row[2]}")
        else:
            print("No speakers match search.")

        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)

# option 2: view attendees by company
def view_attendees_by_company():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="appdbproj"
        )

        cursor = connection.cursor()

        while True:
            company_id = input("Enter Company ID: ")

            if not company_id.isdigit() or int(company_id) <= 0:
                print("Invalid company ID. Please enter a number greater than 0.")
            else:
                break

        # Check if company exists
        cursor.execute("SELECT companyName FROM company WHERE companyID = %s", (company_id,))
        company = cursor.fetchone()

        if not company:
            print("Company does not exist.")
            return

        print(f"\nCompany: {company[0]}")

        # Main query
        query = """
        SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, r.roomName
        FROM attendee a
        JOIN registration reg ON a.attendeeID = reg.attendeeID
        JOIN session s ON reg.sessionID = s.sessionID
        JOIN room r ON s.roomID = r.roomID
        WHERE a.attendeeCompanyID = %s
        """

        cursor.execute(query, (company_id,))
        results = cursor.fetchall()

        if results:
            print("\nAttendees:")
            print("-----------------------------------------------------")
            for row in results:
                print(f"Name: {row[0]} | DOB: {row[1]} | Session: {row[2]} | Speaker: {row[3]} | Room: {row[4]}")
        else:
            print("No attendees found for this company.")

        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)

# option 3: add new attendee
def add_new_attendee():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="appdbproj"
        )

        cursor = connection.cursor()

        # get user input
        attendee_id = int(input("Enter Attendee ID: "))
        name = input("Enter Name: ")
        dob = input("Enter DOB (YYYY-MM-DD): ")
        gender = input("Enter Gender (M/F): ")
        company_id = input("Enter Company ID: ")

        # check if ID already exists
        cursor.execute("SELECT * FROM attendee WHERE attendeeID = %s", (attendee_id,))
        if cursor.fetchone():
            print("Attendee ID already exists.")
            return

        # validate gender
        if gender not in ["M", "F"]:
            print("Invalid gender. Use M or F.")
            return

        # check if company exists
        cursor.execute("SELECT * FROM company WHERE companyID = %s", (company_id,))
        if not cursor.fetchone():
            print("Company ID does not exist.")
            return

        # insert attendee
        query = """
        INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (attendee_id, name, dob, gender, company_id))
        connection.commit()

        print("Attendee successfully added.")

        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)

# option 6: rooms
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

# Function to test connection to Neo4j database
def test_neo4j_connection():
    try:
        # Connection details for Neo4j
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "root1234" 

        # Create a driver instance to connect to Neo4j
        driver = GraphDatabase.driver(uri, auth=(username, password))

        # Open a session to run Cypher queries
        with driver.session() as session:
            result = session.run("RETURN 'Connected to Neo4j!' AS message")

            # Print the result from the query
            for record in result:
                print(record["message"])

        driver.close()

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
            view_speakers_sessions()
        elif choice == "2":
            view_attendees_by_company()
        elif choice == "3":
            add_new_attendee()
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