# Applied Databases Project

## Overview
This project is a Python console application developed for the Applied Databases module.  
It demonstrates the use of both relational and graph databases.

The application allows users to manage and explore data from a conference system, including attendees, sessions, rooms, and connections between attendees.

The application is a Python-based conference management system that uses both:
- MySQL
- Neo4j

The system allows users to:
- View speakers and sessions
- View attendees by company
- Add new attendees
- View attendee connections
- Add attendee connections
- View conference rooms

## Technologies Used
- Python
- MySQL (via WAMP)
- Neo4j (Graph Database)
- MySQL Connector (Python library)
- Neo4j Python Driver

## Configuration
Database credentials are stored in a separate configuration file called `config.py`

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

### Option 4 – View Connected Attendees
- Uses Neo4j to display attendee connections
- Handles:
  - Invalid attendee IDs
  - Attendees with no connections
  - Connections in either direction

### Option 5 – Add Attendee Connection
- Creates CONNECTED_TO relationships between attendees
- Includes validation for:
  - Duplicate connections
  - Invalid attendees
  - Self-connections

### Option 6 – View Rooms
- Displays room details
- Uses room caching to match project specification requirements

## Requirements

Required Python packages are listed in `requirements.txt`.

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## Database Setup

Before running the application:

1. Ensure MySQL is running
2. Ensure Neo4j is running
3. Import the provided databases:
   - `appdbproj.sql` into MySQL
   - `appdbprojNeo4j.json` into Neo4j