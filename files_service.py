from pathlib import Path
import datetime
from config_service import load_config

def load_folders():       
    try:

        BASE_DIR = Path(__file__).resolve().parent

        FOLDER_EXPORTS = BASE_DIR / "EXPORTS"
        FOLDER_INPUTS = BASE_DIR / "INPUTS FOLDER"
        FOLDER_DATA = BASE_DIR / "DATABASE"
        FOLDER_CONFIG = BASE_DIR / "CONFIG"

        # Crear carpetas base
        create_path_if_exists(FOLDER_EXPORTS, is_file=False)
        create_path_if_exists(FOLDER_INPUTS, is_file=False)
        create_path_if_exists(FOLDER_DATA, is_file=False)
        create_path_if_exists(FOLDER_CONFIG, is_file=False)

        # Subcarpetas
        GRAPH_DIR = FOLDER_EXPORTS / "graficas"
        TABLE_DIR = FOLDER_EXPORTS / "tablas"
        HTML_GRAPH_DIR = FOLDER_EXPORTS / "graficas_html"

        # Crear subcarpetas
        create_path_if_exists(GRAPH_DIR, is_file=False)
        create_path_if_exists(TABLE_DIR, is_file=False)
        create_path_if_exists(HTML_GRAPH_DIR, is_file=False)

        UNDO_STACK = []
        error = False
    except (FileNotFoundError, FileExistsError):
        print("An error occurred while setting up the necessary folders.")
        error = True
    if error == False:
        folders = {
            "BASE_DIR": BASE_DIR,
            "FOLDER_EXPORTS": FOLDER_EXPORTS,
            "FOLDER_INPUTS": FOLDER_INPUTS,
            "FOLDER_DATA": FOLDER_DATA,
            "FOLDER_CONFIG": FOLDER_CONFIG,
            "GRAPH_DIR": GRAPH_DIR,
            "TABLE_DIR": TABLE_DIR,
            "HTML_GRAPH_DIR": HTML_GRAPH_DIR,
            "UNDO_STACK": UNDO_STACK
        }
        return folders
    else:
        return None

def create_path_if_exists(path, is_file=bool):
    if not path.exists():
        if is_file:
            path.touch(exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)
    return path

def return_file_age(file_path):
    if file_path.exists():
        date = datetime.datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%d/%m/%Y %H:%M')
        return date
    return None

def clear_exports():
    folders = load_folders()
    config_data = load_config()
    max_live_time = config_data["config"]["export_lifetime"]
    if folders == None:
        return None

    for folder in ["GRAPH_DIR", "TABLE_DIR", "HTML_GRAPH_DIR"]:
        path = folders[folder]
        ages = {}
        for file in path.iterdir():
            if file.is_file():
                ages[file.name] = return_file_age(file)
    for file in ages:
        file_path = path / file
        if datetime.datetime.now() - datetime.datetime.strptime(ages[file], '%d/%m/%Y %H:%M') > datetime.timedelta(days=max_live_time):
            file_path.unlink()
    print(f"Deleted files older than {max_live_time} days.")

def say_all_in_order():
    folders = load_folders()
    ok_folders = []
    for folder in folders:
        path = folders[folder]
        ok_folders.append(path)
    if len(ok_folders) == len(folders):
        return True
    return False

        