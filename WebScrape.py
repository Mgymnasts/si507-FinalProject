from bs4 import BeautifulSoup
import lxml
import os.path
import urllib.request
import json
import pprint as pp
from datetime import datetime
import time


def read_json(filepath, encoding='utf-8'):
    """Reads a JSON file and converts it to a Python dictionary.

    Parameters:
        filepath (str): a path to the JSON file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """
    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def get_meets(athlete):
    """
    Takes the json input of an Athlete's info from Athletic.net and parses through
    to find the meet names and event id numbers for meets in 2022. Could be changed for any year.

    Parameters:
    Inputs: athlete (a dictionary from the json file)

    Returns: a list of dictionaries of the meet name and meet id number

    """
    meet_list = []
    dates_names =[]
    meet_dict = athlete.get("meets")
    print(meet_dict)

    for key in meet_dict.keys():
        dates_names.append(meet_dict[key])
    for entry in dates_names:
        x= entry.get('EndDate')
        y= x.split("-")[0]
        if y == "2022":
            meet_list.append({entry.get("MeetName"): entry.get("IDMeet")})
    return meet_list

def get_results(athlete):
    """
    Inputs: athlete (a dictionary from the json file of all info for that athlete)
    Returns a list of dictionaries of race info
    """
    results_dict = []
    results_dict = athlete.get("resultsTF")
    return results_dict


def get_800(athlete):
    """
    Takes the json input of an athlete's info from athletic.net, as well as the list of dictionaries
    of meet names/meet id numbers and returns the results of the 800 meter races for the 2022 season
        Parameters:
    Inputs: athlete (a dictionary from the json file of all info for that athlete)

    Returns: a list of Tuples with Meet Names and 800m times
    """
    times800 = []
    for result in get_results(athlete):
        if result.get("EventID") == 4:
            times800.append((result.get("Result"), result.get("MeetID")))
    return times800

def get_1600(athlete):
    """
    Takes the json input of an athlete's info from athletic.net and returns the results of the 1600 meter races for the 2022 season
        Parameters:
    Inputs: athlete (a dictionary from the json file of all info for that athlete)

    Returns: a list of Tuples with Meet Names and 800m times
    """
    times1600 = []
    for result in get_results(athlete):
        if result.get("EventID") == 52: #and result.get("MeetID") in meetlist.values():
            times1600.append((result.get("Result"), result.get("MeetID")))
    return times1600

def get_3200(athlete):
    """
    Takes the json input of an athlete's info from athletic.net and returns the results of the 3200 meter races for the 2022 season
        Parameters:
    Inputs: athlete (a dictionary from the json file of all info for that athlete)

    Returns: a list of Tuples with Meet Names and 800m times
    """
    times3200 = []
    for result in get_results(athlete):
        if result.get("EventID") == 60: #and result.get("MeetID") in meetlist.values():
            times3200.append((result.get("Result"), result.get("MeetID")))
    return times3200

def get_4x800(athlete):
    """
    Takes the json input of an athlete's info from athletic.net and returns the results of the 4 x 800 meter races for the 2022 season
        Parameters:
    Inputs: athlete (a dictionary from the json file of all info for that athlete)

    Returns: a list of Tuples with Meet Names and 800m times
    """
    times4x800 = []
    for result in get_results(athlete):
        if result.get("EventID") == 39: #and result.get("MeetID") in meetlist.values():
            times4x800.append((result.get("Result"), result.get("MeetID")))
    return times4x800

def get_4x400(athlete):
    """
    Takes the json input of an athlete's info from athletic.net and returns the results of the 4 x 800 meter races for the 2022 season
        Parameters:
    Inputs: athlete (a dictionary from the json file)

    Returns: a list of Tuples with Meet Names and 800m times
    """
    times4x400 = []
    for result in get_results(athlete):
        if result.get("EventID") == 8: #and result.get("MeetID") in meetlist.values():
            times4x400.append((result.get("Result"), result.get("MeetID")))
    return times4x400

def pretty_results(meets, distance_results):
    """
    Takes in the athlete info, the meets that are being considered (correct year) and the results of the 
    relevant distance and then connects the time with the name of the meet. The return statement is a list
    of tuples of meet name, time.

    Inputs: A list of the meets run and their information and
            the list of tuples of the time with the meet id.
    """
    results_list = []
    for meet in meets:
        for key, value in meet.items():
            name = key
            meetid = value
            for result in distance_results:
                if result[1] == meetid:
                    results_list.append((result[0], name))
    return results_list

