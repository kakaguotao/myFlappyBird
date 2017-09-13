import pygame
from pygame.locals import *
from sys import exit
import time
import numpy as np

def compute_position(current_time,last_frame_time,last_press_time,bird_pos,bird_vel,bird_acc):
    if current_time-last_press_time<0.2:
        acc=-bird_acc*2
    else:
        acc=bird_acc
    time_diff=current_time-last_frame_time
    new_vel=bird_vel+time_diff*acc
    new_pos=bird_pos+time_diff*bird_vel+acc*time_diff*time_diff
    return new_pos,new_vel

def add_block(block_list,block_hole_size):
    block_pair=[640,np.random.randint(50,480-block_hole_size-50),True]
    block_list.append(block_pair)
    return block_list


def update_block(current_time,last_frame_time,block_list,block_moving_vel,block_distance,block_width,block_hole_size):
    time_diff=current_time-last_frame_time
    for block in block_list:
        block[0]=block[0]-time_diff*block_moving_vel
    if block_list[-1][0]<(640-block_distance):
        block_list=add_block(block_list,block_hole_size)
    if block_list[0][0]<(-block_width):
        del block_list[0]
    return block_list


pygame.init()
screen=pygame.display.set_mode((640,480),0,32)

#the state of bird
#the y position of bird
bird_pos=239
#the y velocity of bird
bird_vel=0
#the y acceleration velocity of bird
#if the key is pressed, in the following 0.2s, the bird fly up
bird_acc=700
bird_x_pos=200
bird_r=20


#start time
start_time=time.time()
#last_press_time
last_press_time=-0.2
#last frame time
last_frame_time=0

if_start=False

block_list=[]
block_moving_vel=300
block_distance=300
block_width=100
block_hole_size=200

block_list=add_block(block_list,block_hole_size)

font=pygame.font.SysFont('arial',40)
over_font=pygame.font.SysFont('arial',80)

score=0

if_conflict=False

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
        if event.type==KEYDOWN:
            if event.key==K_UP and if_start:
                last_press_time=time.time()-start_time
                bird_vel=0
            elif event.key==K_UP and not if_start:
                start_time=time.time()
                if_start=True
            elif event.key==K_RIGHT and if_conflict:
                block_list=[]
                block_list=add_block(block_list,block_hole_size)
                score=0
                bird_vel=0
                bird_acc=700
                bird_pos=239
                if_conflict=False
                start_time=time.time()
                last_frame_time=0
                last_press_time=-0.2


    screen.fill((0,0,0))
    if not if_conflict:
        if if_start:
            current_time=time.time()-start_time
            bird_pos,bird_vel=compute_position(current_time,last_frame_time,last_press_time,bird_pos,bird_vel,bird_acc)
            if bird_pos<=0:
                bird_pos=0
                bird_vel=0
            if bird_pos>=479:
                bird_pos=479
                bird_vel=0
            block_list=update_block(current_time,last_frame_time,block_list,block_moving_vel,block_distance,block_width,block_hole_size)
            last_frame_time=current_time
        else:
            screen.blit(font.render('PRESS UP TO START!', True,(0,255,0)),(100,20))

        if bird_pos>480-bird_r or bird_pos<bird_r:
            if_conflict=True

    #draw block
    for block in block_list:
        #update score
        if (block[0]-bird_x_pos)<-(block_width/2) and block[2] is True:
            score+=1
            block[2]=False

        #conflict detect
        if bird_x_pos-block[0]>0 and bird_x_pos-block[0]<block_width:
            if bird_pos+bird_r>=block[1]+block_hole_size or bird_pos-bird_r<=block[1]:
                if_conflict=True

        pygame.draw.rect(screen,(255,255,255),(block[0],0,block_width,block[1]))
        pygame.draw.rect(screen,(255,255,255),(block[0],block[1]+block_hole_size,block_width,480-block_hole_size-block[1]))

    #draw bird
    pygame.draw.circle(screen,(0,255,0),(bird_x_pos,int(bird_pos)),bird_r)

    #draw score
    screen.blit(font.render('Score: %d'%(score), True,(255,0,0)),(20,400))

    #draw score and game over
    if if_conflict:
        screen.blit(over_font.render('Score: %d'%(score), True,(255,0,0)),(90,140))
        screen.blit(over_font.render('GAME OVER', True,(255,0,0)),(90,220))
        screen.blit(font.render('PRESS RIGHT TO RESTART!', True,(0,255,0)),(60,300))

    pygame.display.update()
