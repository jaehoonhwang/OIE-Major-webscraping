from bs4 import BeautifulSoup
import urllib.request
import os
import csv


def main():
    # Base URLs
    baseURL = 'https://www.fresnostate.edu'
    degree_programURL = '/academics/degrees-programs/'

    # Read html from urllib
    readhtml = urllib.request.Request(baseURL + degree_programURL,
                                      headers={'User-Agent': 'Mozilla/5.0'})

    # Open and read html and put it into BeautifulSoup
    r = urllib.request.urlopen(readhtml).read()
    soup = BeautifulSoup(r, "lxml")

    # Targeting "div class="main-content clearfix"
    # Other call for this one: soup.find_all('element', limit=n) | n=1
    div_mccf = soup.find('div', class_="main-content clearfix")

    # Find first instance of 'ul' and give all of 'li' within that specific
    # 'li'
    li_list = div_mccf.find_next('ul').find_all('li')

    # Create 'degree_list' to store text and href
    degree_list = {}

    # Store text and create its own dictionary
    for element in li_list:
        degree_list[element.text] = {"Major": element.text}

    # Store link with its respective dictionary name (if it exists)
    for element in li_list:
        if element.a and element.a.has_attr("href"):
            degree_list[element.text]["Link"] = baseURL + element.a["href"]
        else:
            degree_list[element.text]["Link"] = None

    # Test for one major and parsing necessary information
    for major_dict in degree_list.keys():
        major_name = degree_list[major_dict]["Major"]
        major_link = degree_list[major_dict]["Link"]
        if major_link:
            degree_list[major_dict]["Courses"] = readMajor(
                major_link, major_name)

    writeCSV("requiredcourses.csv", degree_list=degree_list)


def writeCSV(name, degree_list):
    with open(name, "w") as toWrite:
        writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
        writer.writerow(["Major", "Courses"])
        for major in degree_list.keys():
            if "Courses" in degree_list[major] and degree_list[major]["Courses"]:
                for required_courses in degree_list[major]["Courses"]:
                    writer.writerow([degree_list[major]["Major"],
                                     required_courses])
            else:
                writer.writerow([degree_list[major], "Error"])


def readMajor(link, major_name):
    """
    :param link:string of major url
    :return: list of courses
    """
    # Standard Reading Major html
    readAFRShtml = urllib.request.Request(link,
                                          headers={'User-Agent': 'Mozilla/5.0'})

    try:
        readAFRS = urllib.request.urlopen(readAFRShtml).read()
    except Exception:
        # print (major_name)
        return

    soupAFRS = BeautifulSoup(readAFRS, "lxml")

    # Find HTML tags with "div" with class as "tabs minimal hide-title
    # cross-fade"
    div_AFRS = soupAFRS.findAll(
        "div", class_="tabs minimal hide-title cross-fade")

    # After finding the all relevant "div" tag, find all "sections" within
    # that tags
    sec_AFRS = div_AFRS[0].findAll("section")

    # TODO: Find better way to detect major requirements
    req_AFRS = sec_AFRS[2]  # Third element

    # Find every tag "p", req_AFRS
    p_AFRS = req_AFRS.findAll("p")

    # Grab all the "a" so we can get courses
    required_tagsAFRS = []
    for p in p_AFRS:
        required_tagsAFRS.append(p.findAll('a', href=True))

    # Unmake the lists. (list of list -> list)
    required_aTag = ([x for sublist in required_tagsAFRS for x in sublist])
    required_links = []

    # Grab all link present in required_aTag
    for element in required_aTag:
        required_links.append(element["href"])

    courses = []

    # If link contains `#`, it means the course. Therefore, parse it and store
    # string after `#`.
    for text in required_links:
        if '#' in text:
            courses.append(text.split("#")[1].upper())

    return courses


if __name__ == "__main__":
    main()
