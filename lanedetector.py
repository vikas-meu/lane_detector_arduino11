import cv2
import numpy as np
import utlis

curveList = []
avgVal = 10

def getLaneCurve(img, display=2):
    imgCopy = img.copy()  # This should be an image, not a VideoCapture object
    imgResult = img.copy()
    
    # STEP 1: Thresholding
    imgThres = utlis.thresholding(img)
    
    # STEP 2: Image Transformation
    hT, wT, c = img.shape
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utlis.drawPoints(imgCopy, points)
    
    # STEP 3: Histogram and Lane Curvature Calculation
    middlePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint
    
    # STEP 4: Curve Smoothing
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))
    
    # STEP 5: Visualize Lane and Curvature
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
    
    # Show final results
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp], 
                                            [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Result', imgResult)
    
    # Normalize curve
    curve = curve / 100
    if curve > 1: curve = 1
    if curve < -1: curve = -1

    return curve


if __name__ == '__main__':
    cap = cv2.VideoCapture('video.mp4')
    intialTrackBarVals = [102, 80, 20, 214]
    utlis.initializeTrackbars(intialTrackBarVals)
    
    while True:
        success, img = cap.read()  # Read each frame from the webcam
        if not success:
            break  # If no frame is read, exit the loop
        
        img = cv2.resize(img, (480, 240))  # Resize image to fit processing size
        curve = getLaneCurve(img, display=2)  # Process image and get lane curve
        print(curve)  # Print curve for debugging
        cv2.waitKey(1)  # Wait for 1 ms (useful for live video feed)
    
    cv2.destroyAllWindows()  # Close all windows after the loop
