import sys, getopt
import mapper, elements

outputSettings = {'node':False, 'hist':False, 'match':False, 'gen':False}

featval = {}
featdim = {}
structures = {}
objects = {}

def read_line(prompt):
    if sys.stdin.isatty():
        line = raw_input(prompt)
    else:
        line = raw_input()
    if len(line)>0:
        if line[len(line)-1] == "\\":
            line = line[:len(line)-1] + read_line(" ")
    else:
        return line
    return line

reserved = {
        'have' : 'HAVE',
        'has' : 'HAS',
        'compare' : 'COMPARE',
        'brain' : 'BRAIN',
        'clear' : 'CLEAR',
        'structure' : 'STRUCTURE',
        'quit' : 'QUIT',
        'history' : 'HISTORY',
        'nodeinfo' : 'NODEINFO',
        'match' : 'MATCH',
        'general' : 'GENERAL',
        'set' : 'SET'        
    }

tokens = ['NAME','OBJNAME','STRNAME','FVNAME','FDNAME','NUMBER', 'EQUALS', 'IMPLIES', 'OR', 'VAR', 'COMMENT',
    'PRINT_COMMENT','PARNAME'] + reserved.values()

literals = ['=','+','-','*','/', '(',')', '<', '>', '^', '!', ',', '?', ':', '[', ']', '{', '}']

t_VAR    = r'_[a-zA-Z_][a-zA-Z0-9_]*'

t_EQUALS = r'\=\='
t_IMPLIES = r'->'
t_OR = r'\|'


def t_ID(t):
    r'[a-zB-Z][a-zA-Z_0-9-]*'
    if objects.has_key(t.value):
        t.type = 'OBJNAME'
    elif structures.has_key(t.value):
        t.type = 'STRNAME'
    elif featval.has_key(t.value):
        t.type = 'FVNAME'
    elif featdim.has_key(t.value):
        t.type = 'FDNAME'
    elif mapper.mapperParams.has_key(t.value):
        t.type = "PARNAME"
    else:
        t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    if(not(t.type)):
        t.type = 'NAME'
    return t

def t_NUMBER(t): #Modified to allow positive reals
    r'(\d*[.]\d*)|\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print "Integer value too large", t.value
        t.value = 0
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_COMMENT(t):
    r'\# .*'
    t.type='COMMENT'
    return t

def t_PRINT_COMMENT(t):
    r'%.*'
    t.type='PRINT_COMMENT'
    t.value = t.value.replace("\\n", "\n")
    return t

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules
#low to high
precedence = (
    ('nonassoc', 'HAS', 'HAVE'),
    #('nonassoc', 'TEST', 'QUERY', 'BRAIN', 'GIVEN'),
    #('nonassoc', '<', '>'),
    ('left', ','),
    ('left', 'EQUALS'),
    #('left','+','-'),
    #('left', 'CAUSES'),
    #('left', 'ISA'),
    #('left', 'IMPLIES'),
    #('left', 'OR'),
    #('left', '^'),
    #('left','*','/'),
    #('right','UMINUS'),
    ('nonassoc', 'COMPARE')
    )

def p_statement_comment(p):
    "statement : COMMENT"
    p[0] = p[1]
    pass

def p_statement_print_comment(p):
    "statement : PRINT_COMMENT"
    p[0] = p[1]
    print (p[1][1:] + "\n")

def p_objectplus(p):
    """objectplus : NAME ',' objectplus
                    | NAME
                    | OBJNAME ',' objectplus
                    | OBJNAME"""
    if(len(p)==2):
        p[0] = [p[1]]
        if not objects.has_key(p[1]):
            objects.setdefault(p[1],elements.Object(p[1]))
    else:
        p[0] = [p[1]] + p[3]
        if not objects.has_key(p[1]):
            objects.setdefault(p[1],elements.Object(p[1]))

def p_featurepairplus(p):
    """featurepairplus : featurepair ',' featurepairplus
                    | featurepair """
    if(len(p)==2):
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_featurepair(p):
    """featurepair : NAME NAME
                    | FVNAME NAME
                    | NAME FDNAME
                    | FVNAME FDNAME
                    | """
    p[0] = elements.FeaturePair(p[1],p[2])
    featval.setdefault(p[1])
    featdim.setdefault(p[2])

def p_statement(p):
    """statement : objectplus HAS featurepairplus
                | objectplus HAVE featurepairplus"""
    for obj in p[1]:
        objects[obj].append_features(p[3])


