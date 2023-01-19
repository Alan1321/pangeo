import os

class local_read:
    def __init__(self, path):
        self.path = path
        self.files = []
        self.read()
    def read(self):
        files = os.listdir(self.path)
        for file in files:
            self.files.append(self.path + file)
    def get_files(self):
        return self.files