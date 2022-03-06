from urllib.request import urlopen
from datetime import datetime
import re
import subprocess
import sys

#url is the url of pornhub you are looking for, remove the number of the page you are looking for, you might need to go onto page 2 for pagenum to appear
#Length_search is the length of the video you are looking for, in seconds..
url = "https://www.pornhub.com/video?c=492&max_duration=10&hd=1&page="
length_search = 318


def go(url):
    try:
        
        page = urlopen(url)
        html_bytes = page.read()
    except:
        return False
    
    a = str(html_bytes)
    durations = [a[m.start()+10:m.start() + 16] for m in re.finditer('duration', a)] 
    places  = [m.start() for m in re.finditer('duration', a)] 
    dictionary = dict(zip(places, durations))
    to_pop = []

    links = [a[m.start()+23:m.start() + 50] for m in re.finditer('view_video', a)] 
    places2  = [m.start() for m in re.finditer('view_video', a)] 
    videos = dict(zip(places2, links))
    for x in videos:
        if "title" not in videos[x]:
            to_pop.append(x)
        videos[x] = videos[x][:15]
    for x in to_pop:
        videos.pop(x)
    to_pop = []

    #Keeps only ones with videos in, and removes excess characters
    for x in dictionary:
        if ":" not in dictionary[x]:
            to_pop.append(x)
        dictionary[x] = dictionary[x].translate({ord(i): None for i in '>/<'})
    for x in to_pop:
        dictionary.pop(x)
        try:
            places2.remove(x)
        except:
            pass

    #Converts mins+seconds to seconds
    for x in dictionary:
        z = dictionary[x].split(":")
        dictionary[x] = int(z[0]) * 60 + int(z[1])
    

    hyperlinks = []
    duration = []
    for x in dictionary:
        temp = x
        while temp not in places2 and temp > 10:
            temp -= 1
        if temp > 11:
            hyperlinks.append(videos[temp])
            duration.append(dictionary[x])
    
    data = dict(zip(hyperlinks, duration))
    return data


def test(url):
    page = urlopen(url)
    html_bytes = page.read()
    a = str(html_bytes)
    place = a.find("property=\"video:duration\" conten")
    return int(a[place:place + 70].split(" ")[1].split("=")[1][1:][:-1])

with  open("output.txt", "w") as file:
	content = ""
	file.write(content)
	file.close()

with open("perfect.txt", "w") as file:
	content = ""
	file.write(content)
	file.close()


lcv = 1
done = []
while True:
    new_dict = go(url + str(lcv))
    if new_dict == False:
        print("this is everything")
        break
    to_write = []
    to_writeP = []
    for x in new_dict:
        length = int(new_dict[x])
        if abs(length - length_search) < 5 and str(x) not in done:
            done.append(str(x))
            if length == length_search :
                data = "length: " + str(length) + " " + "https://www.pornhub.com/view_video.php?viewkey=" + str(x) + " pagenum:" + str(lcv) + " PERFECT" + "\n"
                to_writeP.append(data)
                to_write.append(data)
                print(data[:-1])
            else:
                data = "length: " + str(new_dict[x]) + " " + "https://www.pornhub.com/view_video.php?viewkey=" + str(x) + " pagenum:" + str(lcv) + "\n"
                to_write.append(data)
            
    with  open("output.txt", "a") as file:
        file.writelines(to_write)
        file.close()
    with  open("perfect.txt", "a") as file:
        file.writelines(to_writeP)
        file.close()
    lcv = int(lcv) + 1