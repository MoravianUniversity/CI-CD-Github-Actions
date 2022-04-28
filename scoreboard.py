

class HighScore:

    def __init__(self, db):
        self.db = db

    @property
    def name(self):
        if self.db.exists('name'):
            # Redis returns a byte string.  We decode to a Unicode string
            # (which is what we get when we say something like 'hi')
            return self.db.get('name').decode()
        return None

    @property
    def score(self):
        if self.db.exists('score'):
            return int(self.db.get('score'))
        return 0

    def submit(self, name, score):
        if score > self.score:
            self.db.set('name', name)
            self.db.set('score', score)
