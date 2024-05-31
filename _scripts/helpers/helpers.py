def min_max_norm(val, min, max):
    return (val - min)/(max - min)



def get_last_word(string):
    # split by space and converting 
    # string to list and
    lis = list(string.split(" "))
    
    # length of list
    length = len(lis)
    
    # returning last element in list
    return lis[length-1]


