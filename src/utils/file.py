import os
from src.utils.logger import Logger

def delete_all_files():
    logger = Logger()
    directory = os.path.join(os.getcwd(), "output")
    for file in os.listdir(directory):
        full_path = os.path.join(directory, file)
        # Check if it is a file and not a directory
        if os.path.isfile(full_path):
            # Remove the file
            os.remove(full_path)
    logger.info("Arquivos deletados da pasta!")