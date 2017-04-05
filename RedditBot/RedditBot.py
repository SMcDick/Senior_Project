import requests
from selenium import webdriver
import os
import re
import time
import random
import FakeNameGenerator
import csv
import bs4
import DBC
from selenium.webdriver.common.proxy import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
proxies = {
        }

#a = page.select('.commentarea')
'''for comments in e:
e = a[0].select('.entry')
    comments = comments.select('.md')
    print(comments[0].getText())'''
    #e[0].select('.score')[1].getText()
def get_num(x):
    try:
        return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
    except:
        return 0
def GetIp():
        return "IP Adress: {}".format(requests.get('http://icanhazip.com', proxies=proxies, headers=headers).text)
def UserNameCreator(FirstName=None, LastName=None):
    Usernames = []
    with open('Words.txt') as f:
        lines = f.read().splitlines()
    for i in range(150):
        Usernames.append('{}{}{}'.format(FirstName, LastName, random.choice(lines)))
    for i in range(150):
        Usernames.append('{}{}{}'.format(FirstName, random.choice(lines), LastName))
    for i in range(150):
        Usernames.append('{}_{}_{}'.format(FirstName, LastName, random.choice(lines)))
    for i in range(30):
        Usernames.append('{}{}{}{}'.format(FirstName, LastName, random.choice(lines), str(random.randint(0, 99999))))
    #Converts to unique username
    for i in range(75):
        Usernames.append(str(FirstName) + str(LastName))
    username = random.choice(Usernames)
    return username

def LoadUserAgentFromCSV(Location):
    UserAgentCSV = open(Location, 'r')
    UserAgentList = csv.reader(UserAgentCSV)
    RowOfUserAgent = [row for row in UserAgentList]
    UserAgent = [l[0] for l in RowOfUserAgent]
    random.shuffle(UserAgent)
    return UserAgent

def LoadUsernames(Location):
    userpass = []
    UserAgentCSV = open(Location, 'r')
    UserAgentList = csv.reader(UserAgentCSV)
    RowOfUserAgent = [row for row in UserAgentList]
    for names in RowOfUserAgent:
        userpass.append(names[:6])
    for user in userpass:
        if user[0] == user[1]:
            userpass.remove(user)
    return userpass

def GetNewIP():
    Command = 'sudo adb shell input tap 1300 1080'
    os.system(str(Command))
    for i in range(5):
        Command = 'sudo adb shell input keyevent 4'
        os.system(str(Command))
    Command = 'sudo adb shell input swipe 0 10 0 500'
    os.system(str(Command))
    Command = 'sudo adb shell input tap 1300 150'
    os.system(str(Command))
    Command = 'sudo adb shell input tap 1300 530'
    os.system(str(Command))
    time.sleep(5)
    Command = 'sudo adb shell input tap 1300 530'
    os.system(str(Command))
    print('newip')
    time.sleep(5)
    Command = 'sudo adb shell input tap 600 1700'
    os.system(str(Command))
    time.sleep(4)
    Command = 'sudo adb shell input tap 1300 1080'
    os.system(str(Command))
    print('turned on hotspot')
    time.sleep(20)
    
    Command = 'sudo service network-manager restart'
    os.system(str(Command))
    time.sleep(10)
    IP = GetIp()
    print(str(IP))
def DetectRepost(posts):
    #to be called from grab recent
    links = []
    for post in posts:
        try:
            e = post.select('.thumbnail')
            links.append(str(re.search("(?P<url>http?://[^\s]+)", str(e)).group("url"))[:-1])
        except:
            pass
    for link in links:
        url = 'http://karmadecay.com/{}'.format(link)
        res = requests.get(url, headers=headers)
        page = bs4.BeautifulSoup(res.text, "lxml")
        if 'No very similar images were found on Reddit.' in str(page):
            print('original')

        else:
            a = str(page).partition('Less similar images')[0]
            a = str(a).partition('very similar image')[2]
            reposturl = str(re.search("(?P<url>http?://[^\s]+)", str(a)).group("url"))[:-1] + '?sort=top'
            res = requests.get(reposturl, headers=headers)
            page = bs4.BeautifulSoup(res.text, "lxml")
            a = page.select('.commentarea')
            e = a[0].select('.entry')
            for comments in e:
                try:
                    score = comments.select('.score')[1].getText()
                    comments = comments.select('.md')[0].getText().replace('\n', "")
                    print(comments + ' | ' + str(score))  
                except:
                    pass


    
