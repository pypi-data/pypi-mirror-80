

def return_indices(l, elems):
    
    placeholder = []
    
    for elem in elems:
        
        placeholder.append(l.index(elem))
        
    return placeholder

def get_max_value_key(d):
    
    return max(d, key=d.get)

def get_min_value_key(d):
    
    return min(d, key=d.get)

   
def merge_dicts(dicts):
    super_dict = {}
    for d in dicts:
        for k, v in d.items():
            super_dict[k] = v
    return super_dict 

def remove_elems(source_list, remove_elements):
    
    return [elem for elem in source_list if elem not in remove_elements]