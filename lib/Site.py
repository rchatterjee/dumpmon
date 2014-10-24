from Queue import Queue
import requests
import time
import re, os, json, random
#from pymongo import MongoClient
from requests import ConnectionError
#from twitter import TwitterError
from settings import USE_DB, DB_HOST, DB_PORT, EMAIL_THRESHOLD
import logging, codecs
import helper


class Site(object):
    '''
    Site - parent class used for a generic
    'Queue' structure with a few helper methods
    and features. Implements the following methods:

            empty() - Is the Queue empty
            get(): Get the next item in the queue
            put(item): Puts an item in the queue
            tail(): Shows the last item in the queue
            peek(): Shows the next item in the queue
            length(): Returns the length of the queue
            clear(): Clears the queue
            list(): Lists the contents of the Queue
            download(url): Returns the content from the URL

    '''
    # I would have used the built-in queue, but there is no support for a peek() method
    # that I could find... So, I decided to implement my own queue with a few
    # changes
    def __init__(self, queue=None):
        if queue is None:
            self.queue = []
        if USE_DB:
            # Lazily create the db and collection if not present
            self.db_client = MongoClient(DB_HOST, DB_PORT).paste_db.pastes
        else:
            if not os.path.exists('pastebindump'):
                os.mkdir('pastebindump')

    def empty(self):
        return len(self.queue) == 0

    def get(self):
        if not self.empty():
            result = self.queue[0]
            del self.queue[0]
        else:
            result = None
        return result

    def put(self, item):
        self.queue.append(item)

    def peek(self):
        return self.queue[0] if not self.empty() else None

    def tail(self):
        return self.queue[-1] if not self.empty() else None

    def length(self):
        return len(self.queue)

    def clear(self):
        self.queue = []

    def list(self):
        print('\n'.join(url for url in self.queue))

    def monitor(self, bot, t_lock):
        self.update()
        while(1):
            while not self.empty():
                paste = self.get()
                self.ref_id = paste.id
                logging.info('[*] Checking ' + paste.url)
                paste.text = self.get_paste_text(paste)
                save_dic = {
                    'pid' : paste.id,
                    'text' : paste.text,
                    'emails' : paste.emails,
                    'hashes' : paste.hashes,
                    'num_emails' : paste.num_emails,
                    'num_hashes' : paste.num_hashes,
                    'type' : paste.type,
                    'db_keywords' : paste.db_keywords,
                    'url' : paste.url
                    }
                tweet = None; # helper.build_tweet(paste)
                if tweet:
                    with t_lock:
                        try:
                            bot.statuses.update(status=tweet)
                        except TwitterError:
                            pass
                if USE_DB:
                    with t_lock:
                        self.db_client.save(save_dic)
                else:
                    if paste.num_emails>EMAIL_THRESHOLD:
                        print "Found one paste with many email-ids: %s" % paste.id
                        with codecs.open('pastebindump/%s.txt' % paste.id, 'w', 'utf-8-sig') as f:
                            f.write(paste.emails)
                            f.write('\n' + ('--'*10) + '\n')
                            f.write(paste.text)
                            f.write('\n' + ('-='*10) + '\n')
                    else:
                        print paste
                time.sleep(random.randint(0,self.sleep/5))
            self.update()
            while self.empty():
                logging.debug('[*] No results... sleeping')
                time.sleep(random.randint(0,self.sleep*2))
                self.update()
