from  selenium import webdriver
from termcolor import cprint
import time
import random
from selenium.webdriver.common.keys import Keys
import os.path

class Follow():
    def __init__(self):
        cprint('[*] Program başlatılıyor...','yellow')
        self.startBrowser()
        self.login()
        followingsList = self.getFollowings()
        ratioList = self.examineFollowings(followingsList)
        self.writer(ratioList)
        cprint("PROGRAM SONLANDIRILIYOR","yellow")
        cprint("...","red")
        time.sleep(1)
        cprint("..","green")
        time.sleep(1)
        cprint(".","blue")



    def startBrowser(self):
        driver_path = "lib\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(executable_path=driver_path,chrome_options=options)
        cprint('[+] Tarayıcı başlatıldı','green')

    def login(self):
        username = input("Kullanıcı adı: ")
        password = input("Şifre: ")
        cprint('[*] Giriş yapılıyor...','yellow')

        self.browser.get('https://instagram.com/accounts/login')
        time.sleep(3)

        username_page = self.browser.find_element_by_name("username")
        password_page = self.browser.find_element_by_name("password")
        username_page.send_keys(username)
        password_page.send_keys(password)
        loginBtn = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[4]/button/div")
        loginBtn.click()
        time.sleep(3)

        self.browser.get('https://instagram.com/'+username)
        time.sleep(2)

    def getFollowings(self):
        numFollows=(self.browser.find_element_by_xpath("//li[2]/a/span").text) 
        numFollowings=int(self.browser.find_element_by_xpath("//li[3]/a/span").text)
        print("Takipçi sayısı: "+(numFollows))
        print("Takip edilen kişi sayısı: "+str(numFollowings))
        
        followersLink = self.browser.find_element_by_css_selector(' ul > li:nth-child(3) > a')
        followersLink.click()
        time.sleep(2)
        followingsList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowingsInList = len(followingsList.find_elements_by_css_selector('li'))
    
        followingsList.click()
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowingsInList < int(numFollowings)):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(0.7)
            followingsList.click()
            numberOfFollowingsInList = len(followingsList.find_elements_by_css_selector('li'))
            
            
        count=1
        followings = []
        for user in followingsList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            countPrint = "{}. takipçi: ".format(count)
            cprint(countPrint+userLink,'blue'.format(count))
            count +=1
            followings.append(userLink)
            if (len(followings) == numFollowings):
                break
        return followings

    def examineFollowings(self,followingsList):
        possible_0=[]
        possible_30=[]
        possible_50=[]
        possible_70=[]
        possible_85=[]
        for following in followingsList:
            self.browser.get(following)
            time.sleep(1.5)

            followings=self.browser.find_element_by_xpath("//li[2]/a/span").text
            if ',' or '.' or 'k' or 'm' in followings:
                followings = followings.replace(',','')
                followings = followings.replace('.','')
                followings = followings.replace('k','')
                followings = followings.replace('m','000000')

            followers=self.browser.find_element_by_xpath("//li[3]/a/span").text
            if ',' or '.' or 'k' or 'm' in followers:
                followers = followers.replace(',','')
                followings = followings.replace('.','')
                followings = followings.replace('k','000')
                followings = followings.replace('m','000000')
            
            followers = int(followers)
            followings = int(followings)
            
            ratio = followings/followers

            if 0 < ratio < 0.1:
                possible_0.append(following)
                print(following + " 'geri takip olasılığı %0")

            elif 0.1 < ratio < 0.5:
                possible_30.append(following)
                print(following + " 'geri takip olasılığı %30")

            elif 0.5 >= ratio < 1.5:
                possible_50.append(following)
                print(following + " 'geri takip olasılığı %50")
            elif 1.5 >= ratio < 1.7:
                possible_70.append(following)
                print(following + " 'geri takip olasılığı %70")
            elif 1.7 >= ratio:
                possible_85.append(following)
                print(following + " 'geri takip olasılığı %85")
        
        return [possible_0,possible_30,possible_50,possible_70,possible_85]

    def writer(self,ratioList):

        save_path = "output\\"
        completeName = os.path.join(save_path,'percentage_0' +".txt")
        f = open(completeName, "a")
        for i in ratioList[0]:
            f.write(i)
        f.close()
        cprint("[+] geri takip olasılığı %0 olan kullanıcılar output/percantage_0.txt dosyasına kaydedildi.","green")

        completeName = os.path.join(save_path,'percentage_30' +".txt")
        f = open(completeName, "w")
        for i in ratioList[1]:
            f.write(i+"\n")
        f.close()
        cprint("[+] geri takip olasılığı %30 olan kullanıcılar output/percantage_30.txt dosyasına kaydedildi.","green")
    
        completeName = os.path.join(save_path,'percentage_50' +".txt")
        f = open(completeName, "w")
        for i in ratioList[2]:
            f.write(i+"\n")
        f.close()
        cprint("[+] geri takip olasılığı %50 olan kullanıcılar output/percantage_50.txt dosyasına kaydedildi.","green")
        
        completeName = os.path.join(save_path,'percentage_70' +".txt")
        f = open(completeName, "w")
        for i in ratioList[3]:
            f.write(i+"\n")
        f.close()
        cprint("[+] geri takip olasılığı %70 olan kullanıcılar output/percantage_70.txt dosyasına kaydedildi.","green")

        completeName = os.path.join(save_path,'percentage_85' +".txt")
        f = open(completeName, "w")
        for i in ratioList[4]:
            f.write(i+"\n")
        f.close()
        cprint("[+] geri takip olasılığı %85 olan kullanıcılar output/percantage_85.txt dosyasına kaydedildi.","green")

run = Follow()
