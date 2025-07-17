# NutriQuery - Nutrition Recommendation System

This project is a full-stack application with:
- **Flask** (Python) as the backend API
- **Vue.js** for the frontend

## Project Structure
- /backend       -> Flask API
- /frontend      -> Vue.js App

---

## 🚀 Backend Setup (Flask)

### 1. Clone the repository
```bash
    git clone git@github.com:mansi717/NutriQuery.git
    cd backend
```
### If you haven’t set up SSH keys yet, GitHub will give you an error like:
```bash
    Permission denied (publickey).
```
In that case generate private and public keys and add it to github 

### 2. Create & activate virtual environment

```bash
    python3 -m venv venv
    source venv/bin/activate  # On Mac/Linux
    venv\Scripts\activate     # On Windows
```

### 3. Install dependencies

```bash
    pip install -r requirements.txt
```

### 4. Run the Flask server

```bash
    python app.py
```

## 🎨 Frontend Setup (Vue.js)

### 1. Navigate to frontend folder

```bash
   cd frontend
```

### 2. Install dependencies

```bash
   npm install
```

### 3. Run the Vue app

```bash
   npm run serve
```