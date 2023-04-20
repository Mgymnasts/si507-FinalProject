import os.path
import urllib.request
import json
import pprint as pp
import datetime
import matplotlib.pyplot as plt
import numpy as np
import webbrowser


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

def get_meets(athlete, year='2022'):
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
    #print(meet_dict)

    for key in meet_dict.keys():
        dates_names.append(meet_dict[key])
    for entry in dates_names:
        x= entry.get('EndDate')
        y= x.split("-")[0]
        if y == year:
            meet_list.append({entry.get("MeetName"): entry.get("IDMeet")})
    return meet_list

def get_meet_dates(athlete, year='2022'):
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
    #print(meet_dict)

    for key in meet_dict.keys():
        dates_names.append(meet_dict[key])
    for entry in dates_names:
        x= entry.get('EndDate')
        x1 = datetime.datetime.fromisoformat(x)
        # date = month/date/year
        y= x.split("-")[0]
        if y == year:
            meet_list.append({x1.strftime("%Y-%m-%d"): entry.get("IDMeet")})
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

    Returns: a list of Tuples with Meet Names and 1600m times
    """
    times1600 = []
    for result in get_results(athlete):
        if result.get("EventID") == 52:
            times1600.append((result.get("Result"), result.get("MeetID")))
    return times1600

def get_3200(athlete):
    """
    Takes the json input of an athlete's info from athletic.net and returns the results of the 3200 meter races for the 2022 season
        Parameters:
    Inputs: athlete (a dictionary from the json file of all info for that athlete)

    Returns: a list of Tuples with Meet Names and 3200m times
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

    Returns: a list of Tuples with Meet Names and 4x800m times
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

    Returns: a list of Tuples with Meet Names and 4x400m times
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

    Inputs: A list of dictionaries of the meets run and their information and
            the list of tuples of (meet name, and time) for that distance.

    Return: A list of tuples of the meet name and time.
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

