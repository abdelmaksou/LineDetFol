from follower import *

# global variables
cap = cv2.VideoCapture(0)
direction = 'r'
orientation = 'h'
changed = False
prev = time.time()
curr = time.time()

# read camera feed
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # preprocess the frames
        flip_frame, mask = preprocess(frame)
        # get current time in seconds
        curr = time.time()
        try:
            # get the line and its information
            last_point, intersept, output_img = window_search(mask, orientation, direction)
            # check if the direction is changed or not
            if changed == True and int(curr-prev) > 2:
                changed = False
            if changed == False:
                print(check_line_posistion(intersept, output_img, orientation))
                changed, orientation, direction = change_direction(output_img, orientation, direction, last_point)
                if changed == True:
                    prev = time.time()
                    curr = time.time()
                print_direction(direction)
        except:
            print("No Line is Detected")

        # display the results
        cv2.imshow('frame',flip_frame)
        cv2.imshow('mask',mask)
        try:
            cv2.imshow('result',output_img)
        except:
            print("No Line is Detected") 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
