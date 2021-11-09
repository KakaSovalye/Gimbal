#include<Servo.h>
#include<math.h>

Servo x, y;
int xpos = 90, ypos = 90; 
int laserpin = 11; 
void setup() {

  pinMode (laserpin, OUTPUT);
  Serial.begin(9600);
  y.attach(9);
  x.attach(10);
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
    int x_gelen, y_gelen, t_gelen;
    if (Serial.read() == 'X')
    {
      x_gelen = Serial.parseInt();  
      if (Serial.read() == 'Y')
        y_gelen = Serial.parseInt(); 
        if (Serial.read() == 'T')
          t_gelen = Serial.parseInt(); 
        
    }
    int miktarX=abs(x_gelen);
    int miktarY = abs(y_gelen);
    if (x_gelen < 0)
      xpos -= angle;    
    if (x_gelen > 0)
      xpos += angle;    
    if (y_gelen < 0)
      ypos += angle;
    if (y_gelen > 0)
      ypos -= angle;


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
