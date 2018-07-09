import pickle

with open("../data/agisoftExport.obj", "r") as agisoft:
    vertices = agisoft.readlines()
    vertices = vertices[2:]

col = []
for line in vertices:
    items = line.split(" ")
    if items[0] != "v":
        break
    col.append([float(items[4]), float(items[5]), float(items[6])])

pkl_file=open("../data/agisoftExportColors.pkl", "wb")
pickle.dump(col, pkl_file)