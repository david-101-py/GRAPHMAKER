import sqlite3
from datetime import datetime
from services.files_service import load_folders, create_path_if_exists
import zlib
from core.tools import today

# --------------------Creación de ids--------------------
def create_id(name, is_group=False):
    serie_id = zlib.crc32(name.encode('utf-8'))
    if is_group:
        serie_id = f"group_{serie_id}"
    else:
        serie_id = f"serie_{serie_id}"
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
    conn = sqlite3.connect(create_db_file())
    cursor = conn.cursor()
    cursor.execute(f''' CREATE TABLE IF NOT EXISTS values_db (
                  serie_id INTEGER PRIMARY KEY,
                  value FLOAT NOT NULL,
                  date DATE NOT NULL
        )''')
    conn.commit()
    conn.close()

def delete_values_db(name):
    serie_id = create_id(name, is_group=False)
    conn = sqlite3.connect(create_db_file())
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM values_db WHERE serie_id = ?", (serie_id,))
    conn.commit()
    conn.close()

def clear_last_values(serie_id, days_range):
    conn = sqlite3.connect(create_db_file())
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM values_db WHERE serie_id = ? AND date < date('now', '-{days_range} days')", (serie_id,))
    conn.commit()
    conn.close()

def give_values_to_serie(serie_id, value):
    today = today()
    conn = sqlite3.connect(create_db_file())
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO values_db (serie_id, value, date) VALUES (?, ?, ?)", (serie_id, value, today))
    conn.commit()
    conn.close()

#--------------------Manejo de db para datos de series--------------------
def create_serie_db():
    conn = sqlite3.connect(create_db_file())
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS series_data (
                   serie_id TEXT NOT NULL,
                   name TEXT NOT NULL UNIQUE,
                   group_name TEXT,
                   birth_date DATE NOT NULL,
                   total_ignore BOOLEAN DEFAULT 0
        )''')
    conn.commit()
    conn.close()

#--------------------Manejo de db para los grupos de series--------------------
def create_serie_group():
    conn = sqlite3.connect(create_db_file())
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
        group_id TEXT NOT NULL,
        group_name TEXT NOT NULL UNIQUE,
        birth_date DATE NOT NULL,
        group_reason TEXT
    )''')
    conn.commit()
    conn.close()

#--------------------Funciones grandes finales--------------------
def create_serie(name, group=None):
    group = group if group else None
    create_serie_db()
    serie_id = create_id(name, is_group=False)
    conn = sqlite3.connect(create_db_file())
    cursor = conn.cursor()
    cursor.execute("INSERT INTO series_data (serie_id, name, group_name, birth_date, total_ignore) VALUES (?, ?, ?, ?, ?)", (serie_id, name, group, datetime.now(), False))
    conn.commit()
    conn.close()
    create_values_db()
    return serie_id

def add
