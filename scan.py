import requests
from bs4 import BeautifulSoup as bs
from anytree import Node, RenderTree

CURRENT_URL = "http://intranet.daiict.ac.in/~daiict_nt01"
intranet = Node("Lecture");
LOCATION = [intranet];

reserved = [
  "Name",
  "Last modified",
  "Size",
  "Description",
  "Parent Directory"
]

def getURL(locn):
  url = CURRENT_URL + "/" + "/".join([i.name for i in locn]);
  resp = requests.get(url);
  html = resp.content;

  soup = bs(html, "html.parser");
  return soup.find_all("a");


def addDIR(dir_names, node):
  dirList = [];
  for name in dir_names:
    if name.string not in reserved:
      dir_node = Node(str(name.string), parent=node);
      if "/" == name.string[-1]:
        isDirExist = True;
        dirList.append(dir_node);

  return dirList;


dirList = addDIR(getURL(LOCATION), intranet);

for dir_node in dirList:
  LOCATION.append(dir_node);
  dirList = addDIR(getURL(LOCATION), dir_node);
  LOCATION.pop();
  
"""
for child in intranet.children:
  print(child.name);
"""
for pre, fill, node in RenderTree(intranet):
  print("%s%s" % (pre, node.name));
