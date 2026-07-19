import json
from core.folders_init import FOLDER_CONFIG, FOLDER_DATA, FOLDER_HISTORY

CONFIG_FILE = FOLDER_CONFIG / "config.json"
HISTORY_FILE = FOLDER_HISTORY / "logging.jsonl"
DATA_FILE = FOLDER_DATA / "database.db"

if not DATA_FILE.exists():
    DATA_FILE.touch(exist_ok=True)
if not HISTORY_FILE.exists():
    with open(HISTORY_FILE, 'w', encoding='utf-8'):
        pass
if not CONFIG_FILE.exist():
    default_content = {
        "config": {
            "default_colour": "#000000",
            "export_lifetime": 15
        }
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(default_content, f, indent=4, ensure_ascii=False)    

