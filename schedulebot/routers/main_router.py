import aiogram

from schedulebot.controllers.database_controller import DatabaseController

router: aiogram.Router = aiogram.Router(name=__name__)
db_controller = DatabaseController("suitt_schedule.db")

@router.startup()
async def on_startup() -> None:
    print("Bot started!")
    db_controller.connect()
    
@router.shutdown()
async def on_shutdown() -> None:
    print("Bot shutdown!")
    db_controller.disconnect()
        
