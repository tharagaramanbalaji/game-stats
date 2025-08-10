# Game Stats Application

A Flask web application for managing game statistics with MySQL database.

## Features

- Dashboard with top 3 players
- Add new player records
- View all records sorted by wins
- Remove player records

## Setup

1. Install dependencies:

   ```bash
   pip install flask mysql-connector-python
   ```

2. Configure database in `config.py`

3. Run the application:
   ```bash
   python app.py
   ```

## Database Schema

The application uses a MySQL database with a `gameinfo` table containing player statistics.
