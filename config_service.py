import json

from files_service import create_path_if_exists, load_folders

def create_config():
    folders = load_folders()
    BASE_DIR = folders["BASE_DIR"]
    FOLDER_CONFIG = folders["FOLDER_CONFIG"]
    CONFIG_FILE = BASE_DIR / FOLDER_CONFIG / "config_graphmaker.json"
    create_path_if_exists(CONFIG_FILE, is_file=True)
    return CONFIG_FILE

def load_config():
    default_config = {
        "config": {
            "default_colour": "#000000",
            "export_lifetime": 15
        }
    }

    try:
        CONFIG_FILE = create_config()

        if CONFIG_FILE.stat().st_size == 0:
            with open(CONFIG_FILE, "w", encoding="utf-8") as file:
                json.dump(default_config, file, indent=4)
            return default_config

        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            try:
                config_data = json.load(file)
            except json.JSONDecodeError:
                config_data = None

        if not isinstance(config_data, dict) or "config" not in config_data:
            with open(CONFIG_FILE, "w", encoding="utf-8") as file:
                json.dump(default_config, file, indent=4)
            return default_config

        return config_data
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        return default_config

def update_config(new_config_data):
    CONFIG_FILE = create_config()
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        if isinstance(new_config_data, dict):
            json.dump(new_config_data, file, indent=4)
        else:
            file.write(str(new_config_data))

def show_config():
    CONFIG_FILE = create_config()
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config_data = file.read()
        print("Configuration file content:")
        print(config_data)

def modify_config():
    config = load_config()
    keys = list(config["config"].keys())
    for i, key in enumerate(keys, 1):
        print(f"{i}: {key} ({config['config'][key]})")
    try:
        op = int(input("¿Qué quieres modificar? (número): "))
        if op < 1 or op > len(keys):
            print("Número fuera de rango.")
            return
        key = keys[op - 1]
        current_val = config["config"][key]
        new_val = input(f"Nuevo valor para '{key}' (actual: {current_val}): ")
        if isinstance(current_val, bool):
            new_val = new_val.lower() in ("true", "1", "sí", "si", "yes")
        elif isinstance(current_val, int):
            new_val = int(new_val)
        elif isinstance(current_val, float):
            new_val = float(new_val)
        config["config"][key] = new_val
        update_config(config)
        print("Configuración actualizada.")
    except (ValueError, IndexError):
        print("Entrada inválida.")
    

