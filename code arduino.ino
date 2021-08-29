#include <FastLED.h>
#include <SPI.h>
#include <MFRC522.h>


//led strip
#define LED_PIN     7
#define NUM_LEDS    18
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

#define UPDATES_PER_SECOND 100


// rfid
#define SS_PIN 10
#define RST_PIN 9
 
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

MFRC522::MIFARE_Key key; 

// Init array that will store new NUID 
//byte nuidPICC[4];


int status = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 


//  setup led strip
  delay( 3000 ); // power-up safety delay
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness(  BRIGHTNESS );

//  setup rfid 
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522 

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

}

void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available()) {         
    String line = Serial.readString();
   if (line == "green"){
      leds[(status*3)+3] = CHSV( HUE_GREEN, 255, 255);
      leds[(status*3)+4] = CHSV( HUE_GREEN, 255, 255);
      leds[(status*3)+5] = CHSV( HUE_GREEN, 255, 255);
    
      FastLED.show();
      FastLED.delay(1000 / UPDATES_PER_SECOND);
      status = status + 1;
    } 
    else if (line == "red"){
      leds[(status*3)+3] = CHSV( HUE_RED, 255, 255);
      leds[(status*3)+4] = CHSV( HUE_RED, 255, 255);
      leds[(status*3)+5] = CHSV( HUE_RED, 255, 255);
    
      FastLED.show();
      FastLED.delay(1000 / UPDATES_PER_SECOND);
      status = status + 1;
    } 
    else if (line == "yellow"){
      leds[(status*3)+3] = CHSV( HUE_YELLOW, 255, 255);
      leds[(status*3)+4] = CHSV( HUE_YELLOW, 255, 255);
      leds[(status*3)+5] = CHSV( HUE_YELLOW, 255, 255);
    
      FastLED.show();
      FastLED.delay(1000 / UPDATES_PER_SECOND);
      status = status + 1;
    } 
    else if (line == "orange"){
      leds[(status*3)+3] = CHSV( HUE_ORANGE, 255, 255);
      leds[(status*3)+4] = CHSV( HUE_ORANGE, 255, 255);
      leds[(status*3)+5] = CHSV( HUE_ORANGE, 255, 255);
    
      FastLED.show();
      FastLED.delay(1000 / UPDATES_PER_SECOND);
      status = status + 1;
    } 
    else{
      leds[(status*3)+3] = CRGB::Gray;
      leds[(status*3)+4] = CRGB::Gray;
      leds[(status*3)+5] = CRGB::Gray;
      
      FastLED.show();
      FastLED.delay(1000 / UPDATES_PER_SECOND);
      status = status + 1;
    }
    if (status == 5){
      status = 0;
    }
  }

    // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;
  
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
   
//  Serial.println(F("The NUID tag is:"));
//  Serial.print(F("In hex: "));
  printHex(rfid.uid.uidByte, rfid.uid.size);
  Serial.println();
  
  // Halt PICC
  rfid.PICC_HaltA();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
    
    
}


/**
 * Helper routine to dump a byte array as hex values to Serial. 
 */
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}
