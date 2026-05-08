import mysql.connector
from neo4j import GraphDatabase
import config

# MySQL Connection
conn = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    password=config.MYSQL_PASSWORD,
    database=config.MYSQL_DATABASE
)

cursor = conn.cursor()

# Neo4j Connection
driver = GraphDatabase.driver(
    config.NEO4J_URI,
    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)

# ========================
# Functions
# ========================

# option 1: speakers & sessions
def view_speakers_sessions():
    try:

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
            print("----------------------------------------")

            for row in results:
                print(f"Speaker: {row[0]}")
                print(f"Session: {row[1]}")
                print(f"Room: {row[2]}")
                print("----------------------------------------")

        else:
            print("No speakers match search.")

        input("\nPress Enter to return to menu...")

    except Exception as e:
        print("Error:", e)

# option 2: view attendees by company
def view_attendees_by_company():
    try:

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
            input("\nPress Enter to return to menu...")
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
            print("----------------------------------------")

            for row in results:
                print(f"Name: {row[0]}")
                print(f"DOB: {row[1]}")
                print(f"Session: {row[2]}")
                print(f"Speaker: {row[3]}")
                print(f"Room: {row[4]}")
                print("----------------------------------------")

        else:
            print("No attendees found for this company.")

        input("\nPress Enter to return to menu...")

    except Exception as e:
        print("Error:", e)

# option 3: add new attendee
def add_new_attendee():
    try:

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
            input("\nPress Enter to return to menu...")
            return

        # validate gender
        if gender not in ["M", "F"]:
            print("Invalid gender. Use M or F.")
            input("\nPress Enter to return to menu...")
            return

        # check if company exists
        cursor.execute("SELECT * FROM company WHERE companyID = %s", (company_id,))
        if not cursor.fetchone():
            print("Company ID does not exist.")
            input("\nPress Enter to return to menu...")
            return

        # insert attendee
        query = """
        INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (attendee_id, name, dob, gender, company_id))
        conn.commit()

        print("Attendee successfully added.")

        input("\nPress Enter to return to menu...")

    except Exception as e:
        print("Error:", e)

# option 4: view connected attendees
def view_connected_attendees():
    try:

        # validate input
        while True:
            attendee_id = input("Enter Attendee ID: ")

            if not attendee_id.isdigit():
                print("Invalid input. Please enter a numeric ID.")
            else:
                attendee_id = int(attendee_id)
                break

        # check MySQL
        mysql_query = """
        SELECT attendeeName
        FROM attendee
        WHERE attendeeID = %s
        """

        cursor.execute(mysql_query, (attendee_id,))
        mysql_result = cursor.fetchone()

        # attendee does not exist anywhere
        if not mysql_result:
            print("Attendee does not exist.")
            input("\nPress Enter to return to menu...")
            return

        attendee_name = mysql_result[0]

        with driver.session() as session:

            # check Neo4j connections in both directions
            neo4j_query = """
            MATCH (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO]-(b:Attendee)
            RETURN b.AttendeeID AS connectedID
            """

            results = session.run(neo4j_query, id=attendee_id)

            connections = [record["connectedID"] for record in results]

            print(f"\nAttendee: {attendee_name}")

            # if no Neo4j connections
            if not connections:
                print("No connections")

            else:
                print("\nConnected Attendees:")
                print("----------------------------")

                for connected_id in connections:

                    # get attendee name from MySQL
                    cursor.execute(
                        "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
                        (connected_id,)
                    )

                    connected_name = cursor.fetchone()

                    if connected_name:
                        print(f"ID: {connected_id}")
                        print(f"Name: {connected_name[0]}")
                        print("----------------------------")

        input("\nPress Enter to return to menu...")

    except Exception as e:
        print("Error:", e)

# option 5: add attendee connection
def add_attendee_connection():
    try:

        # Input validation
        while True:
            id1 = input("Enter first Attendee ID: ")
            id2 = input("Enter second Attendee ID: ")

            if not id1.isdigit() or not id2.isdigit():
                print("Invalid input. Please enter numeric IDs.")
            else:
                id1 = int(id1)
                id2 = int(id2)
                break

        with driver.session() as session:

            # Check both attendees exist
            check_query = """
            MATCH (a:Attendee)
            WHERE a.AttendeeID = $id1 OR a.AttendeeID = $id2
            RETURN a.AttendeeID AS id
            """
            result = session.run(check_query, id1=id1, id2=id2)

            found_ids = [record["id"] for record in result]

            if id1 not in found_ids or id2 not in found_ids:
                print("One or both attendees do not exist.")
                input("\nPress Enter to return to menu...")
                return

            # Create connection (avoids duplicates)
            query = """
            MATCH (a:Attendee {AttendeeID: $id1}), (b:Attendee {AttendeeID: $id2})
            MERGE (a)-[:CONNECTED_TO]->(b)
            """
            session.run(query, id1=id1, id2=id2)

            print("Connection successfully added.")

        input("\nPress Enter to return to menu...")

    except Exception as e:
        print("Error:", e)

# option 6: view rooms
def view_rooms():
    try:

        # get all rooms
        query = "SELECT roomID, roomName, capacity FROM room"
        cursor.execute(query)

        results = cursor.fetchall()

        # Check if any rooms exist
        if results:
            print("\nRooms:")
            print("-----------------------------")

            for row in results:
                print(f"Room ID: {row[0]}")
                print(f"Room Name: {row[1]}")
                print(f"Capacity: {row[2]}")
                print("-----------------------------")

        else:
            print("No rooms found.")

        input("\nPress Enter to return to menu...")

    except Exception as e:
        print("Error:", e)

# ========================
# Main Menu
# ========================

# main menu display
def main_menu():
    while True:
        print("\nConference Management")
        print("----------------------")
        print("\nMENU")
        print("====")
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
            view_connected_attendees()
        elif choice == "5":
            add_attendee_connection()
        elif choice == "6":
            view_rooms()
        elif choice.lower() == "x":
            print("Exiting application...")

            cursor.close()
            conn.close()
            driver.close()
            break
    
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main_menu()