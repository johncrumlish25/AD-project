# Applied Databases Project

## Overview
This project is a Python console application developed for the Applied Databases module.  
It demonstrates the use of both relational and graph databases.

The application allows users to manage and explore data from a conference system, including attendees, sessions, rooms, and connections between attendees.

## Technologies Used
- Python
- MySQL (via WAMP)
- Neo4j (Graph Database)
- MySQL Connector (Python library)
- Neo4j Python Driver

---

## Features Implemented

### 1. View Speakers & Sessions
- Search for speakers by name
- Displays session title and room

### 2. View Attendees by Company
- Displays attendees from a selected company
- Includes session, speaker, and room details
- Includes input validation

### 3. Add New Attendee
- Add attendee with validation
- Checks for:
  - Duplicate ID
  - Valid gender
  - Existing company

### 4. View Connected Attendees
- Displays connections between attendees

### 5. Add Attendee Connection
- Creates relationships between attendees

### 6. View Rooms
- Displays all rooms with capacity