import sqlite3
import datetime
from core.files_init import DATA_FILE

def get_id(name, serie=True):
    with sqlite3.connect(DATA_FILE) as conn:
        cursor = conn.cursor()
        if serie:
            cursor.execute("SELECT id FROM accounts_metadata WHERE name = ?", (name,))
        else:
            cursor.execute("SELECT group_id FROM groups WHERE group_name = ?", (name,))
        result = cursor.fetchone
        if result:
            id = result[0]
        else:
            id = None
        conn.close()
    return id

def delete_account(name):
    with sqlite3.connect(DATA_FILE) as conn:
        cursor = conn.cursor()
        account_id = cursor.execute("SELECT id FROM accounts_metadata WHERE name = ?", (name,))
        cursor.execute(f"DELETE FROM values_db WHERE account_id = ?", (account_id,))
    conn.close()

def clear_last_values(account_id, days_range):
    with sqlite3.connect(DATA_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM values_db WHERE account_id = ? AND date < date('now', '-{days_range} days')", (account_id,))
    conn.close()

def give_values_to_account(account_id, value):
    today = today()
    with sqlite3.connect(DATA_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO values_db (account_id, value, date) VALUES (?, ?, ?)", (account_id, value, today))
    conn.close()

#--------------------Funciones grandes finales--------------------
def create_account(name, group=None):
    group = group if group else None
    id = get_id(name)
    with sqlite3.connect(DATA_FILE) as conn:
        cursor = conn.cursor()
        if group != None:
            cursor.execute("INSERT INTO accounts_metadata (name, group_name, birth_date) VALUES (?, ?, ?, ?)", (name, group, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            cursor.execute("INSERT INTO accounts_metadata (name, birth_date) VALUES (?, ?, ?)", (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    
    conn.close()
    return name

def move_account_into_group(name, group):
    with sqlite3.connect(DATA_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                    UPDATE accounts_metadata
                    SET group_name = ?
                    WHERE name = ?
        ''', (group, name))
    conn.close()



