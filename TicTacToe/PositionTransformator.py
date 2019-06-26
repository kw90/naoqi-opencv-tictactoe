def get_string_from_coordinates(valx, valy):
    temp = ""
    if valx == 0:
        temp += "t"  # top
    elif valx == 1:
        temp += "m"  # middle
    else:
        temp += "d"  # down
    if valy == 0:
        temp += "l"  # left
    elif valy == 1:
        temp += "m"  # middle
    else:
        temp += "r"  # right
    return temp