def GrabRecent(subreddit):
    posts = []
    url = 'https://www.reddit.com/r/{}'.format(subreddit)
    res = requests.get(url, headers=headers)
    page = bs4.BeautifulSoup(res.text, "lxml")
    links = page.select('.link')
    #print(links[9])
    for i in range(len(links)):
        t = links[i].select('a')
        #print('\n[{}] {} - {}'.format(str(i), t[1].getText()[:100], t[4].getText()))
        #print(t[5].get('href'))
        upvotes = links[i].select('div')
        a = upvotes[0].getText()[1]
        posts.append([t[1].getText()[:100], t[4].getText(), t[5].get('href'), str(get_num(upvotes))])
    DetectRepost(links)
    return posts
def login(username, password):
    """
    Logs in to reddit and creates a requests Session to use for
    follow-up requests via this object
    
    :param str username: username to login with
    :param str password: password to login with
    """
    self.session = requests.Session()
    self.login_payload['user'] = username
    self.login_payload['passwd'] = password
    url = self.login_url + username
    while True:
        r = self.session.post(url, headers=self.hdrs, data=self.login_payload)
        if r.status_code != 200:
            continue
        if r.json()['json']['errors']:
            raise Exception(r.json()['json']['errors'])
        self.modhash = r.json()['json']['data']['modhash']
        return
def CreateAccounts():
    UserAgent = LoadUserAgentFromCSV('UserAgent.csv')
    UsernameDatabase = LoadUsernames('redditusernames.csv')
    for Usernames in UsernameDatabase:
        print(str(Usernames))
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", random.choice(UserAgent))
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", "108.59.14.208")
        profile.set_preference("network.proxy.http_port", 13010)
        profile.update_preferences() 
        driver = webdriver.Firefox(profile)
        driver.get('http://reddit.com')
        driver.find_element_by_link_text("Log in or sign up").click()
        time.sleep(1)
        driver.find_element_by_id("user_reg").click()
        driver.find_element_by_id("user_reg").send_keys(str(Usernames[0]))
        driver.find_element_by_id("passwd_reg").click()
        driver.find_element_by_id("passwd_reg").send_keys(str(Usernames[1]))
        driver.find_element_by_id("passwd2_reg").click()
        driver.find_element_by_id("passwd2_reg").send_keys(str(Usernames[1]))
        driver.find_element_by_id("email_reg").click()

        '''CompletedUsernamesDoc = 'CompletedUsernames.csv_' + str(random.randint(999, 999999))
        CompletedUsernames = open(CompletedUsernamesDoc, 'a')
        WritingCSV = csv.writer(CompletedUsernames)
        WritingCSV.writerow(Usernames)
        CompletedUsernames.close()
'''


