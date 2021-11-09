#include<Servo.h>

Servo x, y;
int width = 640, height = 480;  
int xpos = 90, ypos = 90; 
int laserpin = 11; 
void setup() {
  
  pinMode (laserpin, OUTPUT);
  Serial.begin(9600);
  x.attach(9);
  y.attach(10);
  // Serial.print(width);
  //Serial.print("\t");
  //Serial.println(height);
  x.write(xpos);
  y.write(ypos);
}
const int angle = 2;   

void loop() {
  if (Serial.available() > 0)
  {
    int xaPos=xpos;
    int yaPos=ypos;
    int x_mid, y_mid, t_gelen;
    if (Serial.read() == 'X')
    {
      x_mid = Serial.parseInt();  
      if (Serial.read() == 'Y')
        y_mid = Serial.parseInt(); 
        if (Serial.read() == 'T')
          t_gelen = Serial.parseInt(); 
    }
    
//    if (x_mid < width / 2 )// + 30)
//      xpos += angle;
//    if (x_mid > width / 2 )// - 30)
//      xpos -= angle;
//    if (y_mid < height / 2 )// + 30)
//      ypos += angle;
//    if (y_mid > height / 2 )// - 30)
//      ypos -= angle;



    if (x_mid < width / 2  + 40)
      ypos -= angle;
    if (x_mid > width / 2  - 40)
      ypos += angle;
    if (y_mid < height / 2  + 40)
      xpos += angle;
    if (y_mid > height / 2  - 40)
      xpos -= angle;


    //Servo limiti
    if (xpos >= 180)
      xpos = 180;
    else if (xpos <= 0)
      xpos = 0;
    if (ypos >= 180)
      ypos = 180;
    else if (ypos <= 0)
      ypos = 0;
    
//    while((xaPos!=xpos)&&(yaPos!=ypos)){
//      if (xaPos>xpos){
//        xaPos=xaPos-1;
//        x.write(xaPos);              
//      }
//      if (xaPos<xpos){
//        xaPos=xaPos+1;
//        x.write(xaPos);
//      }
//      if (yaPos>ypos){
//        yaPos=yaPos-1;
//        y.write(yaPos);              
//      }
//      if (yaPos<ypos){
//        yaPos=yaPos+1;
//        y.write(yaPos);
//      }
//      delay(100);      
//    }


    if (t_gelen==1){
      digitalWrite(laserpin, HIGH);
    }
    else {
      digitalWrite(laserpin, LOW);
    }
    
    x.write(xpos);    
    y.write(ypos);
    delay(20);
    
  }
}
