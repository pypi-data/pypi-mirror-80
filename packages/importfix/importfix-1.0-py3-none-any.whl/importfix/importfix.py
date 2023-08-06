import sys,os

def setImportPathRoot(rootPath):
    fullPath = os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/"+rootPath)
    if not fullPath in sys.path:
        sys.path.append(fullPath)