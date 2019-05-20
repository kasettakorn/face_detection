import cv2
import threading
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True
        self.video = camera

    def run(self):
        while self.isRunning:
            ret, frame = self.video.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.video = cv2.VideoCapture(0)
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.video.release()
        
    def draw_boundary(self, img, classifier , scaleFactor, minNeighbor, color, text):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray, scaleFactor, minNeighbor)
        coordinate = [] #(x,y)
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1)
            coordinate = [x, y, w, h]
            print(coordinate)
        return img
    def detect(self,img, faceCascade):
        img = self.draw_boundary(img, faceCascade, 1.1, 10, (255,0,0), "Face")
        img = self.draw_boundary(img, eyeCascade, 1.1, 10, (0,255,0), "Eye")
        return img    
    def get_frame(self):
        ret, frame = self.video.read()
        frame = self.detect(frame, faceCascade)
        cv2.imshow('frame', frame)
        ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))
                
            #     ret, frame = self.video.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None  

        return jpeg.tobytes()

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.video)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

            