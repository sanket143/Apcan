from tkinter import *

class App:
  def __init__(self, master):
    scroll = Scrollbar(master)
    master.title("Apcan");
    master.geometry("670x443");
    firstFrame = Frame(master);
    firstFrame.pack();

    self.keywordLabel = Label(firstFrame, text="Keyword");
    self.keywordLabel.pack(side=LEFT);

    self.keyword = StringVar();
    self.keywordEntry = Entry(firstFrame, textvariable=self.keyword);
    self.keywordEntry.pack(side=LEFT, fill=X);

    self.printButton = Button(firstFrame, text="Search", command=self.logLinks);
    self.printButton.pack(side=LEFT);

    self.quitButton = Button(firstFrame, text="Quit", command=firstFrame.quit)
    self.quitButton.pack(side=LEFT);

    logFrame = Frame(master);
    logFrame.pack();

    self.log = "";
    self.logLabel = Label(logFrame, text="LOG");
    self.logLabel.pack(fill=X);

    self.statusBar = Label(master, text="Searching...", bd=1, relief=SUNKEN, anchor=W);
    self.statusBar.pack(side=BOTTOM, fill=X);

  def message(self):
    keyword = self.keywordEntry.get();
    print(keyword);
    self.statusBar.configure(text=keyword);
    self.logLinks;

  def logLinks(self):

    self.log += "\n" + self.keywordEntry.get();
    self.logLabel.configure(text=self.log);

root = Tk()
b = App(root);
root.mainloop();

