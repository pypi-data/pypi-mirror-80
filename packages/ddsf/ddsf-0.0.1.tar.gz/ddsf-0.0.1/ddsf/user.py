
class User():
    data = {}

    def __init__(self, username):
        self.data['username'] = username

    def get(self):
        return self.data
