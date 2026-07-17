import sqlite3
from datetime import datetime
from services.files_service import load_folders, create_path_if_exists
from core.tools import today

def get_id(name, serie=True): #Futuro que pueda dar el id de un grupo
    with sqlite3.connect(create_db_file()) as conn:
        cursor = conn.cursor()
        if serie:
            cursor.execute("SELECT id FROM series_metadata WHERE name = ?", (name,))
        else:
            cursor.execute("SELECT group_id FROM groups WHERE group_name = ?", (name,))
        result = cursor.fetchone
        if result:
            serie_id = result[0]
        else:
            serie_id = None
        conn.close()
    return serie_id

#--------------------Creación de base de datos--------------------
def create_db_file():
    folders = load_folders()
    BASE_DIR = folders["BASE_DIR"]
    FOLDER_DATA = folders["FOLDER_DATA"]
    DB_FILE = BASE_DIR / FOLDER_DATA / "db_graphmaker.db"
    create_path_if_exists(DB_FILE, is_file=True)
    return DB_FILE

#--------------------Manejo de db para los valores de las series--------------------
def create_values_db():
    with sqlite3.connect(create_db_file()) as conn:
        cursor = conn.cursor()
        cursor.execute(f''' CREATE TABLE IF NOT EXISTS values_db (
                  serie_id INTEGER PRIMARY KEY,
                  value FLOAT NOT NULL,
                  date DATE NOT NULL
        )''')
    conn.close()

def delete_serie(name):
    with sqlite3.connect(create_db_file()) as conn:
        cursor = conn.cursor()
        serie_id = cursor.execute("SELECT id FROM series_metadata WHERE name = ?", (name,))
        cursor.execute(f"DELETE FROM values_db WHERE serie_id = ?", (serie_id,))
    conn.close()

def clear_last_values(serie_id, days_range):
    with sqlite3.connect(create_db_file()) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM values_db WHERE serie_id = ? AND date < date('now', '-{days_range} days')", (serie_id,))
    conn.close()

def give_values_to_serie(serie_id, value):
    today = today()
    with sqlite3.connect(create_db_file()) as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO values_db (serie_id, value, date) VALUES (?, ?, ?)", (serie_id, value, today))
    conn.close()

#--------------------Manejo de db para datos de series--------------------
def create_serie_metadata():
    with sqlite3.connect(create_db_file()) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS series_metadata (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL UNIQUE,
                   group_name TEXT,
                   birth_date DATE NOT NULL,
                   total_ignore BOOLEAN DEFAULT 0
        )''')
    conn.close()

#--------------------Manejo de db para los grupos de series--------------------
def create_serie_group():
    with sqlite3.connect(create_db_file()) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRYMARY KEY AUROINCREMENT,
        group_name TEXT NOT NULL UNIQUE,
        parent_group 
        birth_date DATE NOT NULL
    )''')
    conn.close()

#--------------------Funciones grandes finales--------------------
def create_serie(name, group=None):
    group = group if group else None
    create_serie_metadata()
    id = get_id(name)
    with sqlite3.connect(create_db_file()) as conn:
        cursor = conn.cursor()
        if group != None:
            cursor.execute("INSERT INTO series_metadata (name, group_name, birth_date) VALUES (?, ?, ?, ?)", (name, group, datetime.now()))
        else:
            cursor.execute("INSERT INTO series_metadata (name, birth_date) VALUES (?, ?, ?)", (name, datetime.now()))    
    conn.close()
    create_values_db()
    return name

def move_serie_into_group(name, group):
    create_serie_metadata()
    with sqlite3.connect(create_db_file()) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                UPDATE series_metadata
                SET group_name = ?
                WHERE name = ?
                   ''', (group, name))
    conn.close()



