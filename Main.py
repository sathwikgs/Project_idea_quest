import cv2
import mail as m


def difference(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)

    return cv2.bitwise_and(d1, d2)


filename = "trigger"
index = "0"

detect_start = 0
detect_stop = 0

cam = cv2.VideoCapture(0)
t0 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
t1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
t2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)

while True:
    to_be_displayed = cam.read()[1]
    diff_img = difference(t0, t1, t2)
    diff_img = cv2.threshold(diff_img, 30, 255, cv2.THRESH_BINARY)[1]
    diff_img = cv2.dilate(diff_img, None, iterations=2)
    im2, contours, hierarchy = cv2.findContours(diff_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    contour_count = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 200:
            contour_count += 1

    if contour_count >= 3:
        if detect_start == 0:
            detect_start = 1
        index_new = int(index) + 1
        index = str(index_new)
        filename_new = filename + index
        cv2.imwrite(filename_new + ".png", to_be_displayed)
    else:
        if detect_start == 1:
            detect_stop = 1
            to_be_sent = index_new/2
            print to_be_sent
            m.sendmail(filename + str(to_be_sent) + ".png")

    cv2.imshow('Output', difference(t0, t1, t2))

    t0 = t1
    t1 = t2
    t2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
    k = cv2.waitKey(100)

    if k == 27:
        cv2.destroyAllWindows()
        break
    elif detect_stop == 1:
        break
    else:
        continue





