from elements import *

params = {'L':1, 'S':1, 'R':5}
outputSettings = {'node':False, 'hist':False, 'match':False, 'gen':False}

def find_similarity(struct1, struct2,objects, paramsIn = {}, settingsIn = {}):
    global params
    global outputSettings
    
    params = paramsIn
    outputSettings = settingsIn
    
    nodelist = make_nodes(struct1,struct2,objects)
    identifyconsistentnodes(nodelist)
    if outputSettings['node']:
        for i in range(len(nodelist)):
            if isinstance(nodelist[i],FeatureNode):
                print "Feat", str(i)
                print struct1.name,nodelist[i].owner_one,nodelist[i].name_one,\
                "|",struct2.name, nodelist[i].owner_two,nodelist[i].name_two
                print "consistent: Obj",nodelist[i].con[0],\
                "Feat",nodelist[i].con[1]
                print "inconsistent: Feat",nodelist[i].inc
            elif isinstance(nodelist[i],ObjectNode):
                print "Obj", str(i)
                print struct1.name,nodelist[i].name_one,"|",struct2.name,\
                nodelist[i].name_two
                print "consistent: Roles",nodelist[i].con[0],\
                "Obj",nodelist[i].con[1],"Feat",nodelist[i].con[2]
                print "inconsistent: Obj",nodelist[i].inc
            else:
                print "Role", str(i)
                print struct1.name,nodelist[i].name_one,"|",struct2.name,\
                nodelist[i].name_two
                print "consistent: Roles",nodelist[i].con[0],\
                "Obj",nodelist[i].con[1]
                print "inconsistent: Roles",nodelist[i].inc
            print
        print "################################################\n"

    settledValues = excitenodes(nodelist)
    calculateFinalSimilarity(settledValues, nodelist)

def calculateFinalSimilarity(valueList, nodelist):
    topSum = 0
    botSum = 0
    
    if outputSettings['match']:
        for value, node in zip(valueList, nodelist):
            print "Name: " + node.name_one + node.name_two + " Value: " +\
                str(value) + " matchvalue: " + str(node.matchvalue)
    
    for value, node in zip(valueList, nodelist):
        if node.type == "Feature":
            topSum = topSum + (node.matchvalue*value*1)
            botSum = botSum + (value*1)
    #print "Similarity: " + str(topSum/botSum)
    if(not topSum==0):
        print topSum/botSum
    else:
        print 0

def make_nodes(struct1, struct2, objects):
    global outputSettings
    
    '''Generates every possible (logical) node in the SIAM style.'''
    rolelist = []
    objlist = []
    featlist = []
    
    global outputSettings

    if outputSettings['gen']: print "Generating Nodes:"
    for x, y in [(x,y) for x in struct1.objectlist.iteritems()\
    for y in struct2.objectlist.iteritems()]:
        #This list comprehension returns tuples which represent each role-object
        #pairing within the structure, these are then decomposed, making the
        #code less ugly than it was before, and allows for easier manipulation.
        str1role, str1obj = x
        str2role, str2obj = y

        #IFOUNDYOUROLENODESLANDYTURNEDOFFARG
        rolelist.append(RoleNode(str1role,str2role,str1obj,str2obj))
        objlist.append(ObjectNode(str1obj,str2obj,str1role,str2role))
        if outputSettings['gen']:print_now("*")
        if outputSettings['gen']:print_now("*")
        for a,b in [(a,b) for a in objects[str1obj].featurelist\
        for b in objects[str2obj].featurelist]:
            if a.dimension == b.dimension:
                featlist.append(FeatureNode(a.dimension, a.value, b.value,
                str1obj,str2obj))
                if outputSettings['gen']: print_now("*")

    rolelist.extend(objlist)
    rolelist.extend(featlist)
    if outputSettings['gen']:print
    if outputSettings['node'] == True:
        print str(len(rolelist)) + " nodes generated!\n"
    return rolelist

def identifyconsistentnodes(nodelist = []):
    global outputSettings
    if outputSettings['gen']:print "Identifying Consistencies"
    for x in range(len(nodelist)):
        nodelist[x].identifyconsistencies(nodelist,x)
        if outputSettings['gen']:print_now("*")
    if outputSettings['gen']:print "\nConsistencies Identified.\n"

def excitenodes(nodelist):
    global params
    global outputSettings
    
    from array import array
    from itertools import repeat
    if outputSettings['hist'] == True:
        layerhistory = []
    settling = True
    prev_layer = array('d',repeat(0.5,len(nodelist)))
    match_val = array('h',[x.matchvalue for x in nodelist])
    if outputSettings['hist'] == True:
        layerhistory.append(array('d',prev_layer))
    newlayer = array('d')
    if outputSettings['hist'] == True:
        print "Match Values: " + match_val.__str__()

    for round in range(params['R']):
        newlayer = array('d',[excite(x,prev_layer,match_val) for x in nodelist])
        #check if newlayer is settled
        prev_layer = newlayer
        settling = False
        if outputSettings['hist'] == True:
            layerhistory.append(array('d',newlayer))
        if outputSettings['gen'] == True:
            if round%10 == 0 and round > 0:
                print_now("*")
                if round%100 == 0:
                    print str(round) + "\n"
                
    if outputSettings['gen']:
        print
    if outputSettings['hist'] == True:
        for layer in range(len(layerhistory)):
            print str(layer)
            for i in range(len(layerhistory[layer])):
                print_now("(" + str(i) + ": "+ ("%.3f" % layerhistory[layer][i]) + ") ")
            print
    return prev_layer

#str(round(layerhistory[layer][i],5))

def excite(node, value, matchvalue):
    global outputSettings
    global params
    L = params['L']
        
    
    if outputSettings['match']: print "Updating Node " + str(node.index)
    Ai = value[node.index]
    sum_top = 0
    sum_bot = 0
    for nd in node.simpcon:
        Aj = value[nd]
        if Aj >= 0.5:
            Rji = Ai + (1-Ai)*(Aj-0.5)
        else: Rji = Ai - Ai*(0.5-Aj)
        delta = Rji     # * matchvalue[nd]
        sum_top += delta
        sum_bot += 1
        if outputSettings['match']: print "  Getting " + str(delta) + " from node " + str(nd)
    for nd in node.inc:
        Aj = value[nd]
        if (1-Aj) >= 0.5:
            Rji = Ai+(1-Ai)*((1-Aj) - 0.5)
        else: Rji = Ai - Ai*(0.5-(1-Aj))
        weight = determineWeight()
        delta = Rji # * weight
        sum_top += delta
        sum_bot += 1 # * weight
        if outputSettings['match']: print "  Losing  " + str(delta) + " from node " + str(nd)
    # Of course, features might match
    if(node.type == "Feature" or node.type=="Role"):
        sum_top += Ai + (1-Ai)*(matchvalue[node.index]-0.5)
        sum_bot += 1
        if outputSettings['match']: print "  Getting " + str(matchvalue[node.index]) + " from matchvalue"
    

    Mi = sum_top/sum_bot

    returnable = Ai*(1-L)+L*Mi
    if returnable < 0: return 0
    return returnable

def determineWeight():
    return