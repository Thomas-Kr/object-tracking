from object_tracking import Tracker

source_1 = "Sources/napkins.mp4"
source_2 = "Sources/circle.mp4"

tracker = Tracker(source_1)
tracker.track()

tracker = Tracker(source_2)
tracker.track(threshold=0.7)