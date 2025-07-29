# NutriQuery - Nutrition Recommendation System

A full-stack nutrition recommendation application built with Flask (Python) backend and Vue.js frontend.

## 📁 Project Structure

```
NutriQuery/
├── backend/           # Flask API
│   ├── scraper/      # Recipe scraper and related files
│   ├── sql/          # Database dump files
│   │   └── nutriquery_dump.sql
│   ├── app.py        # Main Flask application
│   ├── models.py     # Database models
│   └── requirements.txt
├── frontend/         # Vue.js Application
└── README.md
```

## 🛠️ Prerequisites

- Python 3.7+
- Node.js 14+
- MySQL Server 8.0+
- Git

## ⚙️ MySQL Server & Workbench Installation

### Install MySQL Community Server

1. **Download MySQL Installer**
   - Go to the [MySQL Community Downloads](https://dev.mysql.com/downloads/) page
   - Download "MySQL Installer for Windows"

2. **Run Installation**
   - Choose "Developer Default" or "Custom" installation
   - Ensure "MySQL Server" and "MySQL Workbench" are selected
   - **Important**: Set a strong password for the root user and remember it
   - Keep the default port (3306) unless there are conflicts

3. **Verify MySQL Server is Running**
   - Open Windows Services (`services.msc`)
   - Find the "MySQL" service (e.g., MySQL80)
   - Ensure Status is "Running" and Startup Type is "Automatic"
   - If not running, right-click and select "Start"

## 🚀 Backend Setup (Flask)

### 1. Clone the Repository

```bash
   git clone git@github.com:mansi717/NutriQuery.git
   cd NutriQuery
```

> **Note**: If you get a "Permission denied (publickey)" error, you need to set up SSH keys with GitHub.

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
   cd Backend
   pip install -r requirements.txt
```

### 4. Database Setup & Configuration

#### Create MySQL Database

1. **Connect to MySQL**
   ```bash
   mysql -u root -p
   ```

2. **Create Database**
   ```sql
   CREATE DATABASE nutriquery;
   ```

#### Configure Database Connection

1. **Edit `backend/app.py`**
   ```python
   # Update this line with your MySQL credentials
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_user:your_password@localhost/nutriquery'
   ```

### 5. Data Initialization

Choose **one** of the following options:

### Option A: Import Pre-Populated Data (Recommended)

Using the database dump file (`Backend/sql/nutriquery_dump.sql`):

**Using MySQL Workbench:**
1. Open MySQL Workbench and connect to your MySQL instance
2. Go to **Server** → **Data Import**
3. Select **"Import from Self-Contained File"**
4. Browse and select `Backend/sql/nutriquery_dump.sql`
5. Set **"Default Schema"** to `nutriquery`
6. Click **"Start Import"**
7. Verify data by expanding `nutriquery` → `Tables` in the Navigator panel

**Using Command Line:**

Windows:
```cmd
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" ^
  --binary-mode=1 ^
  -u root -p nutriquery < backend\sql\nutriquery_dump.sql
```

Mac/Linux:
```bash
  mysql -u root -p nutriquery < Backend/sql/nutriquery_dump.sql
```

### Option B: Create Fresh Database with Scraped Data

For a fresh start with newly scraped data:

1. **Create Database Tables**
   ```bash
   python create_tables.py
   ```

2. **Run Recipe Scraper**
   ```bash
   python scraper/recipe_scraper.py
   ```

3. **Update Recipe Time Data**
   After scraping, run this SQL query to process cooking times:
   
   Connect to MySQL:
   ```bash
   mysql -u root -p nutriquery
   ```
   
   Execute the following query:
   ```sql
   UPDATE recipes
   SET total_minutes =
       CAST(
           COALESCE(
               TRIM(TRAILING ' hour' FROM 
                   TRIM(TRAILING ' hours' FROM 
                       REGEXP_SUBSTR(cook_time, '[0-9]+\\s*hours?')
                   )
               ),
               0
           ) AS UNSIGNED
       ) * 60
       +
       CAST(
           COALESCE(
               TRIM(TRAILING ' minute' FROM 
                   TRIM(TRAILING ' minutes' FROM 
                       TRIM(TRAILING ' min' FROM 
                           TRIM(TRAILING ' mins' FROM 
                               REGEXP_SUBSTR(cook_time, '[0-9]+\\s*(?:minute|minutes|min|mins)')
                           )
                       )
                   )
               ),
               0
           ) AS UNSIGNED
       )
   WHERE recipe_id > 0;
   ```
   
   Type `exit;` to quit MySQL.

### 6. Start Flask Server

```bash
  python app.py
```

The backend API will be available at `http://localhost:5000`

## 🎨 Frontend Setup (Vue.js)

### 1. Navigate to Frontend Directory

```bash
  cd Frontend
```

### 2. Install Dependencies

```bash
  npm install
```

### 3. Start Development Server

```bash
  npm run serve
```

### 4. Access the Application

Open your browser and navigate to:
```
http://localhost:8080
```

## 🔧 Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   - Verify MySQL service is running
   - Check username/password in `app.py`
   - Ensure database `nutriquery` exists

2. **Port Conflicts**
   - Backend (Flask): Default port 5000
   - Frontend (Vue): Default port 8080
   - MySQL: Default port 3306

3. **Virtual Environment Issues**
   - Make sure virtual environment is activated before installing packages
   - Use `deactivate` to exit virtual environment

4. **SSH Key Issues**
   - Generate SSH keys: `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
   - Add public key to GitHub account

---

**Happy Coding! 🚀**