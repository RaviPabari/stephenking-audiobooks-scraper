import bs4 as bs
import requests
import os

class ScrapItBaby:
    def __init__(self):
        self.main_url = input("Please enter starting url for the audiobook : ")
        self.folder_name = input("\n\nPlease enter the name for the new folder where all files will be saved here in same directory : ")
        self.names = []
        self.pages = 0
        self.get_names()
        # self.write_names_to_txt()
        self.download_audio()
        
    def get_names(self):
        len_1 = len(self.names)
        print("Started scraping names of chapters of your audio book.....")
        for x in range(1,15):
            source = requests.get(self.main_url + str(x))
            soup = bs.BeautifulSoup(source.text, 'lxml')

            p_tag = soup.find_all("p",class_=None)

            for i in p_tag:
                i = str(i)
                if "href" not in i and "style" not in i and "Chapter" in i:
                    i = i.replace("<p>","")
                    i = i.replace("</p>","")
                    if(len(i)>60):
                        break
                    if i not in self.names:
                        self.names.append(i)
            len_2 = len(self.names)
            if len_1 == len_2:
                self.pages  = x
                break
            else:
                len_1 = len_2
            print("Chapters collected --> ",len(self.names))
        print("All chapters collected....")
        print(self.names)
    
    def write_names_to_txt(self):
        print("writing to chapters_names.txt.........")
        with open('chapters_names.txt','a') as file:
            for chapters in self.names:
                file.write(chapters)
                file.write('\n')
        file.close()
    
    def download_audio(self):
        print("\nDownloading your audiobook...\n")
        cc = 0
        for i in range(1,self.pages):
            os.system('youtube-dl '+self.main_url+str(i)+ " -A")
            books = []
            for x in os.listdir():
                if '.mp3' in x:
                    books.append(x)
            books.sort()

            for p in range(0, len(books)):
                os.rename(books[p],self.names[cc]+'.mp3')
                cc+=1
            os.system('mkdir ' + self.folder_name)
            os.system('mv *.mp3 ' + self.folder_name +'/')           
        print("\nDownloaded all your audiobook to" + self.folder_name + "....Have Fun")

if __name__ == '__main__':
    ScrapItBaby()