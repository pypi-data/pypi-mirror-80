""" Some comment here would be nice. """

def print_lol(the_list, indent=0):
    """ Print all elements from list and its all nested lists."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent+1)
        else:
            start_string = ""
            for i in range(0, indent):
                start_string = start_string + "  "
            print(start_string, each_item)
