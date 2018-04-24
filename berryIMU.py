#!/usr/bin/python
#
#    This program  reads the angles from the acceleromter, gyrscope
#    and mangnetometeron a BerryIMU connected to a Raspberry Pi.
#
#    This program includes two filters (low pass and mdeian) to improve the
#    values returned from BerryIMU by reducing noise.
#
#
#    http://ozzmaker.com/
#    Both the BerryIMUv1 and BerryIMUv2 are supported
#




import sys
import time
import math
import IMU
import datetime
import os
from tkinter import  *
IMU_upside_down = 0 	# Change calculations depending on IMu orientation.
                                                # 0 = Correct side up. This is when the skull logo is facing down
                                                # 1 = Upside down. This is when the skull logo is facing up


RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  	# [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      	# Complementary filter constant
MAG_LPF_FACTOR = 0.4 	# Low pass filter constant magnetometer
GYR_HPF_FACTOR = 0.8
ACC_LPF_FACTOR = 0.4 	# Low pass filter constant for accelerometer
ACC_MEDIANTABLESIZE = 10    	# Median filter table size for accelerometer. Higher = smoother but a longer delay
MAG_MEDIANTABLESIZE = 10    	# Median filter table size for magnetometer. Higher = smoother but a longer delay
ACCx_Sample = 0.0
ACCy_Sample = 0.0
ACCx_ref = 0.0
ACCy_ref = 0.0
GYRx_Sample = 0.0
GYRy_Sample = 0.0
GYRz_Sample = 0.0
GYRx_ref = 0.0
GYRy_ref = 0.0
GYRz_ref = 0.0
calibration_count = 0
a = datetime.datetime.now()
ori_x = 400
ori_y = 300
#Kalman filter variables
Q_angle = 0.02
Q_gyro = 0.0015
R_angle = 0.005
y_bias = 0.0
x_bias = 0.0
XP_00 = 0.0
XP_01 = 0.0
XP_10 = 0.0
XP_11 = 0.0
YP_00 = 0.0
YP_01 = 0.0
YP_10 = 0.0
YP_11 = 0.0
KFangleX = 0.0
KFangleY = 0.0
magXmax = 2840
magYmax = 775
magZmax = 1223
magXmin = -43
magYmin = -1783
magZmin = -1916
declination = -36.36 / 1000.0
#

#
count_vx = 0
count_vy = 0
Disp_x = 0.0
Disp_y = 0.0
Vel_x = 0.0
Vel_y = 0.0
Vel_x_pre = 0.0
Vel_y_pre = 0.0
ACCx_pre = 0.0
ACCy_pre = 0.0
rate_gyr_x_pre = 0.0
rate_gyr_y_pre = 0.0
rate_gyr_z_pre = 0.0
T= 0.035
gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0
CFangleXFiltered = 0.0
CFangleYFiltered = 0.0
kalmanX = 0.0
kalmanY = 0.0
oldXMagRawValue = 0
oldYMagRawValue = 0
oldZMagRawValue = 0
oldXAccRawValue = 0
oldYAccRawValue = 0
oldZAccRawValue = 0

oldXGYRRawValue = 0
oldYGYRRawValue = 0
oldZGYRRawValue = 0

n = 0

#Setup the tables for the mdeian filter. Fill them all with '1' soe we dont get devide by zero error
acc_medianTable1X = [1] * ACC_MEDIANTABLESIZE
acc_medianTable1Y = [1] * ACC_MEDIANTABLESIZE
acc_medianTable1Z = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2X = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2Y = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2Z = [1] * ACC_MEDIANTABLESIZE
mag_medianTable1X = [1] * MAG_MEDIANTABLESIZE
mag_medianTable1Y = [1] * MAG_MEDIANTABLESIZE
mag_medianTable1Z = [1] * MAG_MEDIANTABLESIZE
mag_medianTable2X = [1] * MAG_MEDIANTABLESIZE
mag_medianTable2Y = [1] * MAG_MEDIANTABLESIZE
mag_medianTable2Z = [1] * MAG_MEDIANTABLESIZE

