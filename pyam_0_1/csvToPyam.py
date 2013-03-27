import csv, sys, re, json

def makeStruct(ents, name):
    out = ["structure",name,"has"]
        
    for i in range(0,len(ents)):
        out.append("spot" + str(i+1))
        out.append(ents[i] + ",")
    return " ".join(out)[:-1]

def makeEnt(entity, name):
    out = [name, "has"]
    for role, val in entity.iteritems():
        out.append(role)
        out.append(role + val + ",")
    return (" ".join(out))[:-1]

def makeComparison(fieldnames,line):
    comparison={'metadata':{'itemNumber':line['itemNumber'], 'block':line['block'],'type':line['type']}}
    #comparison={'itemNumber':line['itemNumber'], 'block':line['block'],'type':line['type']}
    script = []
    
    ents = []
    entity = {}
    fieldNum = 1
    entNumber = 1
    structName = "structure1"
    meta = False
    for field in fieldnames[3:]:
        if meta:
            comparison['metadata'][field]=line[field]
            #comparison[field]=line[field]
        else:
            if field in entity or field == 'line':
                name = "ent" + str(entNumber)
                script.append(makeEnt(entity,name))
                ents.append(name)
                entNumber+=1
                entity = {}
                fieldNum+=1
            if field == 'line':
                script.append(makeStruct(ents,structName))
                structName = "structure2"
                ents = []
            else:
                if field == 'meta':
                    meta = True
                else:
                    entity[field] = line[field+str(fieldNum)]
    
    name = "ent" + str(entNumber)
    script.append(makeEnt(entity,name))
    ents.append(name)

    script.append(makeStruct(ents,structName))
    script.append("compare(structure1,structure2)")
    #script.append("clear")
    comparison['script']=script
    return comparison

def guiPick():
    from Tkinter import Tk
    from tkFileDialog import askopenfilenames
    from os import getcwd
    
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filenames = askopenfilenames(filetypes=[('CSV', '*.csv')], initialdir = getcwd(), title = "OPEN STIMULUS FILES") # show an "Open" dialog box and return the path to the selected file
    return parseFiles(filenames)

def parseFile(filename,start=-1,end=-1):  
    reader = csv.DictReader(open(filename,'rU'))
    fieldnames = [re.sub('[0-9]+', '', field) for field in reader.fieldnames]
    
    pyam_comparisons =[]
    for item in reader:
        if int(item['itemNumber']) >= start and (end == -1 or int(item['itemNumber']) <=end):
            pyam_comparisons.append(makeComparison(fieldnames,item))
            
    return json.dumps(pyam_comparisons)

def parseFiles(filenames,start=-1,end=-1):
    pyam_per_file = {}
    for filename in filenames:
        reader = csv.DictReader(open(filename,'rU'))
        fieldnames = [re.sub('[0-9]+', '', field) for field in reader.fieldnames]
        
        pyam_comparisons =[]
        for item in reader:
            if int(item['itemNumber']) >= start and (end == -1 or int(item['itemNumber']) <=end):
                pyam_comparisons.append(makeComparison(fieldnames,item))
        
        pyam_per_file[str(filename)] = pyam_comparisons
    return json.dumps(pyam_per_file)

    
if __name__ == "__main__":
    import getopt
    
    if(not len(sys.argv) >= 2):
        print "I need a filename in order to parse the file!"
        quit()
    
    opts, detupler = getopt.getopt(sys.argv[2:], "s:e:")
    start = -1
    end = -1
    for o,a in opts:
        if o in ("-s","--start"):
            #print "new learning rate is " + a
            start = int(a)
        if o in ("-e","--end"):
            end = int(a)

    print parseFile(sys.argv[1],start,end)
    quit()
 
