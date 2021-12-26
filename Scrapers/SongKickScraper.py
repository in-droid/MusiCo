import requests
from bs4 import BeautifulSoup

# This is a event class for easier grouping and formatting of all event information
class Event:
    def __init__(self, artist, date, eventLink, venue, venueLink):
        self.artist = artist
        self.date = date
        self.eventLink = "https://www.songkick.com/" + eventLink
        self.venue = venue
        self.venueLink = "https://www.songkick.com/" + venueLink


# This functions scrapes all the events from a particular location
# Returns list of Event objects consisting of all scraped events from the location
def scrapeAllEvents(LocationURL):

    page = requests.get(LocationURL)
    soup = BeautifulSoup(page.content, "html.parser")

    EventsList = []

    ##get event listing
    events = soup.select("li[class='event-listings-element']")
    for event in events:
        # get date of event
        date = event['title']

        # get the link to the event
        temp = event.find('a', {'class': 'event-link'})
        artistName = temp.text.strip()
        eventPage = temp['href'].strip()

        # get the link to the venue
        temp1 = event.find('a', {'class': 'venue-link'})
        venue = temp1.text.strip()
        venueLink = temp1['href'].strip()

        # create event
        EventsList.append(Event(artistName,date,eventPage,venue,venueLink))

    return EventsList


# This function finds the page of the location based on inputed city and country
# Returns link to location page
def findLocation(city, country):
    page = requests.get("https://www.songkick.com/session/filter_metro_area?utf8=%E2%9C%93&query="
                        +city.lower()+"+"+country.lower())

    soup = BeautifulSoup(page.content, "html.parser")

    ##find matching location
    parentDiv = soup.find('div', {'class': 'component filter-metro-area search'})
    linkToCityPage = parentDiv.find('ul').find('a')
    return "https://www.songkick.com/" + linkToCityPage['href'].strip()


# print(findLocation("ljubljana", "slovenia")) #FOR TESTING

# This function scrapes the event page of an event
# and returns all important information related to it in a dictionary
# Dictionary consists of keys lineUp - all bands performing at the event
#                             tickets - link to ticket vendor website, if not available returns that instead
#                             venueInfo - information on the venue street num city etc..
#                             additionalInfo - extra info sometimes on the site like door opening hours and price
#                             imgLink - link to the image of the artist performing
def scrapeEventPage(URL):

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        lineUpUnclean = soup.find('div', {'class': 'line-up'}).find_all('span')
        lineUp = {}
        for i in lineUpUnclean:
            lineUp[i.text.strip()] = "https://www.songkick.com" + i.find('a')['href']  # add to dictionary artist in lineup and link to their page
    except:
        lineUp = None

    venueInfo = soup.find('p', {'class': 'venue-hcard'}).text.strip()

    try:
        tickets = "https://www.songkick.com" + soup.find('div', {'id': 'tickets'}).find('a')['href'].strip()
    except:
        tickets = "Tickets not available yet"

    try:
        additionalInfo = soup.find('div', {'class': 'component additional-details'}).text.strip()
    except:
        additionalInfo = None

    try:
        imgLink = soup.find('div', {'class': 'profile-picture-wrapper'}).find('img')['data-src']
    except:
        imgLink = "majkati"

    eventPageDict = {
        'lineUp': lineUp,
        'tickets': tickets,
        'venueInfo': venueInfo,
        'additionalInfo': additionalInfo,
        'imgLink': imgLink
    }
    return eventPageDict


# print(scrapeEventPage("https://www.songkick.com/concerts/39559443-taake-at-orto")) #FOR TESTING

# This function scraoes the venue pages for location and upcoming events
# Returns a list of lists, each sublist contains [artist, date, link to event] in that order
def scrapeVenuePage(URL):

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    #These are probably not needed but iI'll leave them for now just in case
    #eventsCount = soup.find('p', {'class': 'events-count'}).text.strip()
    #location = soup.find('p', {'class': 'venue-hcard'}).text.strip()

    # go to calendar page of venue
    page = requests.get(URL+"/calendar")
    soup = BeautifulSoup(page.content, "html.parser")

    listingsUnclean = soup.find('ul', {'class': 'event-listings'}).find_all('p', {'class': 'artists summary'})
    listings = []
    for i in listingsUnclean:
        isCanceled = i.parent.find('strong', {'class': 'item-state-tag canceled'})
        if isCanceled is None:
            listings.append([i.text.strip(), i.parent['title'], i.parent.find('a')['href']])

    return listings

# print(scrapeVenuePage("https://www.songkick.com/venues/57284-orto")) #FOR TESTING