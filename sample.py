import time
from squeue import enqueue_item, dequeue_item
from utils import make_request, logging
from models import db_session, NoResultFound, Item, Keyword

def search(keyword):
    logging.info(u"Searching for keyword: {}".format(keyword))
    
    try:
        _ = db_session.query(Keyword).filter(Keyword.keyword==keyword).one()
    except NoResultFound:
        _ = Keyword(keyword=keyword).save()

    furl = "https://scrapethissite.com/pages/forms/?q={}".format(keyword)
    page = make_request(furl)

    for _ in page.find_all("tr", "team"):
        i = Item()
        i.url = furl
        i.save()
        print(i.to_dict())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keyword", help="Manually specify a one-off keyword to search for.", type=str)
    parser.add_argument("-f", "--file", help="File path to a newline-deliniated list of keywords. ex: 'input/keywords.csv'", type=str)
    parser.add_argument("-w", "--worker", help="Create a worker that takes keywords off the queue", action='store_true')
    args = parser.parse_args()

    if args.keyword:
        search(args.keyword)

    elif args.file:
        with open(args.file, 'r') as f:
            for line in f:
                enqueue_item("keywords", line.strip())

    elif args.worker:
        while True:
            keyword = dequeue_item("keywords")

            if not keyword:
                logging.info("Nothing left in queue")
                time.sleep(5)
                continue

            try:
                search(keyword)
            except Exception as e:
                logging.info("Encountered exception, placing keyword back into the queue: {}".format(keyword))
                enqueue_item("keywords", keyword)
                raise e