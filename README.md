This project is split into two python programs.  1 (TRACK.PY) and 2(TRACK_TREE.PY)
First TRACK.PY
Uses the following python packages
----------------------------------
os.path
urllib.request
json
datetime
matplotlib.pyplot
numpy
webbrowser
----------------------------------

This program asks the user to input an athlete's name. Said athlete must be in the dictionary of athletes in this program to work.
Then it asks the user to select a number corresponding to race options.
It then will share the results of that athlete's races at the choosen distance, the fastest time of the season, and a graph of their results over time
This info is saved into a html file and a link is provided at the end for the user to click on and view the nice output.

The information from the website comes in as a json which is then parsed.
At the end the information the user asks for is saved in an HTML report.


Second TRACK_TREE.py
Uses the following python packages
----------------------------------
os.path
urllib.request
json
datetime
matplotlib.pyplot
numpy
----------------------------------

This program asks the user to input an athlete's name. Then using a tree stucture, asks the user if they want the results of the 800. If they say yes it 
shares those results for that athlete. If they say no, it continues down the tree and asks if they want the 1600, then 3200, then 4x800, and finally. 4x400.


Note: webscrape_py was an early version uploaded just to show progress in this project. It is not final and should not be used as such.
