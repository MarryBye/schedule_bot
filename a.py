from calendar import month
import datetime

lesson_time = "18:00"

lesson_time = datetime.datetime.strptime(lesson_time, "%H:%M")
end_time = lesson_time + datetime.timedelta(hours=1, minutes=30)

print(lesson_time.strftime("%H:%M"), end_time.strftime("%H:%M"))