def CreateHotmail(Proxy=None):
    for i in range(5):
        Firstname = FakeNameGenerator.FirstName()
        Lastname = FakeNameGenerator.LastName()
        Membername = UserNameCreator(Firstname, Lastname)
        Password = FakeNameGenerator.Password()
        PhoneNumber = FakeNameGenerator.PhoneNumber()
        UserAgent = LoadUserAgentFromCSV('UserAgent.csv')
        UsernameDatabase = LoadUsernames('redditusernames.csv')
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", random.choice(UserAgent))
        profile.set_preference("network.proxy.type", 1)
        if Proxy is not None:
            profile.set_preference("network.proxy.http", "108.59.14.208")
        profile.set_preference("network.proxy.http_port", 13010)
        profile.update_preferences() 
        driver = webdriver.Firefox(profile)
        driver.get('https://signup.live.com')
        time.sleep(2)
        screenshot = 'screenshot{}.png'.format(i)
        driver.save_screenshot(screenshot)
        driver.find_element_by_id("FirstName").send_keys(str(Firstname))
        driver.find_element_by_id("LastName").send_keys(str(Lastname))
        driver.find_element_by_id("Password").send_keys(str(Password))
        time.sleep(2)
        driver.find_element_by_id("Country").click()
        driver.find_element_by_css_selector("option[value=\"US\"]").click()
        driver.find_element_by_id("Country").click()
        time.sleep(1)
        driver.find_element_by_id("BirthMonth").click()
        time.sleep(1)
        driver.find_element_by_css_selector('option[value=\"{}\"]'.format(str(random.randint(1,12)))).click()
        time.sleep(1)
        driver.find_element_by_id("BirthMonth").click()
        time.sleep(1)
        driver.find_element_by_id("BirthDay").click()
        driver.find_element_by_css_selector("#BirthDay > option[value=\"{}\"]".format(str(random.randint(1,28)))).click()        
        driver.find_element_by_id("BirthDay").click()
        driver.find_element_by_id("BirthYear").click()
        driver.find_element_by_css_selector('option[value=\"{}\"]'.format(str(random.randint(1950,1994)))).click()
        driver.find_element_by_id("BirthYear").click()
        driver.find_element_by_id("Gender").click()
        driver.find_element_by_css_selector("#Gender").click()
        driver.find_element_by_css_selector("option[value=\"{}\"]".format(random.choice(['u', 'f', 'm']))).click()
        driver.find_element_by_css_selector("#Gender").click()
        driver.find_element_by_css_selector('.input-max-width').click()

        Captcha = DBC.DetectCaptcha(screenshot)
        for e in range(3):
            Text = DBC.solve_captcha(Captcha)
            if str(Text) != 'None':
                break
            else:
                print("DBC returned None")
        
        driver.find_element_by_css_selector('.input-max-width').send_keys(str(Text))
        time.sleep(1)
        driver.find_element_by_id("liveEasiSwitch").click()
        time.sleep(2)
        driver.find_element_by_id("MemberName").send_keys(str(Membername))
        driver.find_element_by_id("RetypePassword").click()
        time.sleep(3)
        driver.find_element_by_id("RetypePassword").send_keys(str(Password))
        driver.find_element_by_css_selector('#PhoneNumber').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#PhoneNumber').send_keys(PhoneNumber)
        driver.find_element_by_id("iAltEmail").click()
        driver.find_element_by_css_selector("#iAltEmail").send_keys('{}@{}.com'.format(Membername, random.choice(['gmail', 'yahoo', 'rocketmail'])))

        time.sleep(random.randint(3,7))
        driver.find_element_by_css_selector('#CredentialsAction').click()
        print('{} - {} - {}'.format(i, Membername, Password))

def Verify():
    for i in range(10):
        try:
            driver.find_element_by_css_selector("div.nextButton > img").click()
            time.sleep(1)
        except:
            break
    time.sleep(30)
    driver.find_element_by_css_selector("div.goButton").click()
    time.sleep(15)



#PhoneNumber

'''
    driver.find_element_by_id("MemberName").click()
    driver.find_element_by_id("user_reg").send_keys(str(Usernames[0]))
    driver.find_element_by_id("passwd_reg").click()
    driver.find_element_by_id("passwd_reg").send_keys(str(Usernames[1]))
    driver.find_element_by_id("passwd2_reg").click()
    driver.find_element_by_id("passwd2_reg").send_keys(str(Usernames[1]))
    driver.find_element_by_id("email_reg").click()


driver.find_element_by_id("MemberName").click()


try: self.assertTrue(self.is_element_present(By.ID, "Country"))
except AssertionError as e: self.verificationErrors.append(str(e))

try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "option[value=\"US\"]"))
except AssertionError as e: self.verificationErrors.append(str(e))
'''


#DBC.solve_captcha('capcha.jpeg')