from pathlib import Path
from files_service import load_folders, create_path_if_exists
def create_history_file():
    folders = load_folders()    
    HISTORY_DIR = folders["FOLDER_HISTORY"]
    HIST_FILE = HISTORY_DIR / "history_graphmaker.jsonl"
    create_path_if_exists(HIST_FILE, is_file=True)
    return HIST_FILE
create_history_file()
