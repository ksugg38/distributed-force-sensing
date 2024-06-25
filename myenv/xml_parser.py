import xml.etree.ElementTree as ET
# import pandas as pd

file_path = 'twoDOFleg.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# Every single element
# Adds in order of file appearance
# So parents come before children
all_descendants = list(root.iter())
# print(all_descendants)

# Every parent child relationship
parent_map = {c: p for p in tree.iter() for c in p}
# print(parent_map)

# the elements need to be collected in the right order
# Or else everything will be wrong
body_elements = []
joint_elements = []
end_eff = []

for element in all_descendants:
    if element.tag == "body":
        body_elements.append(element)
    elif element.tag == "joint":
        joint_elements.append(element)
    elif element.tag == "site":
        end_eff.append(element)

# for this example, there are 3 bodies and 2 joints
# should a [0 0 0] joint axis and posiiton be added?
print(body_elements)
print(joint_elements)
print(end_eff)


# get theta from body geometry element
# get joint position and axes from joint

# initalize 2D array
body_table = [[0]*2 for i in range(len(body_elements))]
