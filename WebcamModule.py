import cv2

cap = cv2.VideoCapture('video.mp4')

def getImg(display=False, size=[480, 240]):
    ret, img = cap.read()  # Read the frame
    if not ret:  # If the frame is not read successfully, return None
        print("Failed to read the frame.")
        return None
    
    img = cv2.resize(img, (size[0], size[1]))  # Resize image
    if display:
        cv2.imshow('IMG', img)  # Show the image in a window
    return img

if __name__ == '__main__':
    while True:
        img = getImg(True)  # Get the frame and display it
        if img is None:  # Break if no frame is available
            break
        
        key = cv2.waitKey(1)  # Wait for 1 ms, check for key press to exit
        if key == ord('q'):  # Press 'q' to quit
            break

    cap.release()  # Release the video capture object
    cv2.destroyAllWindows()  # Close all OpenCV windows
