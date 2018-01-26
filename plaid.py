def make_empty_table():
    cell = [None] * 9
    table = [cell] * 9
    return table

def create_win_cons():
    '''Create a table of win cons.'''
    win_cons = []
    win_cons.append([0,1,2])
    win_cons.append([3,4,5])
    win_cons.append([6,7,8])
    win_cons.append([0,3,6])
    win_cons.append([1,4,7])
    win_cons.append([2,5,8])
    win_cons.append([0,4,8])
    win_cons.append([2,4,6])
    return win_cons