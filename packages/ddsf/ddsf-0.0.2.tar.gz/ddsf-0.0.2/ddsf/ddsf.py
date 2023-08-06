from requests import Session
from requests_ntlm import HttpNtlmAuth
from .user import User
from .person import Person
from .academicTitle import AcademicTitle
from .room import Room

class Ddsf():
    url = None
    session = None

    def __init__(self, url, username, password):
        self.url = url
        self.session = Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.session.auth = HttpNtlmAuth(username, password)

    def user(self, username):
        user = User(self.url, self.session)
        print(user.session)
        user.get(username)
        return user

    def rooms(self):
        response = self.session.get(self.url + "Room()?$filter=IsDeleted eq false")
        roomList = []
        for room in response.json()['value']:
            roomList.append(Room(self.url, self.session, room))
        return roomList

    def person(self, id):
        person = Person(self.url, self.session)
        person.get(id)
        return person

    def academicTitle(self, id=None):
        title = AcademicTitle(self.url, self.session)
        title.get(id)
        return title

    def get(self):
        return self.session.get(self.url)
