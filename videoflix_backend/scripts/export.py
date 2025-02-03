from videoflix_app.admin import VideoResource
import datetime


dataset = VideoResource().export()

with open(f"export/video_data_{datetime.date}.json", "w") as file:
    file.write(dataset.json)