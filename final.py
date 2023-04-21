import requests
import json
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.relativedelta import relativedelta

CACHE_FILENAME = "cache.json"
# def search(title=None, publisher=None, developer=None): #todo: decide how search will work and fix
#     if title:
#         return {'search': title}
#     if publisher:
#         return {'publishers': publisher}

# term = search(title='Ocarina of Time')

# game_tree = \
#     ("Is it a Mario game?",
#         ("Super Mario Bros 3", None, None),
#         ("The legend of Zelda: Breath of the wild", None, None))

# def playLeaf(leaf):
#     """this function takes a tree leaf that it incorrectly guessed, and asks the user to 
#     tell them what they were thinking, and a question that will help them get it right next time.

#     Args:
#         leaf (tuple): a leaf that was incorrectly guessed.

#     Returns:
#         new_branch: an updated branch containing the new question, the new leaf, and the old
#         leaf.
#     """
#     missed_answer = input(f"This brings me great anguish. What were you thinking of?")
#     new_question = input(f"What question distinguishes between {leaf[0]} and {missed_answer}?")
#     question_answer = input(f"And what is the answer to that question for \'{missed_answer}\'?")
    
#     new_leaf = (missed_answer, None, None)
    
#     if question_answer == 'yes':
#         new_branch = (new_question, new_leaf, leaf)
#         # new_leaf = (new_question, (missed_answer, None, None), (leaf[0], None, None))
#     else:
#         # new_leaf = (new_question, (leaf[0], None, None), (missed_answer, None, None))
#         new_branch = (new_question, leaf, new_leaf)
    
#     return new_branch        


# def play(tree):
#     """
#     this function takes a tree. If it is an internal node, it will ask the question
#     and recursively call itself with the parameter depending on the user's response.
    
#     If it is a leaf, it will guess the item. If it is right, it returns the tree.
#     If it is wrong, it will call playLeaf() on the leaf and return the output.
    
#     args:
#         tree (tuple): a tree made of nested tuples 


#     Returns:
#         a tree (tuple), either the original tree if it guessed correctly the first time,
#         or an updated tree from the user's responses.
#     """
    
#     if tree[1] is None and tree[2] is None:
#         question = input(f"Is it {tree[0]}?") # if the tree is a leaf, guess the item in the leaf
#         if question == 'yes':
#             print('searching...')

#             return tree[0]
#         else:
#             return playLeaf(tree)
             
#     else:
#         question = input(tree[0]) # if the tree is internal, ask the question
#         if question == 'yes':
#             return (tree[0], play(tree[1]), tree[2])
#         elif question == 'no':
#             return (tree[0], tree[1], play(tree[2]))


# def saveTree(tree, treeFile):
#     """
#     this function accepts a tree and the handle of a file that is open for writing, 
#     and saves the tree in that file. If it is an internal node, it will put the question followed
#     by the possible answers as leaves.
    
#     args:
#         tree (tuple): a tree made of nested tuples 
#         treeFile (str): the file name to write 
#     """
#     try:
#         if tree[1] is None and tree[2] is None:
#             treeFile.write('Leaf\n')
#             treeFile.write(tree[0] + '\n')

#         else:
#             treeFile.write('Internal Node\n')
#             treeFile.write(tree[0] + '\n')
#             saveTree(tree[1], treeFile)
#             saveTree(tree[2], treeFile)
#     except:
#         saveTree(tree, treeFile)
        
# def play_again(tree):
#     """this function is called after the first play session. It will take the new tree
#     that the user made any changes to, and start a new game, this time asking all the new questions.

#     If the user says no, it will quit. It calls itself again until the user quits.
    
#     Args:
#         tree (tuple): a tree made of nested tuples
#     """
#     new_game = input('Would you like to play again?')
#     if new_game == 'yes':
#         new_tree = play(tree)
#         treeFile = open('cache.json', 'w')
#         saveTree(new_tree, treeFile)
#         treeFile.close()
#         play_again(new_tree)
#     else:
#         print('Bye bye.')
#         exit()




# stock api call
stock_url = "https://twelve-data1.p.rapidapi.com/time_series"

stock_headers = {
	"X-RapidAPI-Key": "71b706dc2cmsh0a68d124f9b0ceep10d3cdjsn5b395e47909d",
	"X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
}
querystring = {"symbol":"NTDOY","interval":"1day","start_date":"1995-01-01","end_date":"2023-03-31","format":"json"}
stock_response = requests.request("GET", stock_url, headers=stock_headers, params=querystring)
stock_data = json.loads(stock_response.text)

# closing = []
# for d in stock_data['values']:
#     close = {d['datetime']: F"${round(float(d['close']), 2)}"}
#     closing.append(close)

