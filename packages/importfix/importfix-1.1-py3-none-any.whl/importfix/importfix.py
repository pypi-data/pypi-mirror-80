import sys,os

def setImportPathRoot(rootPath):
    fullPath = os.path.abspath(os.getcwd()+"/"+rootPath)
    if not fullPath in sys.path:
        sys.path.append(fullPath)