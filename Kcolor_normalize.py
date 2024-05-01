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

def scale_color_value(value, old_min, old_max, new_min, new_max):
    # 计算原始范围中的位置
    if old_max == old_min:
        return new_min
    normalized = (value - old_min) / (old_max - old_min)
    # 映射到新的范围
    scaled = normalized * (new_max - new_min) + new_min
    return scaled