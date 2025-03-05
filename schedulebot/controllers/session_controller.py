from schedulebot.singleton import Singleton

class SessionController(metaclass=Singleton):
    def __init__(self):
        self.__session = {}

    def create_session(self, user_id):
        if self.__session.get(user_id, None) is None:
            self.__session[user_id] = {}

    def get_session(self, user_id):
        session = self.__session.get(user_id, None)
        if session is None:
            self.create_session(user_id)
        return self.__session.get(user_id, None)

    def delete_session(self, user_id):
        if self.__session.get(user_id, None) is not None:
            self.__session.pop(user_id, None)