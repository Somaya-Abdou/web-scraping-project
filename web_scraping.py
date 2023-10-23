import functions as f
        
def main(): 
    while 1 :
        try :
           year = int(input("Please enter year as YYYY \n"))  #gets the year from the user
        except ValueError :
           print("not a valid year")  
        else :    
           if year < 1900 or year > 2023 :
              print("not a valid year \n")
           else :
              break 

    while 1 :
        try :
          month = int(input("Please enter month as MM \n"))   #gets the month from the user
        except ValueError :
          print("not a valid month \n")  
        else :    
           if month < 1 or month > 12 :
              print("not a valid month \n")
           else :
              break 
      
    while 1 :
        try :
          day = int(input("Please enter day as DD \n"))       #gets the day from the user
        except ValueError :
          print("not a valid day")  
        else :    
          if day < 1 or day > 31 :
             print("not a valid day \n")
          else :
             break 
         
    if day <10 :        # to get the day in the website's format
       day = ("{}{}").format("0",str(day))
    if month < 10 :     # to get the month in the website's format
       month = ("{}{}").format("0",str(month))       
   
    date = ("{}-{}-{}").format(str(year),month,day)  
    championships,driver = f.url_request(date) 
    matches_details = f.all_teams(championships)
    driver.close()
    f.csv_upload(matches_details)
    
main()    