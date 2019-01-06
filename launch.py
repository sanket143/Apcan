from tkinter import *
from bs4 import BeautifulSoup as bs;

import re;
import requests;
import threading;

class Information:
  def __init__(self, text, href):
    self.text = text;
    self.href = href;

class ScanThread(threading.Thread):
  def __init__(self):
    super(ScanThread, self).__init__();
    self._stop_event = threading.Event();

class App:
  def __init__(self, master):
    self.CURRENT_URL = "http://intranet.daiict.ac.in/~daiict_nt01";
    self.reserved = [
      "Name",
      "Last modified",
      "Size",
      "Description",
      "Parent Directory"
    ]
    self.SEARCH_LINKS = [];

    master.title("Apcan");
    master.geometry("670x443");
    self.firstFrame = Frame(master);
    self.firstFrame.pack();

    self.keywordLabel = Label(self.firstFrame, text="Keyword");
    self.keywordLabel.pack(side=LEFT);

    self.keyword = StringVar();
    self.keywordEntry = Entry(self.firstFrame, textvariable=self.keyword);
    self.keywordEntry.bind("<Return>", (lambda event: self.search()));
    self.keywordEntry.pack(side=LEFT, fill=X);

    self.printButton = Button(self.firstFrame, text="Search", command=self.search);
    self.printButton.pack(side=LEFT);

    self.quitButton = Button(self.firstFrame, text="Quit", command=self.quit)
    self.quitButton.pack(side=LEFT);

    logFrame = Frame(master);
    logFrame.pack(fill=BOTH, expand=1);

    yscrollbar = Scrollbar(logFrame);
    yscrollbar.pack(side=RIGHT, fill=Y);

    self.listbox = Listbox(logFrame, yscrollcommand=yscrollbar.set);

    self.listbox.pack(fill=BOTH, expand=1);
    yscrollbar.config(command=self.listbox.yview);

    self.statusBar = Label(master, text="Nothing to Search...", bd=1, relief=SUNKEN, anchor=W);
    self.statusBar.pack(side=BOTTOM, fill=X);

  def quit(self):
    self.firstFrame.quit;
    exit();

  def removeBloat(self, ele):
    if ele.text in self.reserved:
      return False;
    else:
      return True;

  def getDirs(self, items):
    if items.text[-1] == "/":
      return True;
    else:
      return False;

  def getData(self, node_dir):
    url = self.CURRENT_URL + node_dir.href;
    resp = requests.get(url);
    html = resp.content;
    soup = bs(html, "html.parser");
    dirList = [Information(i.text, i.get("href")) for i in soup.find_all("a") if self.removeBloat(i)];
    dirList = list(filter(self.removeBloat, dirList));

    output = [Information(node_dir.text + dirInfo.text, node_dir.href + dirInfo.href) for dirInfo in dirList];
    dirs = list(filter(self.getDirs, output));

    # Start Daemon Thread before printing
    threading.Thread(target=self.scan, args=(dirs,), daemon=True).start();

    for _f in output:
      # check for dirs
      if "/" == _f.text[-1] and self.keyword.lower() in _f.text.lower().split("/")[-2]:
        self.addLink(self.CURRENT_URL + _f.text);

      elif self.keyword.lower() in _f.text.lower().split("/")[-1]:
        self.addLink(self.CURRENT_URL + _f.text);

  def scan(self, node_dirs):

    for node_dir in node_dirs:
      try:
        dirList = self.getData(node_dir);
      except:
        print("Error Occured: ", node_dir.text);

  def fastSearch(self):
    root = Information("/" ,"/");
    self.getData(root);

  def search(self):
    self.keyword = self.keywordEntry.get();

    self.scanThread = threading.Thread(target=self.fastSearch, daemon=True);
    self.scanThread.start();
    self.updateStatus("Searching " + self.keyword + "...");

  def updateStatus(self, status):
    self.statusBar.configure(text=status);   

  def addLink(self, link):
    self.listbox.insert(0, link);
    self.updateStatus(str(self.listbox.size()) + ": " + link);

root = Tk()
b = App(root);
root.mainloop();
