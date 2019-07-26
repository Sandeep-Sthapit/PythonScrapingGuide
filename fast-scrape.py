from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
from itertools import repeat
from multiprocessing import Pool, Manager


globalURL = 'https://blockchain-expo.com/global/blockchain-speakers/'


# class to represent each scraped object.
class Speaker():
    def __init__(self, name, bio, url, logo, company, position, image, year, social, extra):
        self.name = name
        self.bio = bio
        self.url = url
        self.logo = logo
        self.company = company
        self.position = position
        self.image = image
        self.year = year
        self.social = social
        self.extra = extra
    # get dictionary from objects which later can be used to construct a dataframe for pandas
    def to_dict(self):
        return {
            'name': self.name,
            'bio': self.bio,
            'url': self.url,
            'logo': self.logo,
            'company': self.company,
            'position': self.position,
            'image': self.image,
            'year': self.year,
            'social': self.social,
            'extra': self.extra
        }


# getting the content into a variable
def getConnection(my_url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(my_url, headers=hdr)
    uClient = urlopen(req)
    rawdata = uClient.read()
    # close the content
    uClient.close()
    return rawdata

# getting the list of urls and saving it into a list of dictionary, which will be further scraped to get detailed information
def get_list(rawdata):
    linklist = []
    soupData = BeautifulSoup(rawdata, 'html.parser')
    container = soupData.find('div', {'class': 'wpb_wrapper'})
    sections = container.findAll('div', {'class': 'speaker_list'})
    print(len(sections))
    speakers = [{'year': 2019, 'data':sections[0]}, {'year': 2018, 'data':sections[2]}]

    for speakerItem in speakers:
        year = speakerItem.get('year', '')
        data = speakerItem.get('data', '')
        persons = data.findAll('div', 'speaker-expand clearfix')
        for person in persons:
            link = person.find('div', 'speaker-photo-expand').find('a')['href']
            link_item = {'year': year, 'url':link}
            linklist.append(link_item)
    return linklist

# all the scraped links are crawled and important information is stored in the passed list as an object defined by class Speaker
def get_details(url_item, list):
    name, bio, url, logo, companyname, position, image, year, social = '', '', '', '', '', '', '', '', ''
    url = url_item.get('url', '')
    year = url_item.get('year', '')
    rawdata = getConnection(url)
    soupData = BeautifulSoup(rawdata.decode('utf-8'), 'html.parser')
    banner = soupData.find('div', {'id': 'banner'})
    name = banner.find('h1', {'class': 'banner-title'}).get_text().strip()
    compdetail = banner.find('div', {'class': 'sbio-list'}).findAll('li')
    extra = [];
    social = ''
    if len(compdetail) > 0:
        position = compdetail[0].get_text().strip()
        companyname = compdetail[-1].get_text().strip()
    if len(compdetail) > 2:
        extra = compdetail[1:-2]
    image = banner.find('div', {'class': 'sbio-img'}).find('img')['src']
    logo = banner.find('div', {'class': 'company-img'}).find('img')['src']

    detail_container = soupData.find('div', {'class': 'single-speaker-cont'})
    bio = detail_container.find('div', {'class': 'sbio-text'}).get_text().strip()
    social_media = detail_container.find('div', {'id': 'social-icons'})
    print(name)
    if social_media is not None:
        social = []
        medias = social_media.findAll('li')
        for item in medias:
            social_platform = ''.join(item['class'])
            link = item.find('a')['href']
            social_dict = {'platform': social_platform, 'link': link}
            social.append(social_dict)
    print(social)
    speaker = Speaker(name, bio, url, logo, companyname, position, image, year, social, extra)
    list.append(speaker)

# function that uses the above function to get all the urls first, then create a manager which will create a list that can be consistent
# across multiple processes. Then the work is divided among 10 processes using starmap, and the results is obtained in the speakerlist
# After the completion, the work by processes is joined and a dataframe is returned using the list.
def get_speaker(url):
    rawdata = getConnection(url)
    urllist = get_list(rawdata)

    manager = Manager()
    speakerlist = manager.list()

    p = Pool(10)  # Pool tells how many at a time
    records = p.starmap(get_details, zip(urllist, repeat(speakerlist)))
    p.terminate()
    print('here')
    p.join()

    df_temp = pd.DataFrame.from_records([speaker.to_dict() for speaker in speakerlist])
    return df_temp

# __name__ == '__main__' is important in Windows machines as it ensures the script is being run directly not as a module. If it were 
# to run it on module, this process will lead to infinite succession of processes until the computer runs out of resources. This is 
# because Windows has no fork, and the multiprocessing module will start a new Python process and imports the calling module
if __name__ == '__main__':
    df = get_speaker(globalURL)
    df.to_csv('blockchain_expo_speakers_global.csv', index=False, encoding='utf-8')
