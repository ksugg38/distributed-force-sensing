# Katie Sugg
# Summer 2024 WVU REU Robotics

import xml.etree.ElementTree as ET
import pandas as pd

# This is a WIP file that extracts data from a MuJoCo xml file
# The geometry sizes need work


# Helper function
def str_to_pos(string):
    # Convert position into array
    string = string.split()
    # Convert each element to an integer
    return [float(x) for x in string]


# TODO
# need to send back the correct length/size depending on the orientation
# idk how to determine that yet
def get_size(geom):
    # size becomes array
    size = str_to_pos(geom.get('size'))
    # if geom.get('type') == "plane":
    #     print("cmmon")
    # elif geom.get('type') == "box":
    #     print("ughhh")
    # elif geom.get('type') == "cylinder":
    #     print("tube")
    # elif geom.get('type') == "sphere":
    #     print("ball")
    # elif geom.get('type') == "capsule":
    #     print("cap")
    # elif geom.get('type') == "ellipsoid":
    #     print('disk')
    return size


# Specifiy file path
file_path = 'twoDOFleg.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# Adds every element in order of file appearance
# Parents come before children because of MuJoCo xml nested nature
all_descendants = list(root.iter())

# Every parent child relationship
parent_map = {c: p for p in tree.iter() for c in p}

# Body dataset - element, name, pos, geom element
# Each row represents a body element
body_elements = []
body_name = []
body_pos = []
body_geom = []

# Joint dataset - elemet, name, pos, axis
# Each row represents a joint element
joint_elements = []
joint_name = []
joint_pos = []
joint_axis = []

# Represents the end effector as position array
end_eff = []

# Go through every element in MuJoCo xml file
for element in all_descendants:
    if element.tag == "body":
        # Add items to correct body list
        body_elements.append(str(element))
        body_name.append(element.get('name'))
        body_pos.append(str_to_pos(element.get('pos')))
        # body_geom.append(str(element.find('geom')))
        # TODO
        body_geom.append(str_to_pos(element.find('geom').get('size')))

    elif element.tag == "joint":
        # Add items to correct joint list
        joint_elements.append(str(element))
        joint_name.append(element.get('name'))
        joint_pos.append(str_to_pos(element.get('pos')))
        joint_axis.append(str_to_pos(element.get('axis')))

    elif element.tag == "site":
        end_eff = str_to_pos(element.get('pos'))


# Create datasets of the desired data
body_data = {'Element': body_elements,
             'name': body_name,
             'pos': body_pos,
             'gemo': body_geom}

body_df = pd.DataFrame(body_data)

joint_data = {'Element': joint_elements,
              'name': joint_name,
              'pos': joint_pos,
              'axis': joint_axis}

joint_df = pd.DataFrame(joint_data)

# make seprate csvs to load into kinematics bridge?

# just realized that geometry has the size for the theta I need
# TODO
# read up on what different number of sizes means

print(joint_df)