def convert_to_time(racetime):
    """
    Takes a string represenation of a racetime and breaks it into an integer

    Input: String of race time in the format ('#:#.#a')
    Returns: Integer (###)
    """
    race1 = racetime.strip("a")
    min_race1 = race1.split(":")[0]
    sec_race1 = (race1.split(":")[1]).split(".")[0]
    hund_race1 = (race1.split(":")[1]).split(".")[1]
    race_time = int(min_race1+sec_race1+hund_race1)
    return race_time

def fastest(racelist):
    """
    Take a list of tuples for whichever distance of races and returns a tuple of the fastest time
    and which meet that occurred at

    Input:
    List of tuples of all the instances of a race at a specific distance

    Returns:
    Tuple of the fastest race and the name of the meet where that occurred

    """
    fastest = ('25:25.25a', "")
    for race in racelist:
        t = race[0]
        t2 = convert_to_time(t)
        if t2 < convert_to_time(fastest[0]):
            fastest = race
        else:
            pass
    return fastest

def main():

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
        }

    base_url = "https://www.athletic.net/api/v1/AthleteBio/GetAthleteBioData?athleteId="


    athlete_info = [{'David Whitaker': '15714155'},
                    {'Brady Heron': '15714146'},
                    {'Brandon Latta': '15714149'},
                    {'Brock Malaikal': '15748733'},
                    {'Brendan Herger': '15979366'},
                    {'Ethan Powell': '17514447'},
                    {'Isaac Luebke': '15714150'},
                    {'Maximilian Potrzeba': '15714152'},
                    {'Nicholas Yaquinto': '12409091'},
                    {'Raunak Chattopadhyay': '15714142'},
                    {'Sohil Jayee': '15714147'}]
    web_type = '&sport=tf&'
    level = 'level=4'

    athlete_name = input("Which athlete do you want to search for?\n")
    try:
        for entry in athlete_info:
            if athlete_name in entry.keys():
                n = entry[athlete_name]
                website = base_url+n+web_type+level

                    #athlete_number = athlete_info.get(athlete_name)
                    #website = base_url+athlete_number+web_type+level
                print(website)
                break
            else:
                pass
    except:
        print("Sorry, check your spelling or try another athlete")

    name = athlete_name.strip()

    filename = os.path.join(name + '.json')

    if not os.path.isfile(filename):
        print('Downloading: ' + filename)
        try:
            request = urllib.request.Request(url=website, headers=hdr)
            response = urllib.request.urlopen(request)
            response_str = response.read().decode()
            f = open(filename, "w")
            f.write(response_str)
            f.close()
        except Exception as inst:
            print(inst)
            print('Encountered unknown error. Continuing.')
    else:
        print("File Already Downloaded")


    neededinfo = {"level": 4, "SchoolID": "12811"}

    athlete = read_json(filename)

    meets = get_meets(athlete)
    #pp.pprint(meets)
    #print(type(meets))

    try_results = get_results(athlete)
    # print(type(try_results))
    pp.pprint(try_results)

    eighthundredresults = get_800(athlete)
    eight100 = pretty_results(meets, eighthundredresults)
    pp.pprint(eight100)

    sixteenhundredresults = get_1600(athlete)
    sixteen100 = pretty_results(meets, sixteenhundredresults)
    pp.pprint(sixteen100)

    thirtytwohundred = get_3200(athlete)
    thirtytwo100 = pretty_results(meets, thirtytwohundred)
    pp.pprint(thirtytwo100)

    fourbyeight = get_4x800(athlete)
    fourbyeight100 = pretty_results(meets, fourbyeight)
    pp.pprint(fourbyeight100)

    fourbyfour = get_4x400(athlete)
    fourbyfour100 = pretty_results(meets, fourbyfour)
    pp.pprint(fourbyfour100)

    fastest1600 = fastest(sixteen100)
    fastest800 = fastest(eight100)
    fastest3200 = fastest(thirtytwo100)
    fastest4x400 = fastest(fourbyfour100)
    fastest4x800 = fastest(fourbyeight100)
    print(f"Fastest 800 = {fastest800}")
    print(f"Fastest 1600 = {fastest1600}")
    print(f"Fastest 3200 = {fastest3200}")
    print(f"Fastest 4x400 = {fastest4x400}")
    print(f"Fastest 4x800 = {fastest4x800}")


if __name__ == "__main__":
    main()