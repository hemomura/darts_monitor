import cv2
import time
import datetime
import queue

class captureClass():
    def __init__(self, cap_number):
        self.cap = cv2.VideoCapture(cap_number)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # self.cap.set(cv2.CAP_PROP_FPS, 10)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

    def readFrame(self):
        ret, self.frame = self.cap.read()
        return ret

    def getFrame(self):
        return self.frame

    def capRelease(self):
        self.cap.release()

    def getWidth(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def getHeight(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def getFrameRate(self):
        return self.cap.get(cv2.CAP_PROP_FPS)

def monitor(cap_number1, cap_number2, delay_time1, delay_time2):
    cap_obj1 = captureClass(cap_number1)
    cap_obj2 = captureClass(cap_number2)
    delay_start1 = time.time() + delay_time1
    delay_start2 = time.time() + delay_time2
    
    delay_queue1 = queue.Queue()
    delay_queue2 = queue.Queue()

    wipe_width = int(cap_obj1.getWidth() / 3)
    wipe_height = int(cap_obj1.getHeight() / 3)
    wipe_mergin = 40
    wipe_pos_x = int(cap_obj1.getWidth()) - wipe_width - wipe_mergin
    
    real_width = 640
    real_height = 360

    delay_width = 960
    delay_height = 540

    real_title = "realtime"
    delay_title1 = str(delay_time1) + "sec delay"
    delay_title2 = str(delay_time2) + "sec delay"

    cv2.namedWindow(real_title, cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL)
    cv2.namedWindow(delay_title1, cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL)
    cv2.namedWindow(delay_title2, cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL)
    
    writer_fps = cap_obj1.getFrameRate() / 3
    writer_size = (int(cap_obj1.getWidth()), int(cap_obj1.getHeight()))
    writer_format = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    onRec = False

    while True:
        cap_obj1.readFrame()
        cap_obj2.readFrame()
        frame1 = cap_obj1.getFrame()
        frame2 = cap_obj2.getFrame()

        frame2 = cv2.resize(frame2, (wipe_width, wipe_height))

        dx = wipe_pos_x    # 横方向の移動距離
        dy = wipe_mergin     # 縦方向の移動距離
        h, w = frame2.shape[:2]
        frame = frame1
        frame[dy:dy+h, dx:dx+w] = frame2

        if onRec:
            writer.write(frame)

        frame = cv2.resize(frame, (delay_width, delay_height))
        delay_queue1.put(frame)
        delay_queue2.put(frame)

        if onRec:
            cv2.putText(frame, "REC", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)

        frame = cv2.resize(frame, (real_width, real_height))
        cv2.imshow(real_title, frame)

        if time.time() > delay_start1:
            frame = delay_queue1.get()
            cv2.imshow(delay_title1, frame)

        if time.time() > delay_start2:
            frame = delay_queue2.get()
            cv2.imshow(delay_title2, frame)

        lastkey = cv2.waitKey(1)
        if lastkey == ord("q"):
            if onRec:
                writer.release()
            cap_obj1.capRelease()
            cap_obj2.capRelease()
            cv2.destroyAllWindows()
            break
        if lastkey == ord("r") and not onRec:
            onRec = True
            now = datetime.datetime.now()
            now_ymdhms = "{0:%Y%m%d_%H%M%S}".format(now)
            writer_filename = "./darts_monitor_" + now_ymdhms + ".mp4"
            writer = cv2.VideoWriter(writer_filename, writer_format, writer_fps, writer_size)
        if lastkey == ord("s") and onRec:
            onRec = False
            writer.release()
        if lastkey == ord("c"):
            cv2.imwrite("frame.png", frame)


if __name__ == "__main__":

    cap_number1 = 2
    cap_number2 = 0
    delay_time1 = 15
    delay_time2 = 30
    
    monitor(cap_number1, cap_number2, delay_time1, delay_time2)

    print("program complete")