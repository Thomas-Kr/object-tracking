import cv2

class Tracker:
    def __init__(self, source: str, tracker=cv2.TrackerCSRT_create()):
        self.video_capture = cv2.VideoCapture(source)
        self.track_method = tracker
        self.bbox, self.frame = self._set_tracker(self.video_capture)
        self.template = self._create_template()

    def _set_tracker(self, video_capture) -> cv2.numpy.ndarray:
        _, frame = video_capture.read()
        bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
        self.track_method.init(frame, bbox)

        return bbox, frame
    
    def _enhance_image(self, img):
        # Adding blur to reduce noise
        img_blurred = cv2.GaussianBlur(img, (5, 5), 0)

        # Increasing contrast using adaptive histogram equalization
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe = clahe.apply(cv2.cvtColor(img_blurred, cv2.COLOR_BGR2GRAY))

        return clahe

    def _create_template(self) -> cv2.numpy.ndarray:
        x, y, w, h = [int(i) for i in self.bbox]
        template = self.frame[y:y + h, x:x + w]

        template_enhanced = self._enhance_image(template)

        return template_enhanced

    def match_template(self, frame, threshold):
        frame_enhanced = self._enhance_image(frame)

        matched = cv2.matchTemplate(frame_enhanced, self.template, cv2.TM_CCOEFF_NORMED)

        # Most similar contour
        _, max_val, _, max_loc = cv2.minMaxLoc(matched)

        if max_val >= threshold:
            bbox = [max_loc[0], max_loc[1], self.bbox[2], self.bbox[3]]

            return [True, bbox]
        return [False, None]

    def update(self, frame):
        return self.track_method.update(frame)
    
    def track(self, threshold):
        while True:
                ret, frame = self.video_capture.read()
                if not ret:
                    break

                is_updated, bbox = self.update(frame)

                if is_updated:
                    # Drawing contour
                    x, y, w, h = [int(i) for i in bbox]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(frame, f'X:{x}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f'Y:{y}', (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    is_found, bbox = self.match_template(frame, threshold)

                    if is_found:
                        self.track_method.init(frame, bbox)
                    else:
                        cv2.putText(frame, "Lost", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow('Object Tracking', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    source = "Sources/napkins.mp4"

    tracker = Tracker(source)
    tracker.track(threshold=0.9)
    