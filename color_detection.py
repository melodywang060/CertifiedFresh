import cv2
import numpy as np
import pandas as pd
import argparse

#Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Reading the image with opencv
img = cv2.imread(img_path)
height = img.shape[0]
width = img.shape[1]
print("height, width; ")
print(height, width)
#totalPixels = height * width

#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def getRottenPixelRate():
    rottenPixels =0
    totalPixels = 0
    #print(totalPixels)
    for i in range(height):
        for j in range(width):
            currPixel = img[i,j]
            currR =currPixel[0] 
            currG =currPixel[1] 
            currB =currPixel[2] 
            #if currB < 250:
               # print(currB)
            if currR != 255 and currG !=250 and currB != 250:
                totalPixels += 1
            #print(currPixel)
            if (60 <=currR and currR <= 115 and currG < 85):
                #if 220 <= currR and currR <= 255 and 0 <=currG and currG <= 100: and 230 <= currR and currR <= 255 and 50 <=currG and currG <= 100)
                #print("here1: ")
                rottenPixels +=1 

                """ if 230 <= currR and currR <= 255 and :
                    print("here2: ")
                    perfectPixels += 1
            elif 50 <=currB and currB <= 100 and 0 <=currG and currG <= 50 and 230 <= currR and currR <= 240:
                    print("here3: ")
                    perfectPixels += 1 """
    
    #print("rottenPix:", rottenPixels)
    #print("totalPix:", totalPixels)
    return round((rottenPixels /totalPixels) * 10000, 4)
    
rottenScore = getRottenPixelRate()

def getRottenLevel(rottenRate):
    rottenLevel = ""
    if rottenRate > 50:
        rottenLevel = "Really Rotten"
    elif rottenRate >= 20 and rottenRate <=50:
        rottenLevel = "Mildly Rotten"
    else:
        rottenLevel = "Perfectly UnRotten"
    return rottenLevel
#print(getRottenPixelRate())      

#getGoodPixels()
#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        #print("I AM CLICKED")
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

        print("rgb: ")
        print(r,g,b)
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

while(1):

    cv2.imshow("image",img)
    rottenText1 = "Rotten Score: " + str(rottenScore) + "%" 
    rottenText2 = "Final Rotten Rating: " + getRottenLevel(rottenScore) 
    upperLeftTextOriginX = int(width * 0.1)
    upperLeftTextOriginY = int(height * 0.1)
    cv2.putText(img, rottenText1,(upperLeftTextOriginX,upperLeftTextOriginY),5,1.2,(0,0,0),1,cv2.LINE_AA)
    cv2.putText(img, rottenText2,(upperLeftTextOriginX,upperLeftTextOriginY+ int(0.3*upperLeftTextOriginY)),5,1.2,(0,0,0),1,cv2.LINE_AA)
    if (clicked):
        #print("CLICKED")
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(10,20), (660,60), (b,g,r), -1)

        #Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),5, 1.0 ,(255,255,255),2,cv2.LINE_AA)
        if (r + g + b < 350):
            rottenText3 = "Warning: Potential Rotten Area Detected"
            cv2.putText(img, rottenText3,(upperLeftTextOriginX -20,upperLeftTextOriginY+ 700),5,1.2,(0,0,0),1,cv2.LINE_AA)
        else:
            cv2.rectangle(img,(0,upperLeftTextOriginY+ 670), (675,upperLeftTextOriginY+ 750), (255,255,255), -1)
            
        #For very light colours we will display text in black colour
        if(r+g+b>=450):
            cv2.putText(img, text,(50,50),5,1.0,(0,0,0),2,cv2.LINE_AA)
        clicked=False

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break

 
cv2.destroyAllWindows()

