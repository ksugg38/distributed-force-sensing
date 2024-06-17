import xml.etree.ElementTree as ET
import pandas as pd


tree = ET.parse('twoDOFleg.xml')
root = tree.getroot()


# for child in root:
#     print(child.tag, child.attrib)


# for country in root.findall('country'):
#     rank = country.find('rank').text
#     name = country.get('name')
#     print(name, rank)

# for body in root.findall('worldbody'):
#     name = body.get('name')
#     print(name)


all_descendants = list(root.iter())
parent_map = {c: p for p in tree.iter() for c in p}

element_list = list()
parent_list = list()
tag_list = list()
text_list = list()


for element in all_descendants:
    element_list.append(str(element))
    parent_list.append(str(parent_map.get(element))
                       if element != root else "None")
    tag_list.append(element.tag)
    text_list.append(element.text)

data = {'Element': element_list,
        'Parent': parent_list,
        'Tag': tag_list,
        'Text': text_list}


df = pd.DataFrame(data)
print(df)
