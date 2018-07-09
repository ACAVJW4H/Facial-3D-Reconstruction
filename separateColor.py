with open("../data/agisoftExport.obj", "r") as agisoft:
    vertices = agisoft.readlines()
    vertices = vertices[2:]

col = []
for line in vertices:
    items = line.split(" ")
    if items[0] != "v":
        break
    col.append(items[4:7])

with open("../data/agisoftExportColors.csv", 'w') as output:
    out = []
    for co in col:
        out.append(str(co[0])+","+str(co[1])+","+str(co[2]))
    output.writelines(out)
print("done")
