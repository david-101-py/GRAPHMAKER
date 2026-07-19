from platformdirs import user_data_dir
from platformdirs import user_documents_dir
from pathlib import Path

HIDDEN_BASE_DIR = Path(user_data_dir("Graphmaker", "David.dev"))

VISIBLE_BASE_DIR = Path(user_documents_dir()) / "Graphmaker"

FOLDER_EXPORTS = VISIBLE_BASE_DIR / "EXPORTS"
FOLDER_INPUTS = HIDDEN_BASE_DIR / "INPUTS FOLDER"
FOLDER_DATA = HIDDEN_BASE_DIR / "DATABASE"
FOLDER_CONFIG = HIDDEN_BASE_DIR / "CONFIG"
FOLDER_HISTORY = HIDDEN_BASE_DIR / "HISTORY"

GRAPH_DIR = FOLDER_EXPORTS / "graficas"
TABLE_DIR = FOLDER_EXPORTS / "tablas"
HTML_GRAPH_DIR = FOLDER_EXPORTS / "graficas_html"

hidden_folders = {
    "HIDDEN_BASE_DIR" : HIDDEN_BASE_DIR,
    "FOLDER_INPUTS": FOLDER_INPUTS,
    "FOLDER_DATA": FOLDER_DATA,
    "FOLDER_CONFIG": FOLDER_CONFIG,
    "FOLDER_HISTORY": FOLDER_HISTORY
}

visible_folders = {
    "VISIBLE_BASE_DIR" : VISIBLE_BASE_DIR,
    "FOLDER_EXPORTS" : FOLDER_EXPORTS,
    "GRAPH_DIR" : GRAPH_DIR,
    "TABLE_DIR" : TABLE_DIR,
    "HTML_GRAPH_DIR" : HTML_GRAPH_DIR
}

for path in {**hidden_folders, **visible_folders}.values():
    path.mkdir(parents=True, exist_ok=True)