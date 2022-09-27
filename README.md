# Line Detection for ROV
The project is an implementation for an algorithm that detects and attempt to follow this red rope while it's hanged vertically.
![Screenshot from MATE ROV Manual 2022](https://github.com/abdelmaksou/LineDetFol/blob/main/prob_img.png)
## Part 1: Preprocessing
Masking out the red line from the image after converting it to HSV.
## Part 2: Curve fitting with sliding windows technique
The algorithm works by 
- taking the histogram of the binary mask.
- for each peak on the histogram, we initialize windows and slide them either horizontaly or vertically based on the input. Each window is centerd by its detected pexels inside.
- then, we extract the center line pixel positions, and fit a second order polynomial to each.
Now, The line is detected and visible. It remains writing the apropriate line following algorithm depending on the task, which is following a red rope that is hanged vertically in this case.
## Part 3: Results
![](https://github.com/abdelmaksou/LineDetFol/blob/main/ezgif.com-gif-maker.gif)
