from object_tracking import Tracker

source = "Sources/maxima_4.mov"

tracker = Tracker(source, FPS=5)
tracker.track(0.8)