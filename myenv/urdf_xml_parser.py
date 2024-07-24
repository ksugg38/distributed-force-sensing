# Katie Sugg
# Summer 2024 WVU REU Robotics

import xml.etree.ElementTree as ET
import pandas as pd

# This is a WIP file that extracts data from a general URDF xml file
# Collecting joint data needs work.
# TODO: need to make sure the file doesnt have xacro elements


# Helper function
def str_to_pos(string) -> list:
    # Convert position into array
    string = string.split()
    # Convert each element to an integer
    return [float(x) for x in string]


# this does not support mesh
def get_size(geom) -> float | list[float]:
    geometry_type = None
    if geom.find('cylinder') is not None:
        # has length and radius
        # don't think you need radius
        geometry_type = float(geom.find('cylinder').get('length'))
    elif geom.find('box') is not None:
        # has 3 numbers
        # TODO: doesn't length/size depend on the orientation?
        # what to do?????
        geometry_type = str_to_pos(geom.find('box').get('size'))
    elif geom.find('sphere') is not None:
        # has radius
        geometry_type = 2*float(geom.find('sphere').get('radius'))
    return geometry_type


# Specifiy file path
file_path = './myenv/example_robot.urdf.xacro'
tree = ET.parse(file_path)
# Robot tag is root tag
root = tree.getroot()
all_descendants = list(root.iter())

# TODO
# Note for parsing: Joint links specifiy parent and child links.
# Need to make sure those are right before adding to list

# links - name, where to get theta from? geomtery in visual
link_elements = []
link_name = []
link_geom_element = []
link_size = []


# joint xyz is posiiton, axis is axis
# TODO
# These joints have limits - idk what to do with them
joint_elements = []
joint_name = []
joint_pos = []
joint_axis = []

# idk where end effector is
# TODO
end_eff = []


for element in all_descendants:
    # Adds links to list
    if element.tag == "link":
        # visual contains origin and geometry
        if (element.find("visual") is not None):
            link_elements.append(str(element))
            link_name.append(element.get('name'))
            geometry = element.find('visual').find('geometry')
            link_geom_element.append(str(geometry))
            # geometry has different elements for the shapes
            geometry_type = get_size(geometry)
            link_size.append(geometry_type)

    elif element.tag == "joint":
        joint_elements.append(str(element))
        joint_name.append(element.get('name'))
        joint_pos.append(str_to_pos(element.find('origin').get('xyz')))
        joint_axis.append(str_to_pos(element.find('origin').get('rpy')))


# Create datasets of the desired data
link_data = {'Element': link_elements,
             'name': link_name,
             'geom': link_geom_element,
             'size': link_size}

link_df = pd.DataFrame(link_data)

joint_data = {'Element': joint_elements,
              'name': joint_name,
              'pos': joint_pos,
              'axis': joint_axis}

joint_df = pd.DataFrame(joint_data)
print(joint_df)
