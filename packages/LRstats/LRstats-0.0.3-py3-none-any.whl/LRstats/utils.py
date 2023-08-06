import os

def checkOutdir(path):
    if not os.path.exists(path):
        os.makedirs(path, 0o750)