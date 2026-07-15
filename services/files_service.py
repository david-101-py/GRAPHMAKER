from pathlib import Path
import datetime
from services.config_service import load_config
from core.files_dir import folders

def load_folders():
    try:
        for folder in folders.values():
            create_path_if_exists(folder, is_file=False)
        return folders
    except (FileExistsError, FileNotFoundError):
        print("Ocurrió un problema al instalar el programa.")
        return None


def create_path_if_exists(path, is_file=bool):
    if not isinstance(path, Path):
        path = Path(path)
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

        