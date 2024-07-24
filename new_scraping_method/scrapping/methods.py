import random

from common_words import words
from api_keys import keys


def get_method():
    return

def random_year():
    # range: 1950 - 199
    year = random
    return {"method": "year", "value": year}

def random_word():
    word = random.choice(words)
    return {"method": "word", "value": word}




def main():
    method = get_method()
    match method:
        case "year":
            return random_year()
        case "word":
            return random_word()

if __name__ == '__main__':
    main()



