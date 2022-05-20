import http.client
#import json
from settings import Settings
from time import sleep

class GrigoryTestPythonBot:

    def __init__(self):
        self.settings = Settings()
            
    def _check_events(self):
        print("222")
#        sys.exit()

    def run_bot(self):
        print("Press Ctrl+C to exit")
        while True:
            self._check_events()
            sleep(1)
