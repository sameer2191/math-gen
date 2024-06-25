# run.py
import json
from my_library.app import create_app
from my_library.db import initialize_database

def main():
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    initialize_database(config)
    app = create_app(config)
    app.run(debug=True)

if __name__ == '__main__':
    main()
