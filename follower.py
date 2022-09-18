#importing some useful packages
import numpy as np
import cv2
import time

def window_search(binary_warped, orientation, direction):
    if orientation == 'h':
        # Take a histogram
        if direction == 'r':
            histogram = np.sum(binary_warped[:,:int(binary_warped.shape[1]/3)], axis=1)
        else:
            histogram = np.sum(binary_warped[:,int(binary_warped.shape[1]*2/3):], axis=1)
        # Create an output image to draw on and  visualize the result
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
        # Find the peak of the center
        # This will be the starting point for the center
        center_base = np.argmax(histogram)

        # Choose the number of sliding windows
        nwindows = 9
        # Set height of windows
        window_width = np.int(binary_warped.shape[1]/nwindows)
        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # Current positions to be updated for each window
        centery_current = center_base
        # Set the height of the windows +/- margin
        margin = 100
        # Set minimum number of pixels found to recenter window
        minpix = 50
        # Create empty lists to receive center and right lane pixel indices
        center_inds = []

        # Step through the windows one by one
        for window in range(nwindows):
            # Identify window boundaries in x and y (center)
            if direction == 'r':
                win_x_low = window*window_width
                win_x_high = (window+1)*window_width
            else:
                win_x_low =  binary_warped.shape[1] - (window+1)*window_width
                win_x_high = binary_warped.shape[1] - window*window_width
            win_ycenter_low = centery_current - margin
            win_ycenter_high = centery_current + margin
            # Identify the nonzero pixels in x and y within the window
            good_center_inds = ((nonzerox >= win_x_low) & (nonzerox < win_x_high) & (nonzeroy >= win_ycenter_low) & (nonzeroy < win_ycenter_high)).nonzero()[0]
            # Append these indices to the lists
            center_inds.append(good_center_inds)
            # If you found > minpix pixels, recenter next window on their mean position
            if len(good_center_inds) > minpix:
                centery_current = np.int(np.mean(nonzeroy[good_center_inds]))

        # Concatenate the arrays of indices
        center_inds = np.concatenate(center_inds)
        
        # Extract center line pixel positions
        centerx = nonzerox[center_inds]
        centery = nonzeroy[center_inds] 

        # Fit a second order polynomial to each
        center_fit = np.polyfit(centerx, centery, 2)

        # Generate x and y values for plotting
        plotx = np.linspace(0, binary_warped.shape[1]-1, num = binary_warped.shape[1])
        center_fity = center_fit[0]*plotx**2 + center_fit[1]*plotx + center_fit[2]
        if direction == 'r':
            last_point = center_fity[-1]
        else:
            last_point = center_fity[0]
        
        # Generate black image and colour lane lines
        out_img[nonzeroy[center_inds], nonzerox[center_inds]] = [1, 0, 0]
            
        # Draw polyline on image
        center = np.asarray(tuple(zip(plotx, center_fity)), np.int32)
        cv2.polylines(out_img, [center], False, (255,255,255), thickness=5)
    
    else:
        # Take a histogram
        if direction == 'u':
            histogram = np.sum(binary_warped[int(binary_warped.shape[0]*2/3):,:], axis=0)
        else:
            histogram = np.sum(binary_warped[:int(binary_warped.shape[0]/3),:], axis=0)
        # Create an output image to draw on and  visualize the result
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
        # Find the peak of the center
        # These will be the starting point for the center
        center_base = np.argmax(histogram)

        # Choose the number of sliding windows
        nwindows = 9
        # Set height of windows
        window_height = np.int(binary_warped.shape[0]/nwindows)
        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # Current positions to be updated for each window
        centerx_current = center_base
        # Set the width of the windows +/- margin
        margin = 100
        # Set minimum number of pixels found to recenter window
        minpix = 50
        # Create empty lists to receive center lane pixel indices
        center_inds = []

        # Step through the windows one by one
        for window in range(nwindows):
            # Identify window boundaries in x and y (and right and center)
            if direction == 'u':
                win_y_low = binary_warped.shape[0] - (window+1)*window_height
                win_y_high = binary_warped.shape[0] - window*window_height
            else:
                win_y_low = window*window_height
                win_y_high = (window+1)*window_height
            win_xcenter_low = centerx_current - margin
            win_xcenter_high = centerx_current + margin

            # Draw the windows on the visualization image
            cv2.rectangle(out_img,(win_xcenter_low,win_y_low),(win_xcenter_high,win_y_high),(0,255,0), 2) 

            # Identify the nonzero pixels in x and y within the window
            good_center_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xcenter_low) & (nonzerox < win_xcenter_high)).nonzero()[0]
            # Append these indices to the lists
            center_inds.append(good_center_inds)
            # If you found > minpix pixels, recenter next window on their mean position
            if len(good_center_inds) > minpix:
                centerx_current = np.int(np.mean(nonzerox[good_center_inds]))

        # Concatenate the arrays of indices
        center_inds = np.concatenate(center_inds)

        # Extract center and right line pixel positions
        centerx = nonzerox[center_inds]
        centery = nonzeroy[center_inds] 
        # Fit a second order polynomial to each
        center_fit = np.polyfit(centery, centerx, 2)

        # Generate x and y values for plotting
        ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )
        center_fitx = center_fit[0]*ploty**2 + center_fit[1]*ploty + center_fit[2]
        if direction == 'u':
            last_point = center_fitx[0]
        else:
            last_point = center_fitx[-1]
        
        # Generate black image and colour lane lines
        out_img[nonzeroy[center_inds], nonzerox[center_inds]] = [1, 0, 0]
            
        # Draw polyline on image
        center = np.asarray(tuple(zip(center_fitx, ploty)), np.int32)
        cv2.polylines(out_img, [center], False, (255,255,255), thickness=5)
    
    return last_point, center_fit[2], out_img


def preprocess(img):
    flip_img = cv2.flip(img, 1)
    img_hsv=cv2.cvtColor(flip_img, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0+mask1

    return flip_img, mask

def check_line_posistion(intersept, img, orientation):
    if orientation == 'h':
        division = int(img.shape[0]/3)
        if(intersept > 2*division):
            return "move UP a bit"
        elif (intersept < division):
            return "move DOWN a bit"
        else:
            return "all is well"
    else:
        division = int(img.shape[1]/3)
        if(intersept > 2*division):
            return "move LEFT a bit"
        elif (intersept < division):
            return "move RIGHT a bit"
        else:
            return "all is well"

def change_direction(frame, orientation, direction, last_point):
    changed = False
    if direction == 'r' or direction == 'l':
        if last_point < 0:
            direction = 'u'
            orientation = 'v'
            changed = True
        elif last_point > frame.shape[0]:
            direction = 'd'
            orientation = 'v'
            changed = True
    elif direction == 'd' or direction == 'u':
        if last_point < 0:
            direction = 'l'
            orientation = 'h'
            changed = True
        elif last_point > frame.shape[1]:
            direction = 'r'
            orientation = 'h'
            changed = True
    return changed, orientation, direction

def print_direction(direction):
    if direction == 'r':
        print("direction is RIGHT")
    elif direction == 'l':
        print("direction is LEFT")
    elif direction == 'u':
        print("direction is UP")
    else:
        print("direction is DOWN")