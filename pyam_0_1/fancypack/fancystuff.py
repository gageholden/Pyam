def uniqify(seq, idfun=None):
    '''idfun must return a marker to identify objects; these markers
    must determine equality!'''
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

def verify_item_uniqueness(itemlist):
    ''''''
    def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: return False
        seen[marker] = 1
        result.append(item)
    return True

def decompress_list(lst, layered = False):
    '''takes a list of lists and returns a simple list
    e.g., [[a] [b]] => [a b]'''
    return_list = []
    if layered == True:
        for l in lst:
            if type(l)==type(list()):
                return_list.extend(decompress_list(l,True))
            else:
                return_list.append(l)
        return return_list
    for l in lst:
        if type(l)==type(list()):
            return_list.extend(l)
        else:
            return_list.append(l)
    return return_list

def find(item, lst):
    for l in lst:
        if item==l:
            return l
    return None

def contains(item,lst):
    '''Returns a boolean value of whether or not the list contains the item'''
    for l in lst:
        if item==l:
            return True
    return False

def index_of(item,lst,list_all = False):
    '''Returns the index of the first item. Returns -1 if not found.'''
    if list_all == False:
        for i in range(len(lst)):
            if item == lst[i]:
                return i
            return -1
    else:
        return_list = []
        for i in range(len(lst)):
            if item == lst[i]:
                return_list.append(i)
        return return_list

'''apply to multiple lists'''
def comp_lists(lst1, lst2):
    val = True
    if(len(lst1)==len(lst2)):
        for i in range(len(lst1)):
            if(lst1[i]!=lst2[i]): return False
        return True
    else: return False
    
def comp_lists_without_order(lst1real, lst2real):
	# make proxies of lists so you don't destroy the originals in the comparison
	lst1 = list(lst1real) 
	lst2 = list(lst2real) 
	lst1.sort()
	lst2.sort()
	if len(lst1)==len(lst2):
		return comp_lists(lst1, lst2)
	else:
		return False
def set_minus(seq1, seq2):
    '''Removes the elements of seq2 from seq1 and returns the result'''
    retseq = []
    return [s for s in seq1 if None==find(s, seq2)]

'''below this are math lists'''
def product(lst):
    '''Multiplies everything in the list'''
    if lst==[]:
        return 1
    else :
        return lst[0] * product(lst[1:])

def my_sum(lst):
    '''Adds everything in the list together, kind of pointless'''
    if lst==[]:
        return 1
    else :
        return lst[0] + sum(lst[1:])

'''boolean lists'''
def or_list(lst,funcy_bool = None):
    if funcy_bool== None:
        for l in lst:
            if l: return True
        return False
    else:
        for l in lst:
            if funcy_bool(l): return True
        return False

def and_list(lst,funcy_bool = None):
    if funcy_bool == None:
        for l in lst:
            if not l: return False
        return True
    else:
        for l in lst:
            if not funcy_bool(l): return False
        return True

'''below this are things you may want to use for various reasons'''
def print_now(string):
    import sys
    '''Forces printing now rather than at a "new line"'''
    sys.stdout.write(string)
    sys.stdout.flush()

def simpledict_speedcopy(org):
     '''Faster than deep copy for a "dict of simple python types"'''
     out = dict().fromkeys(org)
     for k,v in org.iteritems():
         try:
             out[k] = v.copy()   # dicts, sets
         except AttributeError:
             try:
                 out[k] = v[:]   # lists, tuples, strings, unicode
             except TypeError:
                 out[k] = v      # ints

     return out