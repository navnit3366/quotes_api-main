from src.database import get_db
from src import models


def get_quotes(file_path):
    def split_authors(item):
        last_index = item.rfind(" – ")
        return [item[0:last_index], item[last_index + 3:]]

    def stripe_nums(item):
        text = item[0]
        text = text[text.find('.') + 2:]
        return [text, item[1]]

    db = next(get_db())

    quotes_list = []
    with open(file_path, 'r', encoding='utf-8') as quotes_file:
        quotes = quotes_file.read()
        quotes = quotes.split('\n')
        quotes = [quote for quote in quotes if quote]
        quotes = list(map(split_authors, quotes))
        quotes = list(map(stripe_nums, quotes))
        for quote in quotes:

            db_quote = {
                'content': quote[0],
                'author': quote[1],
                'language': 'en'
            }

            db_quote = models.Quote(**db_quote)

            quotes_list.append(db_quote)

        db.add_all(quotes_list)
        db.commit()
        print(f'Added {len(quotes)} quotes')


def main():
    get_quotes('quotes.txt')


if __name__ == "__main__":
    main()
