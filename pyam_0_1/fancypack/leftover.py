def any_relevance(lst1, lst2):
    for l1 in lst1:
        for l2 in lst2:
            if compute_relevance(l1, l2)>0: return True
    return False

def compute_relevance(fact, other_fact):
    # For now, this just counts the intersection of the words in fact and the words in other facts and norms it by the
    # words in both facts
    w1 = set(fact.words())
    w2 = set(other_fact.words())
    inter_length = 1.0 * len(w1.intersection(w2))
    union_length = len(w1.union(w2))

    return inter_length / union_length

def appears(word, fact):
    # returns true iff word appears in fact
    return word in fact.words()
    #w = fact.words()
    #if word in w:
    #    return True
    #else:
    #    return False

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