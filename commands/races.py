import os
import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode
import pandas as pd

PATH = r"D:\Coding\F1_Data_To_CSV\files"
result_file = os.path.join(PATH, "result.txt")

def clean_list(string):
    """
    Used for filter() to check any instance of ""
    """
    if string == "":
        return False
    return True

def get_races(year):
    """
    This will get the races held the year inputted and prompt the user to select their desired race
    Returns "if the user wants to stop", "url for the race", "race name"
    """
    url = f"https://www.formula1.com/en/results.html/{year}/races.html"
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    table = table.find_all(class_="dark bold ArchiveLink")

    races = {}
    print("Please the type the race you want to get or type 'quit' to exit\n")
    for race in table:
        gp = race.get_text(strip=True)
        href = "https://www.formula1.com" + race.get("href")
        races[unidecode(gp.lower())] = href
        print(gp)

    selection = unidecode(input().lower())
    while selection != "quit":
        if selection in races:
            return False, races[selection], selection

        print("Error: please enter a name in the list above\n")
        selection = unidecode(input().lower())
    return True, "", ""

def get_results(url):
    """
    Gets the race results from the specific grand prix that is inputted
    """
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    temp_table = soup.find("table")
    return temp_table.find_all("tr")

def create_txt(table):
    """
    Converts table into txt file, then formats the data for the csv,
    finally converts the txt file into a csv and deletes the txt file
    """
    text_file = open(result_file, "w", encoding="utf-8")
    for driver in table:
        temp_list = list(filter(clean_list, unidecode(driver.text).strip().split("\n")))
        temp_str = "\n".join(temp_list) + "\n"
        text_file.write(temp_str)
    text_file.close()

    with open(result_file, 'r', encoding="utf-8") as fin:
        data = fin.read().split("\n")

    print(data)
    formatted_str = data[0] + "," + data[1] + "," + data[2] + ","
    formatted_str += data[3] + "," + data[4] + "," + data[5]
    formatted_str += "," + data[6] + "\n"

    for index in range(7, len(data)):
        if(index+2)%9 == 2:
            formatted_str += data[index] + " "
        elif(index+2)%9 == 8:
            formatted_str += data[index] + "\n"
        elif(index+2)%9 != 4:
            formatted_str += data[index] + ","

    text_file = open(result_file, "w", encoding="utf-8")
    text_file.write(formatted_str)
    text_file.close()

def create_csv():
    """
    Converts the all the data into a csv
    """
    desired_year = -1
    while(desired_year < 1950 or desired_year > 2022 or desired_year == 0):
        desired_year = int(input("Please enter desired year between 1950-2022 or 0 to exit: "))
    if desired_year != 0:
        end_search, race_url, race = get_races(desired_year)
        if not end_search:
            table = get_results(race_url)
            create_txt(table)
            file_name = f"{desired_year}_{race}_results.csv"
            dataframe1 = pd.read_csv(result_file)
            dataframe1.to_csv(os.path.join(PATH, file_name),
                                index = None)
            os.remove(result_file)
