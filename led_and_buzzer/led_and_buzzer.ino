int led = 7;                                    // LED connected to pin 13
int sound = 8;                                // piezo buzzer connected to pin 8

void setup()
{
   pinMode(led, OUTPUT);               // sets the LED as output
   pinMode(sound, OUTPUT);  
   Serial.begin(9600);
     //Serial.println("Looping");
       // sets the buzzer alarm as output
}

void loop()                                         // run the program continuously
{
   digitalWrite(led, LOW); 
   char command = Serial.read();
   Serial.println(command);
   if(command == '1')
   {
     digitalWrite(led, HIGH);   
     //delay(1000);  
    }    
   
   else if(command == '2')
   {
    digitalWrite(led, LOW);          
    tone(sound, 1000, 250);              // play a tone with 1000 Hz for 250 ms
    delay(1000);                                 
   }              
                                   
}