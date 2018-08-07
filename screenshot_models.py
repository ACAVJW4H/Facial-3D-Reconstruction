import PhotoScan
import os

def getObjs():
    """
    Get the LQ and HQ obj files
    """
    cwd = os.getcwd()
    all_files = sorted(os.listdir(cwd))

    objs = {
        HQ = []
        LQ = []
    }
    for f in files:
        if ".obj" and "HQ" in f:
            objs["HQ"].append(f)
        elif ".obj" and "LQ" in f:
            objs["LQ"].append(f)
    
    print(objs)