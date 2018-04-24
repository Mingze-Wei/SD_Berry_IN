from tkinter import  *

currentx = 485
currenty = 370

def paint( event ):
   mainhall = event.x>130 and event.x<820 and event.y>120 and event.y<580
   womensroom = event.x>130 and event.x<310 and event.y>580 and event.y<640
   mensroom = event.x>660 and event.x<850 and event.y>580 and event.y<640
   conE = event.x>350 and event.x<430 and event.y>580 and event.y<640
   conW = event.x>540 and event.x<630 and event.y>580 and event.y<640
   A = event.x>310 and event.x<350 and event.y>580 and event.y<640
   B = event.x>430 and event.x<540 and event.y>580 and event.y<640
   C = event.x>630 and event.x<660 and event.y>580 and event.y<640
   D = event.x>70 and event.x<390 and event.y>640 and event.y<690
   D1 = event.x>70 and event.x<130 and event.y>550 and event.y<640
   E = event.x>390 and event.x<585 and event.y>640 and event.y<690
   F = event.x>585 and event.x<990 and event.y>640 and event.y<690
   F1 = event.x>850 and event.x<990 and event.y>580 and event.y<640
   G = event.x>20 and event.x<130 and event.y>120 and event.y<550
   H = event.x>20 and event.x<230 and event.y>70 and event.y<120
   I = event.x>230 and event.x<370 and event.y>70 and event.y<120
   J1 = event.x>370 and event.x<480 and event.y>70 and event.y<120
   J2 = event.x>480 and event.x<605 and event.y>70 and event.y<120
   K1 = event.x>605 and event.x<780 and event.y>70 and event.y<120
   K2 = event.x>780 and event.x<840 and event.y>70 and event.y<120
   FHC = event.x>820 and event.x<840 and event.y>120 and event.y<580
   STAIR4 = event.x>740 and event.x<810 and event.y>35 and event.y<70
   ELECTRICROOM = event.x>810 and event.x<850 and event.y>35 and event.y<70
   l = event.x>840 and event.x<875 and event.y>55 and event.y<250
   M = event.x>840 and event.x<960 and event.y>25 and event.y<55
   N = event.x>840 and event.x<900 and event.y>250 and event.y<280
   O = event.x>900 and event.x<990 and event.y>250 and event.y<570
   P = event.x>875 and event.x<910 and event.y>55 and event.y<100
   Q = event.x>875 and event.x<910 and event.y>100 and event.y<190
   R = event.x>875 and event.x<910 and event.y>190 and event.y<220
   S = event.x>875 and event.x<910 and event.y>220 and event.y<240
   T = event.x>840 and event.x<900 and event.y>275 and event.y<380
   U = event.x>840 and event.x<900 and event.y>380 and event.y<405
   V1 = event.x>840 and event.x<865 and event.y>440 and event.y<570
   V2 = event.x>840 and event.x<900 and event.y>400 and event.y<440
   V3 = event.x>865 and event.x<900 and event.y>440 and event.y<500
   V4 = event.x>865 and event.x<900 and event.y>500 and event.y<520
   cv.delete(ALL)
   cv.create_image((550,350),image=img)
   cv.create_oval(currentx-7,currenty-7,currentx+7,currenty+7,fill = "blue") 
   x1, y1 = ( event.x - 7 ), ( event.y - 7 )  
   x2, y2 = ( event.x + 7 ), ( event.y + 7 )
   d = cv.create_oval( x1, y1, x2, y2, fill = "red" )
   print(event.x,event.y)
   if  mainhall:
      cv.create_line(currentx,currenty,event.x,event.y,fill = "black",width = 5,dash = (10,10))
   elif womensroom:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash = (10,10))
      cv.create_line(330,580,310,620,fill = "black",width = 5,dash = (10,10))
      cv.create_line(310,620,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif mensroom:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash = (10,10))
      cv.create_line(645,580,660,620,fill = "black",width = 5,dash = (10,10))
      cv.create_line(660,620,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif conE:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,580,350,620,fill = "black",width = 5,dash =(10,10))
      cv.create_line(350,620,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif conW:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,580,630,620,fill = "black",width = 5,dash =(10,10))
      cv.create_line(630,620,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif A:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,580,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif B:
      cv.create_line(currentx,currenty,495,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(495,580,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif C:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,580,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif D:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,580,330,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,645,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif D1:
      cv.create_line(currentx,currenty,330,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,580,330,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(330,645,130,670,fill = "black",width = 5,dash =(10,10))
      cv.create_line(130,670,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif E:
      cv.create_line(currentx,currenty,485,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(485,580,485,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(485,645,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif F:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,580,645,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,645,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif F1:
      cv.create_line(currentx,currenty,645,580,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,580,645,645,fill = "black",width = 5,dash =(10,10))
      cv.create_line(645,645,855,670,fill = "black",width = 5,dash =(10,10))
      cv.create_line(855,670,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif G:
      cv.create_line(currentx,currenty,210,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(210,120,130,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(130,100,80,120,fill = "black",width = 5,dash =(10,10))      
      cv.create_line(80,120,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif H:
      cv.create_line(currentx,currenty,210,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(210,120,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif I:
      cv.create_line(currentx,currenty,350,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(350,120,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif J1:
      cv.create_line(currentx,currenty,385,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(385,120,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif J2:
      cv.create_line(currentx,currenty,590,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(590,120,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif K1:
      cv.create_line(currentx,currenty,625,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(625,120,event.x,event.y,fill = "black",width = 5,dash =(10,10))      

   elif K2:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif FHC:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif STAIR4:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,795,70,fill = "black",width = 5,dash =(10,10))      
      cv.create_line(795,70,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif ELECTRICROOM:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,820,70,fill = "black",width = 5,dash =(10,10))      
      cv.create_line(820,70,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif l:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))      
      cv.create_line(850,100,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif M:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,55,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,55,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif N:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,250,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,250,event.x,event.y,fill = "black",width = 5,dash = (10,10))         

   elif O:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,910,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(910,260,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif P:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))   
      cv.create_line(850,100,875,100,fill = "black",width = 5,dash =(10,10))      
      cv.create_line(875,100,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif Q:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))   
      cv.create_line(850,100,875,110,fill = "black",width = 5,dash =(10,10))      
      cv.create_line(875,110,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif R:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))   
      cv.create_line(850,100,875,200,fill = "black",width = 5,dash =(10,10))      
      cv.create_line(875,200,event.x,event.y,fill = "black",width = 5,dash =(10,10))   

   elif S:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,850,100,fill = "black",width = 5,dash =(10,10))   
      cv.create_line(850,100,870,235,fill = "black",width = 5,dash =(10,10))      
      cv.create_line(870,235,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif T:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,250,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,250,860,275,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,275,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif U:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10)) 
      cv.create_line(860,100,860,250,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,250,860,275,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,275,850,380,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,380,event.x,event.y,fill = "black",width = 5,dash = (10,10))

   elif V1:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,835,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,500,850,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,500,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif V2:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,835,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,500,850,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,500,855,440,fill = "black",width = 5,dash =(10,10))
      cv.create_line(855,440,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif V3:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,835,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,500,850,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,500,865,485,fill = "black",width = 5,dash =(10,10))
      cv.create_line(865,485,event.x,event.y,fill = "black",width = 5,dash =(10,10))

   elif V4:
      cv.create_line(currentx,currenty,790,120,fill = "black",width = 5,dash =(10,10))
      cv.create_line(790,120,860,100,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,100,860,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(860,260,835,260,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,260,835,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(835,500,850,500,fill = "black",width = 5,dash =(10,10))
      cv.create_line(850,500,865,510,fill = "black",width = 5,dash =(10,10))
      cv.create_line(865,510,event.x,event.y,fill = "black",width = 5,dash =(10,10))

 


root=Tk()

cv=Canvas(root,bg='white',width=1100,height=2500)  
img=PhotoImage(file='mainhalldining2.png')  
cv.create_image((550,350),image=img)  
cv.pack()  

cv.create_oval(currentx-7,currenty-7,currentx+7,currenty+7,fill = "#146FF8")
cv.bind("<Button-1>",paint)

root.mainloop()  