def pretty_results_dates(meets, distance_results):
    """
    Takes in the athlete info, the meets that are being considered (correct year) and the results of the
    relevant distance and then connects the time with the name of the meet. The return statement is a list
    of tuples of (meet dates, time) for that distance.

    Inputs: A list of the meets run and their information and
            the list of tuples of the time with the meet id.

    Outputs: A list of tuples of the meets dates and race times.
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
        try:
            t = race[0]
            t2 = convert_to_time(t)
            if t2 < convert_to_time(fastest[0]):
                fastest = race
            else:
                pass
        except:
                pass
    return fastest

def graph_progress(race_dets, title, png_name):
    """
    Take a list of tuples for whichever distance of races and the dates the occurred on and a graph of the race results

    Input:
    List of tuples of all the instances of a race at a specific distance
    Title for the graph

    Returns:
    a graph
    """
    xpoints = []
    ypoints = []
    if len(race_dets) > 1:
        for set in race_dets:
            if set[0] == "DNS" or set[0] == "DNF" or set[0].lower() == "scratch":
                pass
            else:
                y1 = set[0].strip("a").split(":")[0]
                y2 = set[0].strip('a"').split(":")[1].split(".")[0]
                y3 = set[0].strip('a"').split(".")[1]
                y = float(y1)*60 + float(y2) + float(y3)/100
                ypoints.append(y)
                xpoints.append(np.datetime64(set[1]))
        font1 = {'family':'serif','color':'blue','size':20}
        font2 = {'family':'serif','color':'darkred','size':15}
        plt.plot(xpoints, ypoints)
        plt.title(title, fontdict = font1)
        plt.xlabel("Date of the Race", fontdict = font2)
        plt.ylabel("Time in Seconds", fontdict = font2)
        plt.tick_params(axis='x', labelrotation=45)
        plt.tight_layout()

        full_png_name = os.path.join("reports", png_name)
        plt.savefig(full_png_name)
        plt.show()
    else:
        print(f"No graph available for {title}. Didn't run this event or only ran it once.")

def create_html(athlete_name, name, results_type, results, images):
    """ This function creates the report for the athlete and saves it as an html file. The report contains a header with the athlete's name, school, season, sport, and the
    school logo. Then adds a title, set of race results and a graph of those results based on what the user has asked this website to pull up. It is customizable so if you
    only searched 800 and 1600, then those are the only results displayed. If you search all the races, then all 5 are displayed.
    Inputs:
    athlete_name - a string name of the athlete
    name - a string, the compressed (no spaces) version of the athete's name - used for saving files
    results_type - a list of events that were searched for (i.e. 800, 1600, 3200)
    results - a list of tuples that share the meet name and race time)
    images - a list of links to the graphs

    Outputs:
    url_link - a string that is the url to the athelete's report
    """
    #Build the html string
    html_doc = ""
    html_prefix = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="styles.css">
        <title>Northville Track and Field</title>
    </head>
    <body>
    '''
    html_doc += html_prefix
    html_doc += '    <div class="header">\n'
    html_doc += '        <img class="logo" src="'+ "Mustangs.png" +'" alt="Mustang-Logo">\n'
    html_doc += '        <div class="header-text">\n'
    html_doc += '           <div class="athlete_name">'+ athlete_name.upper() +'</div>\n'
    html_doc += '           <div class="season_year">'+ "2022" +' Season</div>\n'
    html_doc += '           <div class="school">'+ "Northville HS" +'</div>\n'
    html_doc += '           <div class="sport">'+ "Track & Field" +'</div>\n'
    html_doc += '        </div>\n'
    html_doc += '    </div>\n'

    #Create the loops that fill in the rest of the html
    #First loop is the race type
    n = len(results_type)
    i = 0
    while i <n:
        html_doc+= '    <hr class="solid">'
        html_doc+= '    <div class="RaceTitle">' + results_type[i] + '</div>\n'
        html_doc+= '    <div class="Results">\n'

        #Loop for Races within that race type
        m = len(results[i])
        j=0
        while j<m:
            print(results)
            html_doc+= '        <div class="Result">\n'
            html_doc+= '            <div class="Place">' + results[i][j][1] + ': </div>\n'
            html_doc+= '            <div class="Time">' + results[i][j][0] + '</div>\n'
            html_doc+= '        </div>\n'
            j+=1

        html_doc+= '    </div>\n'

        #Graph
        html_doc+= '    <img class="graph" src="' + images[i] + '">\n'
        i+=1

    html_suffix = '''
    </body>
    </html>'''
    html_doc+= html_suffix
    #save html string as a file
    # assign directory
    output_directory = 'reports'
    output_file_name = name + ".html"
    url_link = output_directory + '/' + output_file_name
    f_out_path = os.path.join(output_directory, output_file_name)
    #if there is no current file in the directory, create one
    if not os.path.isfile(f_out_path):
        with open(f_out_path, "w", encoding='utf-8') as f_out:
            f_out.write(html_doc)
            f_out.close()
            print("File Written", f_out_path)
    #if there is a file, either leave it as it, or allow the user to update it with an overwrite
    else:
        print("file exists. Overwrite?", f_out_path)
        if input().upper()=='Y':
            with open(f_out_path, "w", encoding='utf-8') as f_out:
                f_out.write(html_doc)
                f_out.close()
                print("File Written", f_out_path)
        else:
            print("No File Written")
    return url_link

def main():
    #header infor for athletic.net
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
        }
    #url to access athletic.net 
    base_url = "https://www.athletic.net/api/v1/AthleteBio/GetAthleteBioData?athleteId="

    #dictionary of athlete name and athletic.net for team members that I want to be able to look up. 
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

    #asks the user for an athlete to search for. This program was build for NHS, so it only pulls NHS athletes that are in the dictionary above.
    a = True
    while a ==True:
        athlete_name = input("Which athlete do you want to search for?\n")
        try:
            for entry in athlete_info:
                if athlete_name.title() in entry.keys():
                    n = entry[athlete_name.title()]
                    website = base_url+n+web_type+level
                    print(website)
                    a = False
                    break
                else:
                    pass
        except:
            print("Sorry, check your spelling or try another athlete")

    name = athlete_name.replace(" ", "")

    filename = os.path.join(name + '.json')
    #creates a file of info for an athlete if it hasn't already been pulled down. If it has, it doesn't repeat the process (simple cache set up)
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

    #Saved Information that could be relevant in the future
    neededinfo = {"level": 4, "SchoolID": "12811"}
    #reads in the json data for analysis
    athlete = read_json(filename)
    #finds the meets info
    meets = get_meets(athlete)
    #finds the meet names with dates
    meet_dates = get_meet_dates(athlete)

    #This series of function calls gets the race results for an individual athlete
    eighthundredresults = get_800(athlete)
    eight100 = pretty_results(meets, eighthundredresults)
    eight100_dates = pretty_results(meet_dates, eighthundredresults)
    fastest800 = fastest(eight100)

    sixteenhundredresults = get_1600(athlete)
    sixteen100 = pretty_results(meets, sixteenhundredresults)
    sixteen100_dates = pretty_results(meet_dates, sixteenhundredresults)
    fastest1600 = fastest(sixteen100)

    thirtytwohundred = get_3200(athlete)
    thirtytwo100 = pretty_results(meets, thirtytwohundred)
    thirtytwo100_dates = pretty_results(meet_dates, thirtytwohundred)
    fastest3200 = fastest(thirtytwo100)

    fourbyeight = get_4x800(athlete)
    fourbyeight100 = pretty_results(meets, fourbyeight)
    fourbyeight100_dates = pretty_results(meet_dates, fourbyeight)
    fastest4x800 = fastest(fourbyeight100)

    fourbyfour = get_4x400(athlete)
    fourbyfour100 = pretty_results(meets, fourbyfour)
    fourbyfour100_dates = pretty_results(meet_dates, fourbyfour)
    fastest4x400 = fastest(fourbyfour100)

    results_type = []
    results = []
    images = []
    i = True
    while i == True:
        what_distance = int(input("\nWhat distance do you want to see results for? \n Enter 1 for the 800m, Enter 2 for the 1600m, Enter 3 for the 3200m, Enter 4 for the 4x800m Relay, or Enter 5 for the 4x400m Relay\n If you are done, please enter 0\n"))
        #This if, elif, else loop matches the user input of race info request to race results and graph. This info is then saved to enter in a report.
        if what_distance == 1:
            print(f"800 Results = {eight100}")
            results_type.append("800")
            results.append(eight100)
            print(f"800 Results with Dates = {eight100_dates}")
            print(f"Fastest 800 = {fastest800}")
            image_name = "images/" + name + "800.png"
            graph_progress(eight100_dates, "800m", image_name)
            images.append(image_name)
        elif what_distance == 2:
            print(f"1600 Results = {sixteen100}")
            results_type.append("1600")
            results.append(sixteen100)
            print(f"1600 Results with Dates = {sixteen100_dates}")
            print(f"Fastest 1600 = {fastest1600}")
            image_name = "images/" + name + "1600.png"
            graph_progress(sixteen100_dates, "1600m", image_name)
            images.append(image_name)
        elif what_distance == 3:
            print(f"3200 Results = {thirtytwo100}")
            results_type.append("3200")
            results.append(thirtytwo100)
            print(f"3200 Results with Dates = {thirtytwo100_dates}")
            print(f"Fastest 3200 = {fastest3200}")
            image_name = "images/" + name + "3200.png"
            graph_progress(thirtytwo100_dates, "3200m", image_name)
            images.append(image_name)
        elif what_distance == 4:
            print(f"4x800m Relay Results = {fourbyeight100}")
            results_type.append("4x800")
            results.append(fourbyeight100)
            print(f"4x800m Relay Results with Dates = {fourbyeight100_dates}")
            print(f"Fastest 4x800 Relay = {fastest4x800}")
            image_name = "images/" + name + "4x800.png"
            graph_progress(fourbyeight100_dates, "4x800m Relay", image_name)
            images.append(image_name)
        elif what_distance == 5:
            print(f"4x400m Relay Results = {fourbyfour100}")
            results_type.append("4x400")
            results.append(fourbyfour100)
            print(f"4x400m Relay Results with Dates = {fourbyfour100_dates}")
            print(f"Fastest 4x400m Relay = {fastest4x400}")
            image_name = "images/" + name + "4x400.png"
            graph_progress(fourbyfour100_dates, "4x400m Relay", image_name)
            images.append(image_name)
        elif what_distance > 5:
            print("We do not have results for your request")
        else:
            i = False
            print("Bye")
            break


    #Call the create_html function which nicely prints out a personalized report with graphs and gives back the url to the report
    addition = create_html(athlete_name, name, results_type, results, images)
    base = "file:///Users/meganwhitaker/Documents/Megan/umich/courses/SI507/FinalProject/Track/"
    url = base + addition
    webbrowser.open_new(url)

if __name__ == "__main__":
    main()