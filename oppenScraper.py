import time
import datetime
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText

url = "https://www.cineplex.com/movie/oppenheimer-the-imax-experience-in-70mm-film?ic=cpx_hp-moviegrid-en"

def sendEmail(subject, body, recipients, importance="High"):
    sender_email = "example@gmail.com"  # Replace with your Gmail address
    sender_password = "password"  # Replace with your Gmail App password, see here: 
    #https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Importance"] = importance

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

def oppenScrape(url):

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    counter = 0                    

    while True:
        try:
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %I:%M:%S %p")

            #click on tickets button
            buttonDivParent = driver.find_element(By.XPATH, "//button[@data-name='get-tickets']")
            print("\nFOUND TICKET BUTTON")
            buttonDivParent.click()
            print("CLICKED TICKET BUTTON\n")
            time.sleep(5)

            #click on date button
            dateBtn = driver.find_element(By.XPATH, "//button[@data-name='select-Date']")  
            print("\nFOUND DATE BUTTON")
            dateBtn.click()
            print("CLICKED DATE BUTTON\n")
            time.sleep(5)

            #click on saturday button
            satBtn = driver.find_element(By.XPATH, "//span[contains(@class, 'jss175 jss178 jss176') and contains(text(), 'July 29, 2023')]")
            print("\nFOUND SATURDAY DATE")
            satBtn.click()
            print("CLICKED SATURDAY DATE\n")
            time.sleep(5)

            #sanity check by seeing if Sauga is playing on the 29th, which it should be
            try:
                sauga = driver.find_element(By.XPATH, "//h4[contains(@class, 'jss132 jss138 jss133') and contains(text(), 'Cineplex Cinemas Mississauga')]")
                if sauga:
                    systemWorking = True
            except Exception as e:
                error_message = str(e)
                if "no such element: Unable to locate element" in error_message:
                    systemWorking = False

            recipients = ["example1@gmail.com", "example2@gmail.com"] #ist of email addresses to send the email
            #check if vaughan theatre is available
            try:
                vaughan = driver.find_element(By.XPATH, "//h4[contains(@class, 'jss132 jss138 jss133') and contains(text(), 'Cineplex Cinemas Vaughan')]")
                if vaughan:
                    print("\n\nFLOOD GATE HAS OPENED")
                    #send notification email
                    message_body = f"""
                    The movie 'Oppenheimer' is now available at Cineplex Cinemas Vaughan on July 29th.

                    https://www.cineplex.com/movie/oppenheimer-the-imax-experience-in-70mm-film?ic=cpx_hp-moviegrid-en

                    Buy tickets now!

                    Scraper status: {'Functional' if systemWorking else 'Down'}
                    
                    OppenScraperBot
                    """
                    sendEmail("Oppenheimer Available for July 29th", message_body, recipients, importance="High")                    
                break
            except Exception as e:
                error_message = str(e)
                if "no such element: Unable to locate element" in error_message:
                    counter = counter + 1
                    print("\n\nVaughan not available yet. Restarting again in 6 minutes. Counter: ", counter,  " Time: ", formatted_datetime)       
                    closeBtn = driver.find_element(By.ID, "meta-nav--close") #close the navbar to prepare for the next cycle
                    closeBtn.click()
                    #put a counter so that you dont get emails every 6 minutes and instead only get every hour
                    if counter == 10:
                        #send email to show the movie not found
                        message_body = f"""
                        Oppenheimer is NOT playing at Cineplex Cinemas Vaughan on July 29th.

                        https://www.cineplex.com/movie/oppenheimer-the-imax-experience-in-70mm-film?ic=cpx_hp-moviegrid-en

                        Scraper status: {'Functional' if systemWorking else 'Down'}
                        
                        OppenScraperBot"""
                        sendEmail("Oppenheimer NOT Found", message_body, recipients, importance="Low")
                        counter = 0                    
                    time.sleep(360) #wait 6 minutes before retrying
        except Exception as e:
            print("Error: ", e)
            break
    driver.quit()

oppenScrape(url)
