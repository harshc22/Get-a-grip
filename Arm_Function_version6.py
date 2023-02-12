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

def move_arm (location): #moving the arm
    state=False #boolean variable checks if the function is completed 
    while state==False:#The loop runs until the arm is moved 
        thres_left=arm.emg_left()
        thres_right=arm.emg_right()
        time.sleep(0.25)
        #gets the threshold values for both muscles
        
        if thres_left>0.5 and thres_right <0.5 and thres_right != thres_left: #moves the arm if left muscle sensor passes the threshold value
            arm.move_arm(location[0],location[1],location[2])
            print("Arm moved to the assigned location")
            state=True
        
    return


def bin_location(bin_id):#hold the locations of all bins 
    if bin_id==1: #Red small
        location=[-0.5709, 0.2306, 0.3853]
            
    elif bin_id==2: #Green small
        location=[-0.0015, -0.6166, 0.3831]
            
    elif bin_id==3: #Blue small
        location=[0.0015, 0.6166, 0.3831]
            
    elif bin_id==4: #Red large
        location=[-0.4268, 0.1725, 0.3150]
            
    elif bin_id==5: #Green large
        location=[0.0, -0.4604, 0.3190]
            
    elif bin_id==6: #Blue large
        location=[0.0, 0.4604, 0.3140]
            
    return location

def open_bin(ID): #opens the bin
    check=False #boolean to check if the bin is opened 
    while check==False: #loop runs until the bin is opened 
        thres_left=arm.emg_left()
        thres_right=arm.emg_right()
        time.sleep(0.25)
        #the muscle values are taken for comparison
        
        if thres_left == thres_right and thres_right>0.5 and thres_left>0.5:
        #opens the bin if the right muscle value is same as left and they both over the threhold
            
            if ID==4: #red autoclave
                arm.open_red_autoclave(not check)
                print("Bin opened")
                check=True
            elif ID==5: #green autoclave
                arm.open_green_autoclave(not check)
                print("Bin opened")
                check=True
            elif ID==6: #blue autoclave
                arm.open_blue_autoclave(not check)
                print("Bin opened")
                check=True
            elif ID==1 or ID==2 or ID==3:
                check=True #Doesn't do anything if the container is small 
        #opens the bin based on colour if both muscle thresholds are over 0.5 and exits the loop
    return

def close_bin(ID): #closes the bin
    check=False
    while(check==False): #loop runs until the bin is closed
        thres_left=arm.emg_left()
        thres_right=arm.emg_right()
        time.sleep(0.25)
        #the muscle values are taken for comparison
        
        if thres_left == thres_right and thres_right>0.5 and thres_left>0.5:
        #closes the bin when right and left value are over the threshold and equal each other
            
            if ID==4:#red autoclave
                arm.open_red_autoclave(check)
                print("Bin closed")
                check=True
                
            elif ID==5:#green autoclave
                arm.open_green_autoclave(check)
                print("Bin closed")
                check=True
                
            elif ID==6:#blue autoclave
                arm.open_blue_autoclave(check)
                print("Bin closed")
                check=True
            #closes the bins based on their colour 

def drop_mic(ID): #drops the container 
    check=False
    while(check==False):
        thres_right=arm.emg_right()
        thres_left=arm.emg_left()
        time.sleep(0.25)
        #gets the threshold values for both muscles
        
        if thres_right>0.5 and thres_left < 0.5 and thres_right != thres_left:
        #drops the container only when the right muscle value is over 0.5
            if ID==1 or ID==2 or ID==3:
                arm.control_gripper(-35)
                print("Container is dropped")
                time.sleep(2)
                check=True
            else:
                arm.control_gripper(-28)
                print("Container is dropped")
                time.sleep(2)
                check=True

        

def spawn_container(container,i): #spawns the container 
    ID=container[random.randint(0,5-i)] #indexing the values at random

    if ID in container:
        container.remove(ID)
        arm.spawn_cage(ID)
        print("Container no. ",ID, " spawned")
    #removes the ID if it's in the container list
    #spawns the contaianer of that ID
    return ID #returns the ID number



def pick_container(ID): #picks up the container 
    check=False #boolean to check if container is picked 
    while check==False: #the loop runs until the container is picked up
        thres_left=arm.emg_left()
        thres_right=arm.emg_right()
        #gets the threshold value of both muscles
        
        time.sleep(0.25)
        if thres_right>0.5 and thres_left <0.5 and thres_right != thres_left: #only when right muslce is over threshold 
            time.sleep(1)
            if ID==1 or ID==2 or ID==3: #small containers 
                arm.control_gripper(35)
                print("The container is picked up")
                check=True
            else: #big containers 
                arm.control_gripper(28)
                print("The container is picked up")
                check=True
        #if the threshold value of right muscle is over 0.5, the container is picked up
        #If the container is big, the gripper is not closed fully 
    
    
def main(): #main function
    container=[1,2,3,4,5,6] #list for the containers 
    pick_up_location = [0.4989, 0.0009, 0.0407] #pick up location for the container 
    rise = [0.4064, 0.0, 0.4826] #rise location to avoid hitting the bins 
   
    
    for i in range(6): #loop runs 6 times for 6 containers 
        arm.home() #the arm starts from home location 
        time.sleep(1) #waits for one second
        
        ID=spawn_container(container,i) #random container is selected 
        time.sleep(1)
        
        location=bin_location(ID) #location for the container is extracted
        
        move_arm(pick_up_location)#arm moves to the container pick up location
        pick_container(ID)#arm picks up the container 
        time.sleep(1)
        move_arm(rise)#rises high enough to avoid hitting the bins
        time.sleep(1)
        
        if ID == 1 or ID == 2 or ID == 3: #intructions for small containers 
            move_arm(location) #arm moves to the location of container
            time.sleep(1)
            drop_mic(ID)#the container is dropped
            time.sleep(1)
            
        else: #instructions for big containers 
            move_arm(location) #arm moves to the location of container
            time.sleep(1)
            open_bin(ID) #the bin is opened based on the colour
            drop_mic(ID) #the container is dropped 
            time.sleep(1)
            close_bin(ID) #the bin is closed 
            time.sleep(1)

        
        print("Process finished for container no.",ID)
        print("--------------------------------------")
        
    arm.home() #arm return back to home after containers are dropped
    print("All containers dropped")
    

    
    
main()


    
            
            
            
    

