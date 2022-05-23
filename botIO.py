import os
from settings import Settings

class MyIO:
    def __init__(self):
        self.settings = Settings()
        if not os.path.isdir(self.settings.data_dir):
            os.mkdir(self.settings.data_dir)

    def _save(self):
        return True
        