def p_structureplus(p):
    """structureplus : structurebase ',' structureplus
                    | structurebase"""
    if(len(p)==2):
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_structurebase(p):
    """structurebase : STRUCTURE NAME
                        | STRUCTURE STRNAME"""
    if not structures.has_key(p[2]):
        structures[p[2]] = elements.Structure(p[2])
    p[0] = p[2]

def p_structure_statement(p):
    """statement : structureplus HAS roleplus
                    | structureplus HAVE roleplus"""
    for struct in p[1]:
        structures[struct].append_objects(p[3])

def p_roleplus(p):
    """roleplus : role ',' roleplus
                | role"""
    if(len(p)==2):
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_role(p):
    """role : NAME NAME
            | NAME OBJNAME"""
    p[0] = [p[1], p[2]]


def p_compare_objects(p):
    """statement : COMPARE '(' STRNAME ',' STRNAME ')'"""
    global outputSettings
    mapper.find_similarity(structures[p[3]],structures[p[5]],dict(objects), outputSettings)

def p_error(p):
    if p:
        print "Syntax error at '%s'" % p.value
    else:
        print "Syntax error at EOF"

def p_history(p):
    """statement : HISTORY"""
    global outputSettings
    outputSettings['hist'] = not outputSettings['hist']
    print outputSettings['hist']
    
def p_nodeinfo(p):
    """statement : NODEINFO"""
    global outputSettings
    outputSettings['node'] = not outputSettings['node']
    print outputSettings['node']
    
def p_match(p):
    """statement : MATCH"""
    global outputSettings
    outputSettings['match'] = not outputSettings['match']
    print outputSettings['match']

def p_general(p):
    """statement : GENERAL"""
    global outputSettings
    outputSettings['gen'] = not outputSettings['gen']
    print outputSettings['gen']

def p_brain(p):
    """statement : BRAIN"""
    print "###Ze brain is being dumped###"
    sorted(structures)
    for a, b in structures.iteritems():
        print b
    sorted(objects)
    for a, b in objects.iteritems():
        print b

def p_clear(p):
    """statement : CLEAR"""
    structures.clear()
    objects.clear()
    featval.clear()
    featdim.clear()
    print
    print "EVERYTHING HAS BEEN DELETED FOREVER"
    print

def p_quit(p):
    """statement : QUIT"""
    sys.exit()
    
def p_set(p): #I should be able to add a more specific name list with relative ease, afaik
    """statement : SET setplus"""
    for element in p[2]:
        mapper.mapperParams[element[0]]= element[1]
    
def p_setplus(p):
    """setplus : setbase ',' setplus
                    | setbase"""
    if(len(p)==2):
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
        
def p_setbase(p):
    """setbase : PARNAME NUMBER"""
    if not structures.has_key(p[2]):
        structures[p[2]] = elements.Structure(p[2])
    p[0] = [p[1],p[2]]
    
def command(command):
    import ply.yacc as yacc
    yacc.yacc()
    if not command.isspace():
        yacc.parse(command)

def induce(fileIn, paramsIn={}, settingsIn={}):
    import ply.yacc as yacc
    yacc.yacc()
    
    global outputSettings
    
    if(paramsIn!={}):
        for key in paramsIn.keys():
            mapper.mapperParams[key] = paramsIn[key]
            
    if(paramsIn!={}):
        for key in settingsIn.keys():
            outputSettings[key] = settingsIn[key]
    
    with open(fileIn, 'r') as fyle:
        line = fyle.readline()
        while line:
            if not line.isspace():
                yacc.parse(line)
            line = fyle.readline()

def terminal():
    # Define a dictionary: a default set of stuff to do with one keypress
    opts, detupler = getopt.getopt(sys.argv[1:], "nhmgl:r:s:", ["node", "hist",\
    "match", "gen", "learningrate=", "rounds="])
    
    global outputSettings

    for o,a in opts:
        if o in ("-n", "--node"):
            outputSettings['node'] = True
        if o in ("-h", "--hist"):
            outputSettings['hist'] = True
        if o in ("-m", "--match"):
            outputSettings['match'] = True
        if o in ("-g", "--gen"):
            outputSettings['gen'] = True
        if o in ("-l","--learningrate"):
            #print "new learning rate is " + a
            mapper.mapperParams['l'] = float(a)
        if o in ("-r","--rounds"):
            #print "new settle rate is " + a
            mapper.mapperParams['r'] = int(a)
    
    import ply.yacc as yacc
    yacc.yacc()

    while 1:
        try:
            s = read_line("> ")
        except EOFError:
            break
        if not s: continue
        yacc.parse(s)
    
if __name__ == "__main__":
    terminal()