import cv2
import os
import imutils
import sys
import numpy, math

def distance_2d(pt1, pt2):
    return(math.sqrt(math.pow(pt2[0] - pt1[0], 2) + math.pow(pt2[1] - pt1[1], 2)))

def draw_grid(frame):
    h,w = frame.shape[:2]

    side = h - 100
    left_side = (w - side)//4
    right_side = left_side + side

    top_left = (left_side,10)
    top_right = (right_side,10)
    bottom_left = (left_side,h-90)
    bottom_right = (right_side,h-90)

    cv2.line(frame, top_left, top_right, (0,255,255), 4)
    cv2.line(frame, bottom_left, top_left, (0,255,255), 4)
    cv2.line(frame, bottom_left, bottom_right, (0,255,255), 4)
    cv2.line(frame, bottom_right, top_right, (0,255,255), 4)
    arr=[[(0,0) for i in range(9)] for j in range(9)]
    grid_x = left_side
    grid_y = 10

    for i in range(1,9):
        grid_y += side//9
        if(i%3==0):
            THICKNESS = 4
            CONNECTION_COLOR = (0, 255, 255)

        else:
            THICKNESS = 2
            CONNECTION_COLOR = (0, 255, 0)
        cnt=0
        for val in range(grid_x+side//24,right_side,side//9):
            arr[i-1][cnt] = (val,grid_y-side//22)
            cnt+=1
        cv2.line(frame, (grid_x,grid_y), (right_side,grid_y), CONNECTION_COLOR, THICKNESS)

    cnt=0
    grid_y += side//9
    for val in range(grid_x+side//24,right_side,side//9):
        arr[8][cnt] = (val,grid_y-side//22)
        cnt+=1
        
    grid_x = left_side
    grid_y = 10
    
    for i in range(1,9):
        grid_x += side//9  
        if(i%3==0):
            THICKNESS = 4
            CONNECTION_COLOR = (0, 255, 255)
        else:
            THICKNESS = 2 
            CONNECTION_COLOR = (0, 255, 0)                                             
        cv2.line(frame, (grid_x,grid_y), (grid_x,h-90), CONNECTION_COLOR, THICKNESS)
    
    return(frame,arr)

def draw_numbers(frame,arr,puzzle):
    h,w = frame.shape[:2]
    side = h - 60
    for i in range(9):
        for j in range(9):
            if(puzzle[i][j]!=0):
                cv2.putText(frame,str(puzzle[i][j]), (arr[i][j][0], arr[i][j][1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
    
    selection_nums = []
    for i in range(9):
        selection_nums.append((arr[i][8][0]+side//5, arr[i][8][1]))
        cv2.putText(frame,str(i+1), (arr[i][8][0]+side//5, arr[i][8][1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
    
    cv2.putText(frame,"D", (arr[4][8][0]+side//3, arr[4][8][1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
    selection_nums.append((arr[4][8][0]+side//3, arr[4][8][1]))
    return(frame,selection_nums)

def draw_hand(frame, bbox, pointer_text):
    area = -1
    max_area = 150000
    area_pos = ""
    if(bbox != []):
        location = (int((bbox[0][0]+bbox[2][0])//2),int((bbox[0][1]+bbox[2][1])//2))
        # print(location)
        color = (255, 155, 0)
        area = math.pow(bbox[1][0] - bbox[0][0], 2) + math.pow(bbox[1][1] - bbox[0][1], 2)
        # print(bbox,area)

        if(area >= 0.7*max_area):
            area_pos = "close"
        else:
            area_pos = "far"
            color = (194,3,252)

        cv2.putText(frame,str(pointer_text), location, cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
    return(frame, area, area_pos)

def hand_tracking(frame, detector):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    points, bbox = detector(image)
    return (frame,bbox)

def main():
    from seedoku.sudoku import run, best
    from seedoku.trackers.hand_tracker import HandTracker
    cv2.namedWindow("New")

    if("/" in sys.path[-1]):
        package_path = sys.path[-1].split("/")
    else:
        package_path = sys.path[-1].split("\\")

    package_path += ["seedoku","trackers"]
    file_path = package_path[0]+os.path.sep
    for directory in package_path[1:]:
        file_path = os.path.join(file_path,directory)

    
    PALM_MODEL_PATH = os.path.join(file_path,"palm_detection_without_custom_op.tflite")
    CONNECTION_COLOR = (0, 255, 0)
    THICKNESS = 4
    ANCHORS_PATH = os.path.join(file_path,"anchors.csv")

    detector = HandTracker(
        "false",
        PALM_MODEL_PATH,
        "",
        ANCHORS_PATH,
        box_shift=0.2,
        box_enlarge=1
    )


    cap = cv2.VideoCapture(0)

    results, answer = run(n=0)       # find puzzles with as few givens as possible.
    puzzle  = best(results)  # use the best one of those puzzles.
    #print(puzzle)

    if cap.isOpened():
        hasFrame, frame = cap.read()
    else:
        hasFrame = False

    bbox=[]
    pointer_text = "x"
    frame_count = 0

    area_count = 0
    area_pos = "far"
    min_area = 100000
    lives = 5

    while hasFrame:
        frame = cv2.flip(frame,1)
        frame = imutils.resize(frame,width=1100)
        h,w = frame.shape[:2]
        
        unsolved = sum([i.count(0) for i in puzzle])
        cv2.putText(frame,"LIVES LEFT: "+str(lives), (w-200,20), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (100, 100, 200), 2)

        if(lives == 0):
            cv2.putText(frame,"GAME OVER", (w//2-w//6,h//2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 155, 0), 3)
        elif(unsolved == 0):
            cv2.putText(frame,"YOU WON!", (w//2-w//6,h//2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 155, 0), 3)

        else:
            if(frame_count%50==0):
                frame, coords = hand_tracking(frame,detector)
                frame_count = 0
                
                if(coords is not None and bbox == []):
                    bbox = coords
                elif(coords is not None):
                    loc1 = (int((bbox[0][0]+bbox[2][0])//2),int((bbox[0][1]+bbox[2][1])//2))
                    loc2 = (int((coords[0][0]+coords[2][0])//2),int((coords[0][1]+coords[2][1])//2))
                    if(distance_2d(loc1,loc2)>10):
                        bbox = coords

            else:
                frame_count += 1

            frame, area, area_pos_new = draw_hand(frame, bbox, pointer_text)
            frame, arr = draw_grid(frame)
            frame, selection_nums = draw_numbers(frame,arr,puzzle)

            if(area != -1):
                pass
            
            if(area_pos_new == "close" and area_pos == "close"):
                area_count += 1
            elif(area_pos_new == "close"):
                area_pos = "close"
                area_count = 1
            elif(area_pos_new == "far" and area_pos == "far"):
                area_count += 1
            else:
                area_pos = "far"
                area_count = 1


            if(area_count >= 15 and area_pos == "close"):
                area_count = 0
                location = (int((bbox[0][0]+bbox[2][0])//2),int((bbox[0][1]+bbox[2][1])//2))

                distance = float(math.inf)
                pt = (-1,-1)
                value = 0

                for i in range(len(arr)):
                    for j in range(len(arr[0])):
                        if(distance_2d(location,arr[i][j])<distance):
                            distance = distance_2d(location,arr[i][j])
                            value = answer[i][j]
                            pt = (i,j)

                distance2 = float(math.inf)
                pt2 = (-1,-1)
                value2 = 0

                for i in range(len(selection_nums)):
                    if(distance_2d(location,selection_nums[i])<distance2):
                        distance2 = distance_2d(location,selection_nums[i])
                        value2 = i+1
                        pt2 = selection_nums[i]
                
                if(min(distance,distance2) == distance_2d(location,selection_nums[-1])):
                    pointer_text = "x"
                elif(pointer_text != "x" and distance < distance2):
                    if(puzzle[pt[0]][pt[1]] == 0 and value == int(pointer_text)):
                        puzzle[pt[0]][pt[1]] = value
                        pointer_text = "x"
                    elif(puzzle[pt[0]][pt[1]] == 0 and value != int(pointer_text)):
                        area_count -= 8
                        lives -= 1
                    
                elif(pointer_text == "x" and distance2 < distance):
                    pointer_text = str(value2)
        

        cv2.imshow("New",frame)
        hasFrame, frame = cap.read()
        if cv2.waitKey(1)  == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    