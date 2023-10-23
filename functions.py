from bs4 import BeautifulSoup
from selenium import webdriver
import time
import numpy
import csv

def url_request(date) :     # function to open the website and get first data 
    url = "https://www.sportinglife.com/football/fixtures-results/{}".format(date)
    driver = webdriver.Edge("msedgedriver.exe")
    driver.get(url)
    time.sleep(6)
    driver.maximize_window() # the page is enlarged to click on the right button 
    time.sleep(6)
    #height = driver.execute_script("return document.body.scrollHeight") (gets the height of the page)
    driver.execute_script("window.scrollTo(0,600)") # the page is scrolled down to click on the right button 
    time.sleep(6)
    button1 = driver.find_element_by_xpath('//img[@src="/img/Premium/Gold Caret.svg"]')
    button1.click()
    time.sleep(2)
    button2 = driver.find_element_by_css_selector('div.UserSettingsCss__SettingsItem-sc-1oe1q3t-7:nth-child(1) > label:nth-child(2) > span:nth-child(4)')
    button2.click()
    time.sleep(2)
    button3 = driver.find_element_by_css_selector('div.UserSettingsCss__SettingsItem-sc-1oe1q3t-7:nth-child(3) > label:nth-child(2) > span:nth-child(4)')
    button3.click()
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    championships = soup.find_all("li",{"class" :  "CompetitionList__CompetitionListItem-sc-1f2woz6-1"})
    return(championships,driver)

def all_teams(championships): # this function gets the desired data from the website 
    num_of_leagues = len(championships) 
    dict_1 = {}  
    matches_details = []
    matches_details_2 = []  
    scorers_A_list = []
    scorers_B_list = []
    for league in range(0,num_of_leagues,1):
        num_of_teams = len(championships[league].contents[0].find_all("h2"))
        for team in range(0,num_of_teams,2):
            league_name = championships[league].contents[0].find_all("h3")[0].text 
            team_A_name = championships[league].contents[0].find_all("h2")[team].text
            team_B_name = championships[league].contents[0].find_all("h2")[team + 1].text
            try :
                team_A_score = championships[league].contents[0].find_all("span",{"class":"ItemStyles__TeamScore-ci87zm-6"})[team].text.split()
            except :
                team_A_score = numpy.nan
            try :     
                team_B_score = championships[league].contents[0].find_all("span",{"class":"ItemStyles__TeamScore-ci87zm-6"})[team + 1].text.split()
            except :
                team_B_score = numpy.nan
            matches_details.append({"championship name" : league_name,
                                    "1st team name"     : team_A_name,
                                    "2nd team name"     : team_B_name,
                                    "1st team score"    : team_A_score,
                                    "2nd team score"    : team_B_score})

    for league in range(0,num_of_leagues,1):
        num_of_teams = len(championships[league].contents[0].find_all("h2"))        
        for team in range(0,int((num_of_teams)/2),1):
            teams = championships[league].contents[0].find_all("div", {"class" : "ItemStyles__TeamsContainer-ci87zm-1 dgVuvK"})       
            scorers_A_list.clear()
            scorers_B_list.clear()
            dict_1.clear()
            try :               
                scorers_A = teams[team].contents[1].find_all("span",{"class":"SummaryMatchEventsstyles__SummaryMatchEventsText-sc-1w0ef11-0 ermYup"})
                for i in scorers_A :
                    scorers_A_list.append(i.text) 
                #print(scorers_A_list)    
            except :
                scorers_A = numpy.nan
            try :                    
                scorers_B = teams[team].contents[3].find_all("span",{"class":"SummaryMatchEventsstyles__SummaryMatchEventsText-sc-1w0ef11-0 ermYup"})
                for i in scorers_B :
                    scorers_B_list.append(i.text)
            except :
                scorers_B = numpy.nan
            try :
                team_position_B = teams[team].find_all("span", {"class":"ItemStyles__TeamPosition-ci87zm-5 eYQjpa"})[1].text
            except:
                team_position_B = numpy.nan
            try :
                team_position_A = teams[team].find_all("span", {"class":"ItemStyles__TeamPosition-ci87zm-5 eYQjpa"})[0].text
            except:
                team_position_A = numpy.nan
            
            dict_1["scorers of team A"] =   scorers_A_list.copy() 
            dict_1["scorers of team B"] =   scorers_B_list.copy()
            dict_1["team A position"]   =   team_position_A
            dict_1["team B position"]   =   team_position_B
            matches_details_2.append(dict_1.copy())               
    for dict1,dict2 in zip(matches_details,matches_details_2) :
        dict1.update(dict2)
    return(matches_details)                                
      
def csv_upload(matches_details): # this function takes the data as dicts in alist called matches_details and download it as csv
    with open("Desktop\online_project\matches_results.csv",'w') as output_file:
        keys = matches_details[0]
        keys = keys.keys()
        dict_writer = csv.DictWriter(output_file,keys) #put keys of dict as a header
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)