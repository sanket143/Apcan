import re;
import pygame;
import requests;
import platform;
import threading;

from scan import scan;
from pygame.locals import *;
from bs4 import BeautifulSoup as bs;

CURRENT_URL = "http://intranet.daiict.ac.in/~daiict_nt01";

reserved = [
  "Name",
  "Last modified",
  "Size",
  "Description",
  "Parent Directory"
]

SEARCH_LINKS = [];

class Information:
  def __init__(self, text, href):
    self.text = text;
    self.href = href;

def getKeyword(screen):
  val = "";
  name = ""
  gotcha = False;
  font = pygame.font.SysFont("monospace", 15)

  while True:
    for evt in pygame.event.get():
      if evt.type == KEYDOWN:
        if evt.unicode.isalpha():
          name += evt.unicode

        elif evt.key == K_SPACE:
          name += " ";

        elif evt.key == K_BACKSPACE:
          name = name[:-1]

        elif evt.key == K_RETURN:
          val = name;
          name = "Loading...";
          gotcha = True;

      elif evt.type == QUIT:
        return
    
    screen.fill((0, 0, 0))
    block = font.render("Keyword: " + name + "_", True, (0, 255, 0))
    rect = block.get_rect()
    rect.center = screen.get_rect().center
    screen.blit(block, (0, 0))
    pygame.display.flip()
    if gotcha:
      break;

  return val;

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


def scan(search_query):
  bulkArr = [Information("/", "/")];
  while len(bulkArr):
    TraversalSequence = [];
    for node_dir in bulkArr:
      if("/" == node_dir.text[-1]):
        try:
          dirList = getURL(node_dir.href);
          output = [Information(node_dir.text + dirInfo.text, node_dir.href + dirInfo.href) for dirInfo in dirList];
          TraversalSequence = TraversalSequence + output;
          for j in output:
            if search_query.lower() in j.text.lower().split("/")[-1]:
              SEARCH_LINKS.append(j.text)
              print(j.text);
              
        except KeyboardInterrupt:
          exit();
        except:
          pass;
    bulkArr = TraversalSequence;

pygame.init();
myFont = pygame.font.SysFont("monospace", 15);
screen = pygame.display.set_mode((1000, 650))
done = False;
value = getKeyword(screen);
thread = threading.Thread(target=scan, args=(value,), kwargs={});
thread.start();
color = (255, 0, 0)
fontColor = (0, 255, 0);
x = 100;
y = 100;

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True;

  keyPressed = pygame.key.get_pressed();

  if keyPressed[pygame.K_UP]:
    y -= 1;

  if keyPressed[pygame.K_DOWN]:
    y += 1;

  if keyPressed[pygame.K_LEFT]:
    x -= 1;

  if keyPressed[pygame.K_RIGHT]:
    x += 1;

  screen.fill((0, 0, 0));
  textValue = myFont.render("Searching " + value + "...", True, fontColor);
  screen.blit(textValue, (0, 0));

  for link_n in range(len(SEARCH_LINKS)):
    textValue = myFont.render(SEARCH_LINKS[link_n] , True, fontColor);
    screen.blit(textValue, (0, 15 * (link_n + 1)));

  pygame.display.update();
