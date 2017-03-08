from bs4 import BeautifulSoup
import urllib.request
import os, csv

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

    # Find first instance of 'ul' and give all of 'li' within that specific 'li'
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

    # major_courses= {}
    #
    # # Test for one major and parsing necessary information
    # for major_dict in degree_list.keys():
    #     print (major_dict)
    #     major_name = degree_list[major_dict]["Major"]
    #     major_link = degree_list[major_dict]["Link"]
    #     if major_link:
    #         major_courses[major_name] = readMajor(major_link)


    afrs_dict = degree_list["Africana Studies"]
    afrs_name = afrs_dict["Major"]
    afrs_link = afrs_dict["Link"]

# def readMajor(link):
#     """
#     :param link:string of major url
#     :return: list of courses
#     """
    # Standard Reading Major html
    readAFRShtml = urllib.request.Request(afrs_link,
                                          headers={'User-Agent': 'Mozilla/5.0'})

    readAFRS = urllib.request.urlopen(readAFRShtml).read()
    soupAFRS = BeautifulSoup(readAFRS, "lxml")

    # Find HTML tags with "div" with class as "tabs minimal hide-title cross-fade"
    div_AFRS = soupAFRS.findAll("div", class_="tabs minimal hide-title cross-fade")

    # After finding the all relevant "div" tag, find all "sections" within that tags
    sec_AFRS = div_AFRS[0].findAll("section")

    # TODO: Find better way to detect major requirements
    req_AFRS = sec_AFRS[2] # Third element

    # Find every tag "p", req_AFRS
    p_AFRS = req_AFRS.findAll("p")

    # Grab all the "a" so we can get courses
    cnt = 0
    required_tagsAFRS = []
    for p in p_AFRS:
        required_tagsAFRS.append(p.findAll('a', href=True))

    required_aTag = ([x for sublist in required_tagsAFRS for x in sublist])
    # required_tagsAFRS = p_AFRS[:2]
    # required_aTag = [x.findAll('a') for x in required_tagsAFRS]
    required_links = []

    for element in required_aTag:
        # for a in element:
        required_links.append(element["href"])

    print (required_links)
    courses = []

    for text in required_links:
        print (text.split("#"))
        if '#' in text :
            courses.append(text.split("#")[1].upper())

    print (courses)


if __name__ == "__main__":
    main()
