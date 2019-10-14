# Daniel Ryaboshapka
#
#
# input format: 
#   ./folder
#       file
#       file
#       *could be folder*
#   ./*could be folder*
#       file
#       file
#
# output format: 
#   a list of 2 dicts: nodes and links (set of vertices and edges)
# 

import argparse
from copy import deepcopy

data = []

parser = argparse.ArgumentParser(description="Converts pre-specified input format to a list of 2 dicts for use with graphs.")
parser.add_argument('-f', dest="file", help="the input file this program reads from")
args = parser.parse_args()
f = None

# folder is group 1
# file is group 2 
def determine_values(filename):
    container = []
    folder = []
    nodes = []
    children = []
    count = 0
    # first, create the order, then find source/dest
    with open(filename, "r") as f: 
        #first line should be folder 
        for line in f:
            # is the input tabbed? the following is a child. 
            # add target and source
            line = line.replace("\n","")
            print(line)
            if line[0] is " ":
                line = line.replace(" ", "")
                print(line)
                # print(line)
                if line not in folder:
                    nodes.append(line)
                    children.append(line)
            else:
                if count > 0:
                    container.append(children)
                    children = []
                # print(line)
                folder.append(line)
                nodes.append(line)
            count = count + 1
    container.append(children)

    #scrub children that are folders
    return [folder, nodes, container]

def convert_to_dict(group):
    folder = group[0]
    nodes = group[1]
    container = group[2]
    dict_nodes = []
    dict_links = []
    group = "square"
    dict_setup = {}
    dict_setup2 = {}
    cluster = 0
    all_groups = []
    all_clusters = []
    node_copy = deepcopy(nodes)
    # easy step: build the nodes dictionary

    #identify directories and files
    all_groups.append("square")
    all_clusters.append(-1)
    # print(folder)
    del nodes[0]
    for node in nodes:
        check_length = -1 * len(node)
        check = False
        # if within the folder list, set to square and -1
        # print("WORKING NODE: %(node)s" % {"node": node})
        if node in folder:
            print("REMOVED DATA")
            node_copy.remove(node)
        else:
            print("WITHIN ELSE LOOP")
            count = 0
            while check == False and count < len(folder):
                print("WITHIN WHILE LOOP")
                repo = folder[count]
                print(node)
                print(repo[check_length:])
                print()
                if node == repo[check_length:]:
                    all_groups.append("square")
                    all_clusters.append(-1)
                    check = True
                count = count + 1
                    
            if not check:
                all_groups.append("circle")
                all_clusters.append(0)

    c = 0
    for node in node_copy:
        dict_setup = {"name": node, "group": all_groups[c], "cluster": all_clusters[c]}
        dict_nodes.append(dict_setup)
        c = c + 1
    # hard step: link the source to target
    counter = 0

    for child_group in container: 
        for child in child_group:
            child_index = node_copy.index(child)
            node_index = counter
            #set default value to 0
            dict_setup2 = {"source": child_index, "target": node_index, "value": 0}
            dict_links.append(dict_setup2)
        counter = counter + 1
    
    # print(dict_nodes)
    # print(dict_links)
    return {"nodes": dict_nodes, "links": dict_links}

            





# if args.file:
#     print("Reading file %(filename)s" % {"filename": args.file})
#     group = determine_values(args.file)
#     data = convert_to_dict(group)
# else:
#     group = determine_values("dict_test.txt")
#     data = convert_to_dict(group)
        


# def convert_to_dict():










# if __name__ == "__main__":
#     main()