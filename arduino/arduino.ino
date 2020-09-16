#include <TinyGPS.h>
#include "WiFi.h"
#include <SoftwareSerial.h>
#include "Keypad.h"

#define PHONE_Lenght 10
#define WIFI_NETWORK "DEEP_PI"
#define WIFI_PASSWORD "12345678"
int CONNECT_FLAG = 0;
char Data[PHONE_Lenght]; 
char phone[13]="+962000000000"; 
char customKey;
int incomingByte = 0;
byte data_count = 0;
float Latitude, Longitude;

TinyGPS gps;
SoftwareSerial serial_gps(14, 15);//serial3
SoftwareSerial serial_gsm(16, 17);//serial2


const byte ROWS = 4;
const byte COLS = 3;
char keys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};
byte rowPins[ROWS] =  {A6,A5,A4,A3}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {A2,A1,A0}; //connect to the column pinouts of the keypad
Keypad customKeypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS); //initialize an instance of class NewKeypad


////////////////////////////
void connet2wifi()
{
  //Connect ESP32 to WiFi 
  Serial.print("Connecting");
  WiFi.begin(WIFI_NETWORK,WIFI_PASSWORD);
  unsigned long start_time=millis();

  while(WiFi.status()!= WL_CONNECTED)
   { 
    //Serial.print(".");
    delay(100);
  }

  if(WiFi.status()!= WL_CONNECTED)
  {
    //conection failed
    CONNECT_FLAG = 0;
    }
  else
    {
      //conection success
      CONNECT_FLAG = 1;
    }
 
  }
/////////////////////////////
void reset_command()
{
 CONNECT_FLAG = 0;
 phone[13]="+962000000000"; 
 incomingByte = 0;
 data_count = 0;

  
  }


void setup() {
  serial_gsm.begin(9600);
  serial_gps.begin(9600);
  Serial.begin(9600);
  connet2wifi();
}



void loop() {
//update phone number 
    customKey = customKeypad.getKey();///enter new phone number 
    if (customKey == '#')
    {  data_count=0;    
         while (data_count != 0)
             { 
                  customKey = customKeypad.getKey();
                   if (customKey) 
                   {   
                       Data[data_count] =customKey ; 
                       data_count++;
                   }
              
              }
              
    }
  /////////////////////
  //check rasspberry msg    
  if (Serial.available() > 0 & CONNECT_FLAG == 1) {
    
        // read the incoming byte:
        incomingByte = Serial.parseInt();
        if(incomingByte==10)
        {
            while (serial_gps.available())
               {
                int c = serial_gps.read();
                 if (gps.encode(c))
                 {
                    gps.f_get_position(&Latitude, &Longitude);
                 }
              }
   
               serial_gsm.print("\r");
               delay(400);
               serial_gsm.print("AT+CMGF=1\r");
               delay(300);
               int t=0;
               while (t<9){
                phone[t+4]=Data[t+1];
                }
               serial_gsm.print("AT+CMGS=\"");
               serial_gsm.println(phone);
               serial_gsm.println("\"");

               
               delay(400);
               serial_gsm.print("https://www.google.com/maps/?q=");
               serial_gsm.print(Latitude, 6);
               serial_gsm.print(",");
               serial_gsm.print(Longitude, 6);
               delay(1000);
               serial_gsm.write(0x1A);
               delay(1200); 
               
               customKey = customKeypad.getKey();///enter new phone number 
               if (customKey == '*')
                 {
                  reset_command();
                  }
          
        }  
     }    
 else
    {
    connet2wifi();
    }

}
