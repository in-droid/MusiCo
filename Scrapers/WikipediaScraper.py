from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup

# This function uses selenium to use Wikipedia's search bar to find an artist
# Input is the artist name and it outputs teh url of the page
# Afterwards we can use BeautifulSoup to scrape the page
# because it's faster as it takes the html content directly instead of going through a browser
def searchForArtist(artistName):
    # Download driver and change DRIVER_PATH !!!
    DRIVER_PATH = 'C:/Users/tofil/Downloads/chromedriver_win32/chromedriver.exe'
    options = Options()
    options.headless = True

    s = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=s, options=options)
    driver.get('https://wikipedia.org')

    # Get search bar and search for artist
    searchBar = driver.find_element(By.ID, 'searchInput')
    searchBar.send_keys(artistName)
    searchBar.submit()

    url = driver.current_url
    driver.close()
    return url


# This function checks whether the given page is a Disambiguation page or real wikipedia page,
# if it is not real it looks into the music section of the page and checks every link for our artist.
# This is important for artists like 'Kino' who have very basic band names
# Returns link to artist page or None.
def checkForArtist(albumList, URL):

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Check in cat links to see if in 'Disambiguation pages' section
    disambiguous_page = False
    try:
        cat_links = soup.find('div', {'id': "mw-normal-catlinks"}).find('ul').find_all('li')
        for link in cat_links:
            if 'disambiguation pages' in link.text.lower():
                disambiguous_page = True
                break
    except:
        print("No cat links found")

    # dodaj drugiot kod posle....
    if not disambiguous_page:
        return ScrapePage(URL,albumList)
    else:
        # find music section of disambigous page and get related links
        music_section = soup.find('span', {'id': 'Music'}).parent.find_next('ul').find_all('li')
        for i in music_section:
            link = i.find('a')['href']
            checkPage = ScrapePage('https://en.wikipedia.org' + link, albumList)
            if checkPage is not None:
                return checkPage

    return None


# This function scrapes a page to see if it is the artist's page.
# It first checks cat links to references to music, then checks whether a discography section is present,
# then if that holds it checks if any of the artist's albums is present on the page.
# Returns url of artist page if found, if not returns None.
# Not supposed to be called separately, only through checkForArtist().
def ScrapePage(URL, albumList):

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Check in cat links for references to 'music'
    is_musician = False
    try:
        cat_links = soup.find('div', {'id': "mw-normal-catlinks"}).find('ul').find_all('li')
        for link in cat_links:
            if ' music ' in link.text.lower() or ' musician ' in link.text.lower() \
                    or ' musicians ' in link.text.lower() or ' musical ' in link.text.lower():
                is_musician = True
                break
    except:
        print("No cat links found")

    # Check if discography is present in the heading spans
    discography_present = False
    try:
        discography = soup.find('span', {'id': 'Discography'})
        discography_present = True
    except:
        print("Discography not found")

    # if it is a musicians page and the discography section is present,
    # check if any of the artist's albums is present
    if is_musician and discography_present:
        # check if any studio album is in the page
        for album in albumList:
            if album.lower() in page.text.lower():
                return URL
    else:
        return None



#print(checkForArtist(['45'], searchForArtist('kino'))) #FOR TESTING

# To get the album list of the artist we call Ardit's spotify function first
