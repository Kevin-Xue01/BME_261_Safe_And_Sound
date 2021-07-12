import cv2
import numpy as np
from database import Database
from operator import itemgetter

with_video = False


def main():
    database = Database()

    if with_video:
        start_recording_video()
    else:
        img = cv2.imread("assets/main_view.jpg")
        img = warp_perspective(img, database.get_warp_perspective_data())
        mask = apply_green_mask(img, database.get_green_mask_data())
        rectangle_contours = find_green_rectangle_contours(mask)
        find_green_rectangle_polygon(
            rectangle_contours, img, database.get_green_polygon_data()
        )
        canny = detect_ball_edge(img)
        ball_contours = find_ball_contours(canny)
        find_ball_polygon(ball_contours, img)
        cv2.imshow("Original", img)
        cv2.imshow("Ball Canny", canny)
        cv2.imshow("Green Mask", mask)
        while True:
            if cv2.waitKey(1) == ord("q"):  # press q to terminate program
                break
        cv2.destroyAllWindows()


def warp_perspective(img, config_data):
    rows, cols, _ = img.shape  # Color
    # rows, cols = img.shape  # Gray scale
    for i in config_data:
        config_data[i] = int(config_data[i])
    (bLC, bLR, bRC, bRR, tLC, tLR, tRC, tRR,) = itemgetter(
        "bLC",
        "bLR",
        "bRC",
        "bRR",
        "tLC",
        "tLR",
        "tRC",
        "tRR",
    )(config_data)

    pts1 = np.float32(
        [
            [int(cols * (tLC / 100)), int(rows * (tLR / 100))],
            [int(cols * (tRC / 100)), int(rows * (tRR / 100))],
            [int(cols * (bLC / 100)), int(rows * (bLR / 100))],
            [int(cols * (bRC / 100)), int(rows * (bRR / 100))],
        ]
    )
    pts2 = np.float32([[cols * 0.1, rows], [cols, rows], [0, 0], [cols, 0]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    distorted = cv2.warpPerspective(img, matrix, (cols, rows))

    return distorted


def start_recording_video():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        (
            ret,
            frame,
        ) = cap.read()
        mask = apply_green_mask(frame)
        contours = find_green_rectangle_contours(mask)
        find_green_rectangle_polygon(contours, frame)
        cv2.imshow("camera", frame)
        if cv2.waitKey(1) == ord("q"):  # press q to terminate program
            break

    cap.release()
    cv2.destroyAllWindows()


def apply_green_mask(img, config_data):
    lower_bound, upper_bound = itemgetter("lower_bound", "upper_bound")(config_data)
    lower_bound_np_arr = np.array(lower_bound)
    upper_bound_np_arr = np.array(upper_bound)
    mask = cv2.inRange(img, lower_bound_np_arr, upper_bound_np_arr)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    return mask


def find_green_rectangle_contours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def find_green_rectangle_polygon(contours, img, config_data):
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if (
            area > config_data["area"]
            and len(approx) >= config_data["lower_length_threshold"]
            and len(approx) <= config_data["upper_length_threshold"]
        ):
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 3)


def detect_ball_edge(img):
    lower = 400
    upper = 80
    canny = cv2.Canny(img, lower, upper)
    return canny


def find_ball_contours(ball_canny):
    contours, _ = cv2.findContours(ball_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def find_ball_polygon(contours, img):
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.011 * cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if area > 30 and area < 40 and len(approx) >= 17:
            cv2.drawContours(img, [approx], 0, (0, 0, 0), 3)
            cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))


if __name__ == "__main__":
    main()
