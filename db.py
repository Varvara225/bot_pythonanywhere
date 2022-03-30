import sqlite3


class DbHandler(object):
    conn = None
    cur = None

    def __init__(self):
        self.conn = sqlite3.connect('TEDtalks.db')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_topics(self):
        self.cur.execute('''
        SELECT name, id
            FROM  topics
        ''')
        return self.cur.fetchall()

    def get_urls_by_topic(self, topic_id):
        self.cur.execute('''
        SELECT videos.name, url
            FROM videos
            JOIN topics on videos.topic_id = topics.id
        WHERE topic_id = ?
        ORDER BY random()
        LIMIT 10''', (topic_id,))
        return self.cur.fetchall()