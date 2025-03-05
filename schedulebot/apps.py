from schedulebot.config import GEMINI_USED_MODEL, SQLITE_DBFILE

from schedulebot.controllers.session_controller import SessionController
from schedulebot.controllers.ai_controller import AIController
from schedulebot.controllers.database_controller import DatabaseController
from schedulebot.controllers.keyboards_controller import KeyboardsController

class Apps:
    def __init__(self):
        self.session_controller = SessionController()
        self.ai_controller = AIController(GEMINI_USED_MODEL)
        self.database_controller = DatabaseController(SQLITE_DBFILE)
        self.keyboards_controller = KeyboardsController()