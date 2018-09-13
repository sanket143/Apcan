import requests
from bs4 import BeautifulSoup as bs

CURRENT_URL = "http://intranet.daiict.ac.in/~daiict_nt01"
TraversalSequence = [""];

reserved = [
  "Name",
  "Last modified",
  "Size",
  "Description",
  "Parent Directory"
]

class Information:
  def __init__(self, text, href):
    self.text = text;
    self.href = href;

def removeBloat(ele):
  if ele.text in reserved:
    return False;
  else:
    return True;

def getURL(item):
  url = CURRENT_URL + item;
  resp = requests.get(url);
  html = resp.content;

  soup = bs(html, "html.parser");
  temp = [Information(i.text, i.get("href")) for i in soup.find_all("a") if removeBloat(i)];
  temp = list(filter(removeBloat, temp));
  return temp;

bulkArr = [Information("/Lecture/", "/Lecture/")];
while len(bulkArr):
  TraversalSequence = [];
  for node_dir in bulkArr:
    if("/" == node_dir.text[-1]):
      try:
        dirList = getURL(node_dir.href);
        for dirInfo in dirList:
          print(dirInfo.text, dirInfo.href); 
        output = [Information(node_dir.text + dirInfo.text, node_dir.href + dirInfo.href) for dirInfo in dirList];
        TraversalSequence = TraversalSequence + output;
        for j in output:
          print(j.text)
      except:
        pass;
  bulkArr = TraversalSequence;