def judge(evex,evey):
    mainhall = evex>130 and evex<820 and evey>120 and evey<580
    womensroom = evex>130 and evex<310 and evey>580 and evey<640
    mensroom = evex>660 and evex<850 and evey>580 and evey<640
    conE = evex>350 and evex<430 and evey>580 and evey<640
    conW = evex>540 and evex<630 and evey>580 and evey<640
    A = evex>310 and evex<350 and evey>580 and evey<640
    B = evex>430 and evex<540 and evey>580 and evey<640
    C = evex>630 and evex<660 and evey>580 and evey<640
    D = evex>70 and evex<390 and evey>640 and evey<690
    D1 = evex>70 and evex<130 and evey>550 and evey<640
    E = evex>390 and evex<585 and evey>640 and evey<690
    F = evex>585 and evex<990 and evey>640 and evey<690
    F1 = evex>850 and evex<990 and evey>580 and evey<640
    G = evex>20 and evex<130 and evey>120 and evey<550
    H = evex>20 and evex<230 and evey>70 and evey<120
    I = evex>230 and evex<370 and evey>70 and evey<120
    J1 = evex>370 and evex<480 and evey>70 and evey<120
    J2 = evex>480 and evex<605 and evey>70 and evey<120
    K1 = evex>605 and evex<780 and evey>70 and evey<120
    K2 = evex>780 and evex<840 and evey>70 and evey<120
    FHC = evex>820 and evex<840 and evey>120 and evey<580
    STAIR4 = evex>740 and evex<810 and evey>35 and evey<70
    ELECTRICROOM = evex>810 and evex<850 and evey>35 and evey<70
    l = evex>840 and evex<875 and evey>55 and evey<250
    M = evex>840 and evex<960 and evey>25 and evey<55
    N = evex>840 and evex<900 and evey>250 and evey<280
    O = evex>900 and evex<990 and evey>250 and evey<570
    P = evex>875 and evex<910 and evey>55 and evey<100
    Q = evex>875 and evex<910 and evey>100 and evey<190
    R = evex>875 and evex<910 and evey>190 and evey<220
    S = evex>875 and evex<910 and evey>220 and evey<240
    T = evex>840 and evex<900 and evey>275 and evey<380
    U = evex>840 and evex<900 and evey>380 and evey<405
    V1 = evex>840 and evex<865 and evey>440 and evey<570
    V2 = evex>840 and evex<900 and evey>400 and evey<440
    V3 = evex>865 and evex<900 and evey>440 and evey<500
    V4 = evex>865 and evex<900 and evey>500 and evey<520
    if  mainhall:
      cv.create_line(currentx,currenty,evex,evey,fill = "black",width = 5,dash = (10,10))
    elif womensroom:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash = (10,10))
      cv.create_line(330,580,310,620,fill = "black",width = 5,dash = (10,10))
      cv.create_line(310,620,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif mensroom:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash = (10,10))
      cv.create_line(645,580,660,620,fill = "black",width = 5,dash = (10,10))
      cv.create_line(660,620,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif conE:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,580,350,620,fill = "black",width = 5,dash =(10,10))
      cv.create_line(350,620,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif conW:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,580,630,620,fill = "black",width = 5,dash =(10,10))
      cv.create_line(630,620,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif A:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,580,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif B:
      cv.create_line(currentx,currenty,495,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(495,580,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif C:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,580,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif D:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,580,330,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,645,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif D1:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,580,330,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,645,130,670,fill = "black",width = 5,dash =(10,10))
      cv.create_line(130,670,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif E:
      cv.create_line(currentx,currenty,485,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(485,580,485,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(485,645,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif F:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,580,645,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,645,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif F1:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,580,645,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,645,855,670,fill = "black",width = 5,dash =(10,10))
      cv.create_line(855,670,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif G:
      cv.create_line(currentx,currenty,210,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(210,120,130,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(130,100,80,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(80,120,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif H:
      cv.create_line(currentx,currenty,210,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(210,120,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif I:
      cv.create_line(currentx,currenty,350,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(350,120,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif J1:
      cv.create_line(currentx,currenty,385,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(385,120,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif J2:
      cv.create_line(currentx,currenty,590,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(590,120,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif K1:
      cv.create_line(currentx,currenty,625,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(625,120,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif K2:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif FHC:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif STAIR4:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,795,70,fill = "black",width = 5,dash =(10,10))
      cv.create_line(795,70,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif ELECTRICROOM:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,820,70,fill = "black",width = 5,dash =(10,10))
      cv.create_line(820,70,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif l:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,100,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif M:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,55,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,55,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif N:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,250,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,250,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif O:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,910,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(910,260,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif P:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,100,875,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(875,100,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif Q:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,100,875,110,fill = "black",width = 5,dash =(10,10))
      cv.create_line(875,110,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif R:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,100,875,200,fill = "black",width = 5,dash =(10,10))
      cv.create_line(875,200,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif S:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,100,870,235,fill = "black",width = 5,dash =(10,10))
      cv.create_line(870,235,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif T:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,250,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,250,860,275,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,275,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif U:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,250,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,250,860,275,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,275,850,380,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,380,evex,evey,fill = "black",width = 5,dash = (10,10))

    elif V1:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,835,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,500,850,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,500,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif V2:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,835,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,500,850,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,500,855,440,fill = "black",width = 5,dash =(10,10))
      cv.create_line(855,440,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif V3:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,835,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,500,850,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,500,865,485,fill = "black",width = 5,dash =(10,10))
      cv.create_line(865,485,evex,evey,fill = "black",width = 5,dash =(10,10))

    elif V4:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,835,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,500,850,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,500,865,510,fill = "black",width = 5,dash =(10,10))
      cv.create_line(865,510,evex,evey,fill = "black",width = 5,dash =(10,10))
but_on = 0
def paint( event ):
    global currentx
    global currenty
    global ex
    global ey
    global but_on

    but_on = 1
    #print("currentx_b = %d currenty_b = %d" % (currentx,currenty))
    cv.delete(ALL)
    cv.create_image((550,350),image=img)
    cv.create_oval(currentx-7,currenty-7,currentx+7,currenty+7,fill = "blue")
    x1, y1 = ( event.x - 7 ), ( event.y - 7 )
    x2, y2 = ( event.x + 7 ), ( event.y + 7 )
    ex=event.x
    ey=event.y
    d = cv.create_oval( x1, y1, x2, y2, fill = "red" )
    print(event.x,event.y)
    judge(event.x,event.y)
    #print("currentx_a= %d currenty_a = %d" % (currentx,currenty))


def paint2(eventx,eventy,ft):
    global currentx
    global currenty
    #print("currentx_b = %d currenty_b = %d" % (currentx,currenty))
    cv.delete(ALL)
    cv.create_image((550,350),image=img)
    cv.create_oval(currentx-7,currenty-7,currentx+7,currenty+7,fill = "blue")
    x1, y1 = ( eventx - 7 ), ( eventy - 7 )
    x2, y2 = ( eventx + 7 ), ( eventy + 7 )
    if (ft==1):
        d = cv.create_oval( x1, y1, x2, y2, fill = "red" )
        print(eventx,eventy)
        judge(eventx,eventy)
    #print("currentx_a= %d currenty_a = %d" % (currentx,currenty))

def kalmanFilterY ( accAngle, gyroRate, DT):
    y=0.0
    S=0.0

    global KFangleY
    global Q_angle
    global Q_gyro
    global y_bias
    global YP_00
    global YP_01
    global YP_10
    global YP_11

    KFangleY = KFangleY + DT * (gyroRate - y_bias)

    YP_00 = YP_00 + ( - DT * (YP_10 + YP_01) + Q_angle * DT )
    YP_01 = YP_01 + ( - DT * YP_11 )
    YP_10 = YP_10 + ( - DT * YP_11 )
    YP_11 = YP_11 + ( + Q_gyro * DT )

    y = accAngle - KFangleY
    S = YP_00 + R_angle
    K_0 = YP_00 / S
    K_1 = YP_10 / S

    KFangleY = KFangleY + ( K_0 * y )
    y_bias = y_bias + ( K_1 * y )

    YP_00 = YP_00 - ( K_0 * YP_00 )
    YP_01 = YP_01 - ( K_0 * YP_01 )
    YP_10 = YP_10 - ( K_1 * YP_00 )
    YP_11 = YP_11 - ( K_1 * YP_01 )

    return KFangleY

def kalmanFilterX ( accAngle, gyroRate, DT):
    x=0.0
    S=0.0

    global KFangleX
    global Q_angle
    global Q_gyro
    global x_bias
    global XP_00
    global XP_01
    global XP_10
    global XP_11
    global gyroXangle
    global gyroYangle
    global gyroZangle


    KFangleX = KFangleX + DT * (gyroRate - x_bias)

    XP_00 = XP_00 + ( - DT * (XP_10 + XP_01) + Q_angle * DT )
    XP_01 = XP_01 + ( - DT * XP_11 )
    XP_10 = XP_10 + ( - DT * XP_11 )
    XP_11 = XP_11 + ( + Q_gyro * DT )

    x = accAngle - KFangleX
    S = XP_00 + R_angle
    K_0 = XP_00 / S
    K_1 = XP_10 / S

    KFangleX = KFangleX + ( K_0 * x )
    x_bias = x_bias + ( K_1 * x )

    XP_00 = XP_00 - ( K_0 * XP_00 )
    XP_01 = XP_01 - ( K_0 * XP_01 )
    XP_10 = XP_10 - ( K_1 * XP_00 )
    XP_11 = XP_11 - ( K_1 * XP_01 )

    return KFangleX


IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass


root=Tk()
root.title('Indoor Nevigation')
cv=Canvas(root,bg='white',width=1100,height=2500)
img=PhotoImage(file='pyimage2.png')
cv.create_image((550,350),image=img)
cv.pack()

#cv.create_oval(currentx-7,currenty-7,currentx+7,currenty+7,fill = "#146FF8")
#cv.bind("<Button-1>",paint)
def locating():
    global a
    global b
    global c
    global d
    global currentx
    global currenty
    global n
    global ACCx_Sample
    global ACCy_Sample
    global GYRx_Sample
    global GYRy_Sample
    global GYRz_Sample
    global GYRx_ref
    global GYRy_ref
    global GYRz_ref
    global oldXMagRawValue
    global oldYMagRawValue
    global oldZMagRawValue
    global oldXAccRawValue
    global oldYAccRawValue
    global oldZAccRawValue
    global oldXGYRRawValue
    global oldYGYRRawValue
    global oldZGYRRawValue
    global gyroXangle
    global gyroYangle
    global gyroZangle
    global count_vx
    global count_vy
    global Disp_x
    global Disp_y
    global Vel_x
    global Vel_y
    global Vel_x_pre
    global Vel_y_pre
    global ACCx_pre
    global ACCy_pre
    global rate_gyr_x_pre
    global rate_gyr_y_pre
    global rate_gyr_z_pre
    global T
    global CFangleX
    global CFangleY
    global CFangleXFiltered
    global CFangleYFiltered
    global ex
    global ey
    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()

    MAGx -=(magXmin+magXmax)/2.0
    MAGy -=(magYmin+magYmax)/2.0
    MAGz -=(magZmin+magZmax)/2.0

    ##Calculate loop Period(LP). How long between Gyro Reads

    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    T = b.microseconds/(1000000*1.0)
    print ("Loop Time | %7.4f|" % ( T )),

    ###############################################
    #### High pass filter ACC ####
    ###############################################
    GYRx =  oldXGYRRawValue  * GYR_HPF_FACTOR + GYRx*(1 - GYR_HPF_FACTOR);
    GYRy =  oldYGYRRawValue  * GYR_HPF_FACTOR + GYRy*(1 - GYR_HPF_FACTOR);
    GYRz =  oldZGYRRawValue  * GYR_HPF_FACTOR + GYRz*(1 - GYR_HPF_FACTOR);

    oldXGYRRawValue = GYRx
    oldYGYRRawValue = GYRy
    oldZGYRRawValue = GYRz

    ###############################################
    #### reference calibration for ACC ####
    ###############################################
    print (" ")
    print (" n= %d" % (n))
    if n <50:
        n += 1
        ACCx_Sample += ACCx
        ACCy_Sample += ACCy
    print (" ")
    print (" n= %d" % (n))
    print ("\033[1;34;40mACCx_raw_G  %7.4f ACCy_raw_G  %7.4f  \033[0m  " % ((ACCx * 0.244)/1000, (ACCy * 0.244)/1000)),
    print (" ")
    # print (" ACCx_raw %5.2f   ACCy_raw  %5.2f " % (ACCx , ACCy))

    ACCx_ref = ACCx_Sample / 50
    ACCy_ref = ACCy_Sample / 50

    ACCx -= ACCx_ref
    ACCy -= ACCy_ref
    # print (" ACCx_ref %5.2f   ACCy_ref  %5.2f " % (ACCx_ref , ACCy_ref))

    ###############################################
    #### reference calibration for Gyro ####
    ###############################################

    if n <50:
        n += 1
        GYRx_Sample += GYRx
        GYRy_Sample += GYRy
        GYRz_Sample += GYRz

    GYRx_ref = GYRx_Sample / 50
    GYRy_ref = GYRy_Sample / 50
    GYRz_ref = GYRz_Sample / 50

    GYRx -= GYRx_ref
    GYRy -= GYRy_ref
    GYRz -= GYRz_ref
    ###############################################
    #### Apply low pass filter ####
    ###############################################
    MAGx =  MAGx  * MAG_LPF_FACTOR + oldXMagRawValue*(1 - MAG_LPF_FACTOR);
    MAGy =  MAGy  * MAG_LPF_FACTOR + oldYMagRawValue*(1 - MAG_LPF_FACTOR);
    MAGz =  MAGz  * MAG_LPF_FACTOR + oldZMagRawValue*(1 - MAG_LPF_FACTOR);
    ACCx =  ACCx  * ACC_LPF_FACTOR + oldXAccRawValue*(1 - ACC_LPF_FACTOR);
    ACCy =  ACCy  * ACC_LPF_FACTOR + oldYAccRawValue*(1 - ACC_LPF_FACTOR);
    ACCz =  ACCz  * ACC_LPF_FACTOR + oldZAccRawValue*(1 - ACC_LPF_FACTOR);

    oldXMagRawValue = MAGx
    oldYMagRawValue = MAGy
    oldZMagRawValue = MAGz
    oldXAccRawValue = ACCx
    oldYAccRawValue = ACCy
    oldZAccRawValue = ACCz


    #########################################
    #### Median filter for accelerometer ####
    #########################################
    # cycle the table
    for x in range (ACC_MEDIANTABLESIZE-1,0,-1 ):
            acc_medianTable1X[x] = acc_medianTable1X[x-1]
            acc_medianTable1Y[x] = acc_medianTable1Y[x-1]
            acc_medianTable1Z[x] = acc_medianTable1Z[x-1]

    # Insert the lates values
    acc_medianTable1X[0] = ACCx
    acc_medianTable1Y[0] = ACCy
    acc_medianTable1Z[0] = ACCz

    # Copy the tables
    acc_medianTable2Y = acc_medianTable1Y[:]
    acc_medianTable2X = acc_medianTable1X[:]
    acc_medianTable2Z = acc_medianTable1Z[:]

    # Sort table 2
    acc_medianTable2X.sort()
    acc_medianTable2Y.sort()
    acc_medianTable2Z.sort()

    # The middle value is the value we are interested in
    ACCx = acc_medianTable2X[5];
    ACCy = acc_medianTable2Y[5];
    ACCz = acc_medianTable2Z[5];




            #########################################
    #### Median filter for magnetometer ####
    #########################################
    # cycle the table
    for x in range (MAG_MEDIANTABLESIZE-1,0,-1 ):
            mag_medianTable1X[x] = mag_medianTable1X[x-1]
            mag_medianTable1Y[x] = mag_medianTable1Y[x-1]
            mag_medianTable1Z[x] = mag_medianTable1Z[x-1]

    # Insert the latest values
    mag_medianTable1X[0] = MAGx
    mag_medianTable1Y[0] = MAGy
    mag_medianTable1Z[0] = MAGz

    # Copy the tables
    mag_medianTable2X = mag_medianTable1X[:]
    mag_medianTable2Y = mag_medianTable1Y[:]
    mag_medianTable2Z = mag_medianTable1Z[:]

    # Sort table 2
    mag_medianTable2X.sort()
    mag_medianTable2Y.sort()
    mag_medianTable2Z.sort()

    # The middle value is the value we are interested in
    MAGx = mag_medianTable2X[5];
    MAGy = mag_medianTable2Y[5];
    MAGz = mag_medianTable2Z[5];


    ###############################################
    ####                                       ####
    ###############################################
    #Convert Gyro raw to degrees per second
    rate_gyr_x =  GYRx * G_GAIN
    rate_gyr_y =  GYRy * G_GAIN
    rate_gyr_z =  GYRz * G_GAIN


    #Calculate the angles from the gyro.
    gyroXangle+=rate_gyr_x_pre*T+((rate_gyr_x-rate_gyr_x_pre) * T)/ 2
    gyroYangle+=rate_gyr_y_pre*T+((rate_gyr_y-rate_gyr_y_pre) * T)/ 2
    gyroZangle+=rate_gyr_z_pre*T+((rate_gyr_z-rate_gyr_z_pre) * T)/ 2
    rate_gyr_x_pre = rate_gyr_x
    rate_gyr_y_pre = rate_gyr_y
    rate_gyr_z_pre = rate_gyr_z
    ###############################################
    #### Machinenary filter ####
    ###############################################
    if ((ACCx > -70) & (ACCx < 70)):
         ACCx = 0.0
    if ((ACCy > -70) & (ACCy < 70)):
         ACCy = 0.0
    print (" ")
    print ("\033[1;34;40mACCx_ref_ed_G  %7.4f ACCy_ref_ed_G  %7.4f  \033[0m  " % ((ACCx * 0.732)/1000, (ACCy * 0.732)/1000)),
    print (" ")
    print (" ACCz_G%5.2f" % ((ACCz * 0.732)/1000))
    ###############################################
    #### Caulculate displacement ####
    ###############################################
    ACCx_now = (ACCx * 0.732) /1000
    ACCy_now = (ACCy * 0.732) /1000


    Vel_x += (ACCx_pre * T) + ((ACCx_now - ACCx_pre) * T) / 2
    ACCx_pre = ACCx_now

    if (ACCx_now == 0.0) :
        count_vx += 1
    else :
        count_vx = 0
    if (count_vx >=25):
        Vel_x = 0.0

    Disp_x += (Vel_x_pre * T) + ((Vel_x - Vel_x_pre) * T) / 2
    Vel_x_pre = Vel_x
    Vel_y += (ACCy_pre * T) + ((ACCy_now - ACCy_pre) * T) / 2
    ACCy_pre = ACCy_now

    if (ACCy_now == 0.0) :
        count_vy += 1
    else  :
        count_vy = 0
    if (count_vy >=25):
        Vel_y = 0.0

    Disp_y += (Vel_y_pre * T) + ((Vel_y - Vel_y_pre) * T) / 2
    Vel_y_pre = Vel_y

    if (Disp_x <= -3.7):
        Disp_x = -3.7
    if (Disp_x > 5):
        Disp_x = 5
    if (Disp_y <= -2.4):
        Disp_y = -2.4
    if (Disp_y > 4):
        Disp_y = 4
    print (" ")
    print ("\033[0;33m Vel_x=  %5.2f   Vel_y=  %5.2f " % (Vel_x*100 , Vel_y*100))
    print (" ")
    print ("\033[0;31m Disp_x=  %5.2f   Disp_y=  %5.2f " % (Disp_x *100 , Disp_y *100))
    print (" ")



    ##Convert Accelerometer values to degrees
    AccXangle =  (math.atan2(ACCy,ACCz)+M_PI)*RAD_TO_DEG
    AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG




    # Change the rotation value of the accelerometer to -/+ 180 and move the Y axis '0' point to up
    # Two different pieces of code are used depending on how your IMU is mounted
    if IMU_upside_down : 		# If IMU is upside down E.g Skull logo is facing up.
            if AccXangle >180:
                    AccXangle -= 360.0
                    AccYangle-=90
            if AccYangle >180:
                    AccYangle -= 360.0

    else : 						# If IMU is up the correct way E.g Skull logo is facing down.
            AccXangle -= 180.0
            if AccYangle > 90:
                    AccYangle -= 270.0
            else:
                    AccYangle += 90.0



    #Complementary filter used to combine the accelerometer and gyro values.
    CFangleX=AA*(CFangleX+rate_gyr_x*T) +(1 - AA) * AccXangle
    CFangleY=AA*(CFangleY+rate_gyr_y*T) +(1 - AA) * AccYangle

    #Kalman filter used to combine the accelerometer and gyro values.
    kalmanY = kalmanFilterY(AccYangle, rate_gyr_y,T)
    kalmanX = kalmanFilterX(AccXangle, rate_gyr_x,T)



    if IMU_upside_down :
            MAGy = -MAGy

    #Calculate heading
    heading = 180 * math.atan2(MAGy,MAGx)/M_PI

    #Only have our heading between 0 and 360
    if heading < 0:
            heading += 360

    heading = heading - declination * 180/M_PI


    #Normalize accelerometer raw values.
    accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
    accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


    #Calculate pitch and roll
    if IMU_upside_down :
            accXnorm = -accXnorm				#flip Xnorm as the IMU is upside down
            accYnorm = -accYnorm				#flip Ynorm as the IMU is upside down
            pitch = math.asin(accXnorm)
            roll = math.asin(accYnorm/math.cos(pitch))
    else :
            pitch = math.asin(accXnorm)
            roll = -math.atan(ACCy/ACCz)


    #Calculate the new tilt compensated values
    magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
    magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)

    #Calculate tilt compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

    #Only have our heading between 0 and 360
    if tiltCompensatedHeading < 0:
            tiltCompensatedHeading += 360

    #print ("FFFFFFUUUUUUCCCCK")
    #if 1:			#Change to '0' to stop showing the angles from the accelerometer
    #	print ("\033[1;34;40mACCX Angle %5.2f ACCY Angle %5.2f  \033[0m  " % (AccXangle, AccYangle)),

    #if 1:			#Change to '0' to stop  showing the angles from the gyro
    print ("\033[1;31;40m\tGRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f" % (gyroXangle,gyroYangle,gyroZangle)),

    #if 1:			#Change to '0' to stop  showing the angles from the complementary filter
    print ("\033[1;35;40m   \tCFangleX Angle %5.2f \033[1;36;40m  CFangleY Angle %5.2f \33[1;32;40m" % (CFangleX,CFangleY)),


    print ("HEADING  %5.2f \33[1;37;40m tiltCompensatedHeading %5.2f" % (heading,tiltCompensatedHeading)),

    #if 1:			#Change to '0' to stop  showing the angles from the Kalman filter
    print ("\033[1;31;40m kalmanX %5.2f  \033[1;35;40m kalmanY %5.2f  " % (kalmanX,kalmanY)),

    #print(" ")

    #slow program down a bit, makes the output more readable
    #time.sleep(0.03)

    currentx =ori_x + round(Disp_x * 100)
    currenty =ori_y + round(Disp_y * 100)
    if (currentx <=30):
        currentx = 30
    if (currentx >=900):
        currentx = 900
    if (currenty <=80):
        currentx = 80
    if (currenty >=700):
        currenty = 700
    #print("currentx = %d    currenty = %d" % (currentx,currenty))
    cv.update()
    cv.create_oval(currentx-7,currenty-7,currentx+7,currenty+7,fill = "#146FF8")
    cv.bind("<Button-1>",paint)
    if (but_on  == 1 ):
        paint2(ex,ey,1)
    else :
        paint2(currentx,currenty,0)
    print("currentx = %d currenty = %d" % (currentx,currenty))

    cv.after(1,locating)
cv.after(1,locating)

root.mainloop()



