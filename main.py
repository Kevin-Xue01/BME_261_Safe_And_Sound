import cv2 
import numpy as np
import copy

def main():
    getting_pixel_values()
    pass

def warp_perspective():
    def nothing(x):
        pass
    # cap = cv2.VideoCapture(0)
    # while True:
    #     ret, frame, = cap.read()
    #     cv2.imshow('camera', frame)
    #     if cv2.waitKey(1) == ord('q'):
    #         break
    # cap.release()
    # cv2.destroyAllWindows()
    cv2.namedWindow('Trackbars')
    cv2.createTrackbar("Top Left Column", "Trackbars", 25, 100, nothing)
    cv2.createTrackbar("Top Left Row", "Trackbars", 95, 100, nothing)
    cv2.createTrackbar("Top Right Column", "Trackbars", 90, 100, nothing)
    cv2.createTrackbar("Top Right Row", "Trackbars", 95, 100, nothing)
    cv2.createTrackbar("Bottom Left Column", "Trackbars", 10, 100, nothing)
    cv2.createTrackbar("Bottom Left Row", "Trackbars", 0, 100, nothing)
    cv2.createTrackbar("Bottom Right Column", "Trackbars", 100, 100, nothing)
    cv2.createTrackbar("Bottom Right Row", "Trackbars", 0, 100, nothing)


    img = cv2.imread("assets/main_view.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.Canny(img, 99, 99)
    _, thrash = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    rows, cols = img.shape  
    
    while True:
        newImg = copy.deepcopy(img)
        
        tLC = int(cols * cv2.getTrackbarPos("Top Left Column", "Trackbars") / 100)  
        tLR = int(rows * cv2.getTrackbarPos("Top Left Row", "Trackbars") / 100 )
        tRC = int(cols * cv2.getTrackbarPos("Top Right Column", "Trackbars") / 100) 
        tRR = int(rows * cv2.getTrackbarPos("Top Right Row", "Trackbars") / 100 )
        bLC = int(cols * cv2.getTrackbarPos("Bottom Left Column", "Trackbars") / 100 ) 
        bLR = int(rows * cv2.getTrackbarPos("Bottom Left Row", "Trackbars") / 100 )
        bRC = int(cols * cv2.getTrackbarPos("Bottom Right Column", "Trackbars") / 100) 
        bRR = int(rows * cv2.getTrackbarPos("Bottom Right Row", "Trackbars") / 100 )
        
        if cv2.waitKey(1) == ord('q'): # press q to terminate program
            break
        pts1 = np.float32(
            [[tLC, tLR],
             [tRC, tRR],
             [bLC, bLR],
             [bRC, bRR]]
        )
        pts2 = np.float32(
            [[cols*0.1, rows],
             [cols,     rows],
             [0,        0],
             [cols,     0]]
        )    
        
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
        distorted = cv2.warpPerspective(newImg, matrix, (cols, rows))
        #
        lower_bound_for_red = np.array([45]) # optimal value is [55, 55, 55]
        upper_bound_for_red = np.array([65])
        mask = cv2.inRange(newImg, lower_bound_for_red, upper_bound_for_red)   
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel)
        contours, _ = cv2.findContours(newImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #

        cv2.imshow('Mask', mask)
        cv2.imshow('Distorted', distorted)
        cv2.imshow("Original", newImg)
        img = newImg
   
    return

def start_recording_video ():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame, = cap.read()
        # lower_bound_for_red = np.array([45]) # optimal value is [55, 55, 55]
        # upper_bound_for_red = np.array([65])
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # mask = cv2.inRange(frame, lower_bound_for_red, upper_bound_for_red)   
        # kernel = np.ones((15, 15), np.uint8)
        # mask = cv2.erode(mask, kernel)
        # contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(frame, 45, 65, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            if area > 800:
                cv2.drawContours(frame, [approx], 0, (0,0,0), 5)
                if len(approx) >= 4 and len(approx) <= 10:
                    cv2.putText(frame, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))

        # lower_bound_for_green = np.array([118])
        # upper_bound_for_green = np.array([138])
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # mask = cv2.inRange(frame, lower_bound_for_green, upper_bound_for_green)   
        # kernel = np.ones((5, 5), np.uint8)
        # mask = cv2.erode(mask, kernel)
        # contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # for cnt in contours:
        #     area = cv2.contourArea(cnt)
        #     approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        #     x = approx.ravel()[0]
        #     y = approx.ravel()[1]
        #     if area > 400:
        #         cv2.drawContours(frame, [approx], 0, (0,0,0), 5)
        #         if len(approx) >= 4 and len(approx) <= 10:
        #             cv2.putText(frame, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
        
        
        
        
        
        # cv2.imshow('Mask', mask)
        cv2.imshow('camera', frame)
        if cv2.waitKey(1) == ord('q'): # press q to terminate program
            break
        
    cap.release()
    cv2.destroyAllWindows()
    pass

def apply_green_mask(img):
    

    img = cv2.imread("assets/main_view.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.Canny(img, 99, 99)
    _, thrash = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    rows, cols = img.shape  
    
    while True:
        newImg = copy.deepcopy(img)
        
        tLC = int(cols * cv2.getTrackbarPos("Top Left Column", "Trackbars") / 100)  
        tLR = int(rows * cv2.getTrackbarPos("Top Left Row", "Trackbars") / 100 )
        tRC = int(cols * cv2.getTrackbarPos("Top Right Column", "Trackbars") / 100) 
        tRR = int(rows * cv2.getTrackbarPos("Top Right Row", "Trackbars") / 100 )
        bLC = int(cols * cv2.getTrackbarPos("Bottom Left Column", "Trackbars") / 100 ) 
        bLR = int(rows * cv2.getTrackbarPos("Bottom Left Row", "Trackbars") / 100 )
        bRC = int(cols * cv2.getTrackbarPos("Bottom Right Column", "Trackbars") / 100) 
        bRR = int(rows * cv2.getTrackbarPos("Bottom Right Row", "Trackbars") / 100 )
        
        if cv2.waitKey(1) == ord('q'): # press q to terminate program
            break
        pts1 = np.float32(
            [[tLC, tLR],
             [tRC, tRR],
             [bLC, bLR],
             [bRC, bRR]]
        )
        pts2 = np.float32(
            [[cols*0.1, rows],
             [cols,     rows],
             [0,        0],
             [cols,     0]]
        )    
        
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
        distorted = cv2.warpPerspective(newImg, matrix, (cols, rows))
        #
        lower_bound_for_red = np.array([45]) # optimal value is [55, 55, 55]
        upper_bound_for_red = np.array([65])
        mask = cv2.inRange(newImg, lower_bound_for_red, upper_bound_for_red)   
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel)
        contours, _ = cv2.findContours(newImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #

        cv2.imshow('Mask', mask)
        cv2.imshow('Distorted', distorted)
        cv2.imshow("Original", newImg)
        img = newImg
   
    return


def getting_pixel_values():
    img = cv2.imread("assets/main_view.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thrash = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    rows,cols = img.shape
    cv2.imshow("Original", img)
    img = cv2.rectangle(img, (40, 350), (120, 550), (128, 128, 128), 5)
    color = img[250, 30] # 55 the lower the number, the darker
    print(color)
    color = img[350, 40] # 128
    print(color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()