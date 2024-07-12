from flask import Flask, Response, render_template
from refactored_recognize import HandRecognizer
import cv2

# initalize the flask app
app = Flask(__name__)
# create an instance of the HandRecognizer class
hand_recognizer = HandRecognizer()

# generator function to continuosly capture frames from the camera and process them
def generate_frames():
    while True:
        frame, thresholded = hand_recognizer.get_frame()
        if frame is not None:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

# returns response from video feed from camera
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# renders html template when the main page is accessed
@app.route('/')
def index():
    return render_template('index.html')

# runs app
if __name__ == '__main__':
    app.run(debug=True)
