import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise

class HandRecognizer:
    def __init__(self):
        # Initialize background model, camera, and other parameters
        self.bg = None
        self.aWeight = 0.5
        self.camera = cv2.VideoCapture(0)
        self.top, self.right, self.bottom, self.left = 10, 350, 225, 590
        self.num_frames = 0

    def run_avg(self, image):
        # Update the background model using a weighted average
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return
        cv2.accumulateWeighted(image, self.bg, self.aWeight)

    def segment(self, image, threshold=25):
        # Segment the hand region from the background
        diff = cv2.absdiff(self.bg.astype("uint8"), image)
        thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
        cnts, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # If no contours are detected, return None
        if len(cnts) == 0:
            return None
        else:
        # Get the maximum contour area which corresponds to the hand
            segmented = max(cnts, key=cv2.contourArea)
            return (thresholded, segmented)

    def count(self, thresholded, segmented):
        # Count the number of fingers in the segmented hand region
        chull = cv2.convexHull(segmented)
        extreme_top = tuple(chull[chull[:, :, 1].argmin()][0])
        extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
        extreme_left = tuple(chull[chull[:, :, 0].argmin()][0])
        extreme_right = tuple(chull[chull[:, :, 0].argmax()][0])

        cX = (extreme_left[0] + extreme_right[0]) // 2
        cY = (extreme_top[1] + extreme_bottom[1]) // 2

        coordinates = np.array([[cX, cY]])
        extreme_points = np.array([extreme_left, extreme_right, extreme_top, extreme_bottom])
    
        # Compute the maximum distance from the center to the extreme points
        distance = pairwise.euclidean_distances(coordinates, extreme_points)[0]
        max_distance = distance.max()
        radius = int(0.8 * max_distance)
        circumference = (2 * np.pi * radius)

        # Create a circular ROI to count fingers
        circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
        cv2.circle(circular_roi, (cX, cY), radius, 255, 1)

        circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)
        cnts, _ = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        count = 0
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if (cY + (cY * 0.25)) > (y + h):
                count += 1

        return count

    def get_frame(self):
        # Capture a frame from the camera
        grabbed, frame = self.camera.read()
        if not grabbed:
            return None, None

        frame = imutils.resize(frame, width=700)
        frame = cv2.flip(frame, 1)
        clone = frame.copy()
        (height, width) = frame.shape[:2]
        roi = frame[self.top:self.bottom, self.right:self.left]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # Build the background model
        if self.num_frames < 30:
            self.run_avg(gray)
        else:
            # Segment the hand region
            hand = self.segment(gray)
            if hand is not None:
                (thresholded, segmented) = hand
                fingers = self.count(thresholded, segmented)
                # Draw contours and number of fingers on the frame
                cv2.drawContours(clone, [segmented + (self.right, self.top)], -1, (0, 0, 255))
                cv2.putText(clone, f"Fingers: {fingers}", (70, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
                cv2.imshow("Thresholded", thresholded)

        # Draw the green rectangle in every frame
        cv2.rectangle(clone, (self.left, self.top), (self.right, self.bottom), (0, 255, 0), 2)
        self.num_frames += 1

        return clone, None

    def release(self):
        # Release the camera and destroy all OpenCV windows
        self.camera.release()
        cv2.destroyAllWindows()