def plot_stock_prices(stock_prices, points):
    """This function plots stock prices over time and includes labeled points.

    Parameters:
    stock_prices (dict): A dictionary containing a list of dictionaries. Each nested dictionary contains 'datetime' and 'close' keys and their respective values.
    points (list): A list of dictionaries, with each dictionary containing 'date' and 'title' keys and their respective values.

    """
    # Create figure and subplot
    fig, ax = plt.subplots()

    # Create empty lists to store dates and prices
    dates = []
    prices = []

    # Loop through stock price data and extract dates and prices
    for data in stock_prices['values']:
        date_obj = dt.datetime.strptime(data['datetime'], '%Y-%m-%d')
        dates.insert(0, date_obj)
        prices.insert(0, round(float(data['close']), 2))

    # Plot stock prices
    ax.plot(dates, prices)

    # Loop through points and plot labeled points
    for point in points:
        date_obj = dt.datetime.strptime(point['date'], '%Y-%m-%d')
        if date_obj in dates:
            index = dates.index(date_obj)
            ax.plot(date_obj, prices[index], 'ro', label=point['title'])
            ax.annotate(point['title'], xy=(date_obj, prices[index]), xytext=(date_obj, prices[index] + 2),
                        ha='center', va='bottom', textcoords='offset points', fontsize=10)

    # Set x and y labels, title, and legend
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Price')
    ax.set_title('Nintendo Stock Price over Time')
    ax.legend()

    # Show plot
    plt.show()    
    
    
class Game:
    """
    A class representing a video game.

    Attributes:
    -----------
    title: str
        The title of the game.
    release: str
        The release date of the game in format (YYYY-MM-DD).
    platforms: list
        The gaming platforms the game is available on.
    esrb_rating: str
        The game's rating from the Entertainment Software Rating Board (ESRB), if available.
    genre: list
        The genre(s) of the game.
    reception: int
        The game's Metacritic score.

    Methods:
    --------
    stringy() -> str
        Returns a string representation of the game, including its title, release date, 
        gaming platforms, ESRB rating, genre(s), and Metacritic score.
    """
    
    def __init__(self, title=None, release=None, platforms=None, esrb_rating=None, reception=None, genre=None, json=None):
        if json:    
            self.title = json['name']
            self.release = json['released']
            self.platforms = []
            for co in json['platforms']:
                if co['platform']['name'] not in ['PC', 'iOS', 'Android', 'Linux', 'macOS']:
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
            
    def stringy(self):
        return f"{self.title}\n\t{self.release}\n\tFor: {self.platforms}\n\tRated: {self.esrb_rating}\n\tGenre: {self.genre}\n\tScore: {self.reception}\n"


def search_games(last_search=None):
    """this function asks the user for a search term, then calls the RAWG
    video game API to display results.


    Returns:
        the top 5 search results.
    """
    if last_search:
        term = last_search
    else:
        term = input("Enter a game to search for: ")
    
    # game api call
    rawg_key = 'ff728212679b43d3b900088557528855'
    url = f"https://rawg-video-games-database.p.rapidapi.com/games?key={rawg_key}"
    headers = {"X-RapidAPI-Key": "71b706dc2cmsh0a68d124f9b0ceep10d3cdjsn5b395e47909d","X-RapidAPI-Host": "rawg-video-games-database.p.rapidapi.com"}
    response = requests.request('GET', url, params={'search': term, "page_size": 5}, headers=headers)
    game_data = json.loads(response.text)
    game_results = (game_data['results'])
    # nintendo = ['NES', 'SNES', 'Nintendo 64', 'Gamecube', 'Wii', 'Wii U', 'Nintendo Switch', 'Game Boy', 'Game Boy Color', 'Game Boy Advance', 'Nindendo DS', 'Nintendo 3DS']
    # sony = ['PlayStation', 'PlayStation 2', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'PSP', 'PS Vita']
    # microsoft = ['Xbox', 'Xbox 360', 'Xbox One', 'Xbox Series S/X']
    # sega = ['Genesis', 'Game Gear', 'Dreamcast', 'SEGA Saturn', 'SEGA 32X']

    i = 1
    display = []
    for results in game_results:
        game = Game(json=results)
        display.append(game)
        print(f"{i}. {game.stringy()}")
        i += 1
        
    return display
            
            
            
def build_model():
    """This function will allow a user to select from the results
     which game to include in the model.
     
     Returns: (list) all the selected games to display with the stock prices.
    """
    global cache
    model = []
    while True:
        display = search_games()
        selection = input("Enter 1-5 to select a game, or enter 'quit': ")
        try:
            x = int(selection) - 1
            select = display[x]
            model.append(select)
            
            # # Check if game is already in cache
            # if select.title in cache:
                
            
            print(f"{select.title} has been added to the model.")
            new_search = input("Enter 'd' to display model, enter 's' to search again: ")
            if new_search == 'd':
                break
            else:
                continue
        except:
            print('input not understood.')
            break
        
    return model
    
def plot_games(model, stocks):
    """this funtion plots a game as a point on Nintendo's stock prices over time.

    Args:
        model (list) games to be included
        stocks (list): dicts containing Nintendo's closing stock price each day.
    """
    points = []
    for games in model:
        point = {'date': games.release, 'title': games.title}
        points.append(point)
        plot_stock_prices(stocks, points=points)


games = build_model()
plot_games(games, stock_data)


# def main():
#     """this function brings everything together and launches the game with play(),
#     saves the tree file with saveTree(), and asks the user to play again with play_again().
#     """
#     print('Welcome to 20 Questions!\n--------------------')
#     tree = play(game_tree)
#     games = build_model(tree)
#     plot_games(games, stock_data)
#     treeFile = open('cache.txt', 'w')
#     saveTree(tree, treeFile)
#     treeFile.close()
# main()
