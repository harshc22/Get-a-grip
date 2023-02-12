## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.
import random
import time
import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)

## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Example to rotate the base: arm.rotateBase(90)

def move_arm (location): 
    state=False
    while(state==False):
        thres_left=arm.emg_left()
        thres_right=arm.emg_right()
        time.sleep(0.5)
        if(thres_left>0.5) and thres_right <0.5 and thres_right != thres_left: #moves the arm if muscle sensor passes the threshold value
            arm.move_arm(location[0],location[1],location[2])
            state=True
    return


def bin_location(bin_id):
    if bin_id==1: #Red small
        location=[-0.6237,0.252,0.4271]
            
    elif bin_id==2: #Green small
        location=[0.0, -0.6726, 0.4271]
            
    elif bin_id==3: #Blue small
        location=[0.0,0.6726,0.4271]
            
    elif bin_id==4: #Red large
        location=[-0.4268, 0.1725, 0.3150]
            
    elif bin_id==5: #Green large
        location=[0.0, -0.4604, 0.3190]
            
    elif bin_id==6: #Blue large
        location=[0.0, 0.4604, 0.3140]
            
    return location

def open_bin(ID):
    check=False
    while(check==False):
        thres_left=arm.emg_left()
        thres_right=arm.emg_right()
        time.sleep(0.5)
        if(thres_left == thres_right and thres_right>0.5 and thres_left>0.5):
            if(ID==4):
                arm.open_red_autoclave(not check)
                check=True
            elif(ID==5):
                arm.open_green_autoclave(not check)
                check=True
            elif(ID==6):
                arm.open_blue_autoclave(not check)
                check=True
            elif(ID==1)or(ID==2)or(ID==3):
                check=True
    return

def close_bin(ID):
    check=False
    if(ID==4):
        arm.open_red_autoclave(check)
        
    elif(ID==5):
        arm.open_green_autoclave(check)
        
    elif(ID==6):
        arm.open_blue_autoclave(check)
        

def drop_mic():
    check=False
    while(check==False):
        thres_right=arm.emg_right()
        thres_left=arm.emg_left()
        time.sleep(0.5)
        if thres_right>0.5 and thres_left < 0.5 and thres_right != thres_left:
            arm.control_gripper(-45)
            time.sleep(2)
            check=True
       
        

def spawn_container(cancel_list,container,i):
    ID=container[random.randint(0,5-i)]
    cancel_list.append(ID)
    if ID in container:
        container.remove(ID)
        arm.spawn_cage(ID)
    print(ID)
    print(container)
    return ID


def pick_container():
    check=False
    while(check==False):
        thres_left=arm.emg_left()
        thres_right=arm.emg_right()
        print(thres_left,thres_right)
        time.sleep(0.5)
        if(thres_right>0.5) and thres_left <0.5 and thres_right != thres_left:
            time.sleep(1)
            arm.control_gripper(45)
            check=True
    
    
def main():
    container=[1,2,3,4,5,6]
    cancel_list=[]
    pick_up_location = [0.4989, 0.0, 0.0407]
    rise = [0.4064, 0.0, 0.4826]
    
    for i in range(6):
        arm.home()
        time.sleep(1)
        ID=spawn_container(cancel_list,container,i)
        time.sleep(1)
        location=bin_location(ID)
        move_arm(pick_up_location)#pickup
        pick_container()
        time.sleep(1)
        move_arm(rise)#rise high enough
        time.sleep(1)
        if ID == 1 or ID == 2 or ID == 3:
            move_arm(location)
            time.sleep(1)
            drop_mic()
            time.sleep(1)
        else:
            move_arm(location)
            time.sleep(1)
            open_bin(ID)
            drop_mic()
            time.sleep(1)
            close_bin(ID)
            time.sleep(1)
    arm.home()

    
    
main()
#add and statements
#more accurate positions
#both arms flex need to do something unique

    
            
            
            
    

