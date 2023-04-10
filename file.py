import requests
import json

# game api call
rawg_key = 'ff728212679b43d3b900088557528855'
url = f"https://rawg-video-games-database.p.rapidapi.com/games?key={rawg_key}"

headers = {
	"X-RapidAPI-Key": "71b706dc2cmsh0a68d124f9b0ceep10d3cdjsn5b395e47909d",
	"X-RapidAPI-Host": "rawg-video-games-database.p.rapidapi.com"
}

def search(title=None, publisher=None, developer=None): #todo: decide how search will work and fix
    if title:
        return {'search': title}
    if publisher:
        return {'publishers': publisher}

term = search(title='sonic 2')
response = requests.request('GET', url, params=term, headers=headers)
game_data = json.loads(response.text)
game_results = (game_data['results'])

# stock api call
stock_url = "https://twelve-data1.p.rapidapi.com/time_series"

stock_headers = {
	"X-RapidAPI-Key": "71b706dc2cmsh0a68d124f9b0ceep10d3cdjsn5b395e47909d",
	"X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
}
querystring = {"symbol":"NTDOY","interval":"1day","outputsize":"30","format":"json"}
stock_response = requests.request("GET", stock_url, headers=stock_headers, params=querystring)
print(stock_response.text)

    
    
    
class Game:
    def __init__(self, title=None, release=None, platforms=None, esrb_rating=None, reception=None, genre=None, json=None):
        if json:    
            self.title = json['name']
            self.release = json['released']
            self.platforms = []
            for co in json['platforms']:
                if co['platform']['name'] != 'PC':
                    self.platforms.append(co['platform']['name'])
            try:
                self.esrb_rating = json['esrb_rating']['name']
            except:
                self.esrb_rating = 'unavailable'
            self.genre = []
            for g in json['genres']:
                self.genre.append(g['name'])
            self.reception = json['metacritic']
        else:
            self.title = title
            self.release = release
            self.platforms = platforms
            self.esrb_rating = esrb_rating
            self.genre = genre
            self.reception = reception
            
    nintendo = ['NES', 'SNES', 'Nintendo 64', 'Gamecube', 'Wii', 'Wii U', 'Nintendo Switch', 'Game Boy', 'Game Boy Color', 'Game Boy Advance', 'Nindendo DS', 'Nintendo 3DS']
    sony = ['PlayStation', 'PlayStation 2', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'PSP', 'PS Vita']
    microsoft = ['Xbox', 'Xbox 360', 'Xbox One', 'Xbox Series S/X']
    

    
    def stringy(self):
        return f"{self.title}, ({self.release}) For: {self.platforms} Rated: {self.esrb_rating}. Genre: {self.genre} Score: {self.reception}"


# for results in game_results:
    
#     game = Game(json=results)
#     print(game.stringy())
    
