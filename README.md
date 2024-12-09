# WelcomeHome

**Final Project for CS-GY 6083 Databases**

**Authors**: Chetan Goel, Eli Borovoy, Ian Davoren

## Setup Instructions

### Prerequisites

- Python 3.x
- MySQL
- `pip` (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/WelcomeHome.git
cd WelcomeHome
```
### Set up the Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
````
### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Set up the Database
1. Start your SQL server
2. Create a new database
```bash
CREATE DATABASE donationDB;
```
3. Run the SQL scripts `DB_init.sql` followed by ` data_insert.sql` in your database client to create the tables and populate the database

### Step 5: Run the Application
```bash
python init.py
```

### Step 6: Open the Application
Open your browser and navigate to `http://127.0.0.1:5000/`