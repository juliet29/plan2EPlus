# from icecream import ic

# from geomeppy import IDF
# from geomeppy.patches import EpBunch




##MARK: text editing 
def get_last_word(string):
  
    # split by space and converting 
    # string to list and
    lis = list(string.split(" "))
    
    # length of list
    length = len(lis)
    
    # returning last element in list
    return lis[length-1]


