quiet = True
elementParams = {}

class FeaturePair:
    '''Defines a feature dimension feature value pair to be used in an object'''
    def __init__(self, dimension_in=None, value_in=None):
        '''Declares a feature pair.'''
        self.dimension = dimension_in
        self.value = value_in

    def __str__(self):
        '''Returns a simple definition of the feature pair'''
        return "\tDimension: " + self.dimension \
                +"\tValue: " + self.value

class Object:
    '''This class defines an object based on SIAMs definition'''
    def __init__(self,name_in = None, list_in = []):
        self.name = name_in
        self.featurelist = list(list_in)

    def append_features(self, featurepair_in = None):
        '''Appends a bunch of feature pairs to this object.
        Checks for overwrites in order to warn the user.'''
        global quiet
        for fet in featurepair_in:
            for feat in self.featurelist:
                if fet.dimension == feat.dimension:
                    if not quiet: print "Overwriting " + fet.dimension\
                        + " in " + self.name
                    self.featurelist.remove(feat)
                    continue
        self.featurelist += featurepair_in

    def getInfo(self):
        '''Gets a list of info from the object, though I'm not sure why?'''
        return [self.name,self.featurelist]

    def __str__(self, depth = ""):
        '''Prints rather than returns.'''
        print self.name
        for x in self.featurelist: print depth + x.__str__()
        return ""

class Structure:
    '''This defines an overall group/scene/structure to be compared.'''
    def __init__(self, name_in, role_in = []):
        '''Declares the structures name, creates an objectlist dict and appends
        objects given through the role_in to the objectlist.'''
        self.name = name_in
        self.objectlist = {}
        self.append_objects(role_in)
        
    def append_object(self, role, object_name):
        '''Appends a signle role object to the dict.'''
        self.objectlist[role] = object_name

    def append_objects(self, list_in):
        '''Takes a list of short lists that define roles and makes them roles'''
        global quiet
        for element in list_in:
            if element[0] in self.objectlist and not quiet:
                print "OVERWRITING "+element[0]+" IN "+self.name+" AS REQUESTED"
            self.objectlist[element[0]] = element[1]

    def __str__(self):
        '''version of a __str__ function that prints rather than returns'''
        print_now(self.name + " contains ")
        sorted(self.objectlist)
        for a, b in self.objectlist.iteritems():
            print_now("(" + a + ": " + b + ") ")
        return ""

class RoleNode:
    def __init__(self, name_one, name_two, obj_one, obj_two):
        self.type = "Role"
        self.prev = 0.5
        
        self.name_one = name_one
        self.name_two = name_two
        self.obj_one = obj_one
        self.obj_two = obj_two
        #The pattern is role object
        self.con = [[],[]]
        #All elements are only inconsistent with themselves.
        self.inc = []

        # DL changed the match values, since he thinks roles always match.
        self.matchvalue = 1
        if name_one == name_two:
            self.matchvalue = 1
        else:
            self.matchvalue = 0

    def identifyconsistencies(self, nodelist, step_val=-1):
        self.index = step_val
        for i in range(len(nodelist) - step_val - 1):
            i = i + step_val + 1
            if isinstance(nodelist[i],RoleNode):
                if (nodelist[i].name_one == self.name_one
                or nodelist[i].name_two  == self.name_two):
                    self.inc.append(i)
                    nodelist[i].inc.append(step_val)
                else:
                    self.con[0].append(i)
                    nodelist[i].con[0].append(step_val)
            elif isinstance(nodelist[i],ObjectNode):
                if (nodelist[i].role1 == self.name_one and \
                    nodelist[i].name_one == self.obj_one and \
                    nodelist[i].role2 == self.name_two and \
                    nodelist[i].name_two == self.obj_two):
                    self.con[1].append(i)
                    nodelist[i].con[0].append(step_val)
            else:
                break
        self.simpcon = [item for sublist in self.con for item in sublist]

class ObjectNode:
    def __init__(self, name_one, name_two, role1, role2):
        self.type = "Object"
        self.prev = 0.5
        
        self.name_one = name_one
        self.name_two = name_two
        self.role1 = role1
        self.role2 = role2
        #the pattern is role, object, feature
        self.con = [[],[],[]]
        #All elements can only be inconsistent with themselves
        self.inc = []
        # David Landy changed the match value from 1 to 0, because he believes objects don't match
        self.matchvalue = 0

    def identifyconsistencies(self, nodelist, step_val=-1):
        self.index = step_val
        for i in range(len(nodelist) - step_val - 1):
            i = i + step_val + 1
            if isinstance(nodelist[i],ObjectNode):
                if (nodelist[i].role1 == self.role1
                or nodelist[i].role2 == self.role2):
                    self.inc.append(i)
                    nodelist[i].inc.append(step_val)
                else:
                    self.con[1].append(i)
                    nodelist[i].con[1].append(step_val)
            elif isinstance(nodelist[i],FeatureNode) and\
            ((nodelist[i].owner_one == self.name_one and
            nodelist[i].owner_two == self.name_two)):
                self.con[2].append(i)
                nodelist[i].con[0].append(step_val)
        self.simpcon = [item for sublist in self.con for item in sublist]

class FeatureNode:
    def __init__(self, dimension, name_one, name_two, object_one, object_two):
        self.type = "Feature"
        self.prev = 0.5
        
        self.name_one = name_one
        self.name_two = name_two
        self.owner_one = object_one
        self.owner_two = object_two
        self.dimension = dimension
        #the pattern is object, feature
        self.con = [[],[]]
        #Elements are only inconsistent with themselves
        self.inc = []
        if name_one == name_two:
            self.matchvalue = 1
        else:
            self.matchvalue = 0

    def identifyconsistencies(self, nodelist, step_val=-1):
        self.index = step_val
        for i in range(len(nodelist) - step_val - 1):
            i = i + step_val + 1
            if isinstance(nodelist[i],FeatureNode) and\
            nodelist[i].dimension == self.dimension:
                if (nodelist[i].owner_one == self.owner_one
                or nodelist[i].owner_two  == self.owner_two):
                    self.inc.append(i)
                    nodelist[i].inc.append(step_val)
                else:
                    self.con[1].append(i)
                    nodelist[i].con[1].append(step_val)
        self.simpcon = [item for sublist in self.con for item in sublist]

def print_now(string):
    import sys
    '''Forces printing now rather than at a "new line"'''
    sys.stdout.write(string)
    sys.stdout.flush()
