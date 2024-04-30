def clamp(r, minv, maxv):
    if r<minv:
        return minv
    if r>maxv:
        return maxv    
    return r

def colorComponent(r:float)->int:
    return clamp(int(r), 0, 255)

def colorTuple(r,g,b,a):
    return (colorComponent(r), colorComponent(g), colorComponent(b), colorComponent(a))