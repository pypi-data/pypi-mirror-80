from texting import DOT, SP


def brief_name(name):
    vec = name.split(SP)
    last = vec.pop()
    while last == 'Jr.':
        last = vec.pop() + last
    return DOT.join([x[0] for x in vec]) + DOT + last
