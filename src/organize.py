import shutil
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class OrganizeFiles:
    """
    This class is used to organize files in a directory by
    moving files into directions based on extension.
    """
    def __init__(self, directory):
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} does not exist")

        ext_dirs = read_json(DATA_DIR / "extensions.json")
        self.extentions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extentions_dest[ext] = dir_name


    def __call__(self):
        """ Organize files in a directory by moving them
        to sub directories based on extension.
        """
        logger.info(f"Organize files in {self.directory}...")
        file_extensions = []
        for file_path in self.directory.iterdir():
            #ignore directories
            if file_path.is_dir():
                continue
            # ignore hidden files
            if file_path.name.startswith('.'):
                continue
            
            # move files
            file_extensions.append(file_path.suffix)            
            if file_path.suffix not in self.extentions_dest:
                DEST_DIR = self.directory / 'Other'            
            else:
                DEST_DIR = self.directory / self.extentions_dest[file_path.suffix]
                
            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f"Moving {file_path} to {DEST_DIR}...")
            print(f'{file_path.suffix:10} {DEST_DIR}')
            shutil.move(str(file_path), str(DEST_DIR))

if __name__ == "__main__":
    org_files = OrganizeFiles('/mnt/c/Users/DELL/Downloads')
    org_files()
    logger.info("Done!")
