import requests
import random


url = "https://api.npoint.io/72747f3291dd6ac2ec62"

data = requests.get(url).json()




def get_random_joke():
    random_index = random.randint(0, 10)
    joke_list = list(data[random_index].values())
    #joke_type = list(data[random_index].keys())
    joke_index = random.randint(0, len(joke_list[0])-1)
    return joke_list[0][joke_index]


print(get_random_joke())

