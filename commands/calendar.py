import os
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

PATH = r"files"
data_file = os.path.join(PATH, "data.txt")

def get_schedule(year):
    """
    Takes the current race results of the year imputted available from formula1.com
    and converts that data into a list
    ***If using the current year and the season hasn't finished, the data will only
    contain the races that have been finished and not the ones remaining
    """
    url = f"https://www.formula1.com/en/results.html/{year}/races.html"
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("div", class_="table-wrap")[0].get_text("\n", strip=True)

def create_txt(table):
    """
    Converts table into txt file, then formats the data for the csv,
    finally converts the txt file into a csv and deletes the txt file
    """
    text_file = open(data_file, "w", encoding="utf-8")
    text_file.write(table)
    text_file.close()

    with open(data_file, 'r', encoding="utf-8") as fin:
        data = fin.read().split("\n")

    formatted_str = data[0] + "," + data[1] + "," + data[2] + ","
    formatted_str += data[3] + "," + data[4] + "," + data[5] + "\n"

    for index in range(6, len(data)):
        if(index+2)%8 == 2:
            formatted_str += data[index] + " "
        elif(index+2)%8 == 7:
            formatted_str += data[index] + "\n"
        elif(index+2)%8 != 4:
            formatted_str += data[index] + ","

    text_file = open(data_file, "w", encoding="utf-8")
    text_file.write(formatted_str)
    text_file.close()

def create_csv():
    """
    Converts the all the html data into a csv
    """
    desired_year = 0
    while(desired_year < 1950 or desired_year > 2022):
        desired_year = int(input("Please enter desired year between 1950-2022: "))

    schedule = get_schedule(desired_year)
    create_txt(schedule)
    file_name = f"{desired_year}_season_results.csv"
    dataframe1 = pd.read_csv(data_file)
    dataframe1.to_csv(os.path.join(PATH, file_name),
                        index = None)
    os.remove(data_file)