from files_service import load_folders
from data_service import create_db_file, create_serie
from config_service import show_config, load_config

def main():
    create_serie("Example Serie", group="Example Group")
    load_config()
    show_config()
if __name__ == "__main__":
    main()
