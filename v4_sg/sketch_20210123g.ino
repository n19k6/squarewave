/*
 * arduino nano v3 + 3 potentiometer
 * g) 34 + 2 = kurbelwelle
 * 
 *  D12 - yellow - generated squarewave
 *  D11 - red - indicate isr activity
 * 
 */

#define D12 12 // yellow
#define D11 11 // red
#define D10 10 // green - jede umdrehung einmal
#define D9 9 // isr

//int analog_a = 2; // entspricht PIN A2
//int analog_b = 1; // entspricht PIN A1
//int analog_c = 0; // entspricht PIN A0

//int val_a = 0;
//int val_b = 0;
//int val_c = 0;

/*
int last_a = 0;
int last_b = 0;
int last_c = 0;
int register_a = 0;
int register_b = 0;
int register_c = 0;

const boolean invert = true; // implement as macro
*/

volatile boolean buffer_D12;
int val_a;
volatile int val_b;
volatile int val_c;
//unsigned long time;
volatile unsigned long timer0_count = 0;
volatile boolean hack = false;

void setup2() {
  Serial.begin(9600);
  buffer_D12 = false;
  val_a = 0;
  val_b = 0;
  val_c = 0;
  timer0_count = 0;
  hack = false;
  //time = millis();
  //pinMode(D09, OUTPUT);  
  pinMode(D10, OUTPUT);  
  pinMode(D11, OUTPUT);  // indicate isr activity
  pinMode(D12, OUTPUT);  // generated squarewave

  //timer0_count = 0;
  //timer2_count = 0;

  digitalWrite(D9, 0);
  digitalWrite(D10, 0);
  digitalWrite(D11, 0);
  digitalWrite(D12, 0);
  //buffer_D12 = 0;
}

void setup() {
  Serial.begin(9600);
  buffer_D12 = false;
  val_a = 0;
  //time = millis();
  pinMode(D9, OUTPUT);  
  //pinMode(D10, OUTPUT); 
  pinMode(D10, OUTPUT);  // einmal jede umdrehung der kurbelwelle 
  pinMode(D11, OUTPUT);  // indicate isr activity
  pinMode(D12, OUTPUT);  // generated squarewave

  timer0_count = 0;
  //timer2_count = 0;
  digitalWrite(D9, 0);
  digitalWrite(D10, 0);
  digitalWrite(D11, 0);
  digitalWrite(D12, 0);
  //buffer_D12 = 0;
  //buffer_D11 = 0;
  //buffer_D10 = 0;

  // stick with 8-bit Timer 0, other Timers might mess up delay-function
  // Timer 0
  noInterrupts();           // disable all interrupts temporarily
  TCCR0A=(1<<WGM01);    //Set the CTC mode   
  //OCR0A=0xF9; //Value for ORC0A for 16ms
  //OCR0A=0xFF; //Value for 
  //TCCR0B = (1<< CS02) | (0<< CS01) | (1<< CS00); // prescale 256
  //OCR0A=0xE1; //Value for ORC0A for 1ms

  //https://www.exp-tech.de/blog/arduino-tutorial-timer
  //interrupt will be triggered depending on values for OCR0A and OCR0A

  // 100 cpu cycles at 8 Mhz is no prescale and OCR0A = 99, frequency should be 80 kHz ~ 0.0125 ms

  // 255 cpu cycles at 8/256 Mhz, frequency should be (8 Mhz/(256*256))^-1 ~ 8.192 ms
  // w measured is 16.38 ms
  //OCR0A=0xFF; TCCR0B = (1<< CS02) | (0<< CS01) | (1<< CS00); // prescale 256

  // work with prescale 256
  TCCR0B = (1<< CS02) | (0<< CS01) | (1<< CS00); // prescale 
  OCR0A=0x01; // w measured is 0.123 ms
  //OCR0A=0xFF; // w measured is 16.38 ms
  //OCR0A=0x80; // 0x80 = 128 should be 16.38/2 ~ 8.19 ms, measure w: result w=8.25 ms -> yep
  
  TIMSK0|=(1<<OCIE0A);   //Set the interrupt request
  /*
  TCCR2A=(1<<WGM01);    //Set the CTC mode   
  OCR2A=0xFF; //Value for ORC0A
  OCR2A=0x08; //Value for ORC0A
  TIMSK2|=(1<<OCIE0A);   //Set the interrupt request
  TCCR2B = (1<< CS02) | (0<< CS01) | (1<< CS00); // prescale 256
  */
  interrupts();             // activate all interrupts
}

void loop() {
  //if (millis()>1000+time) {
  //time = millis();
  val_a = analogRead(2);
  //val_a = map(val_a,0,1023,255,1);
  // todo: bei 8->2 gibt es aussetzer in 0-3s bei isr signal
  val_a = map(val_a,0,1023,255,8);
  val_b = analogRead(1);
  val_b = map(val_b,0,1023,0,35);
  val_c = analogRead(0);
  val_c = map(val_c,0,1023,0,35);
  OCR0A=val_a;
  //Serial.print(time);
  Serial.print("[");
  Serial.print(val_a);
  Serial.print(",");
  Serial.print(val_b);
  Serial.print(",");
  Serial.print(val_c);
  Serial.print("]");
  Serial.println();
  //attention: using timer0 i.e. TCCR0A, interfers with delay
  //delay(500);
  //}
  // 1 -> f=741Hz
  // 
}


ISR(TIMER0_COMPA_vect)        
{
  //TCNT0 = 0x80;
  digitalWrite(D9, 1);
  //digitalWrite(D10, 1);
  /*
  if ((buffer_D12 && timer0_count > pwm_high) or (!buffer_D12 && timer0_count > pwm_low)) {
    digitalWrite(D12, !buffer_D12);
    buffer_D12=!buffer_D12;
    timer0_count=1;
  }
  timer0_count++;
  */
  //buffer_D12 = !buffer_D12;
  /*
  if (timer0_count == 0) {
    digitalWrite(D10, true);
  } else {
    digitalWrite(D10, false);
  }
  */

  if (timer0_count % 2 == 0 && timer0_count != 68 && timer0_count != 70) {
    digitalWrite(D12, true);
    //digitalWrite(D9, false);
  } else {
    digitalWrite(D12, false);
    //digitalWrite(D9, true);
  }

//  if (timer0_count+val_b % 72 == 0+7 || timer0_count+val_b % 72  == 35+7) {
//  if ((timer0_count+val_b % 72) == 0 || (timer0_count+val_b % 72)  == 35) {
if ((timer0_count == val_b) || (timer0_count == (35+val_b % 72))) {
    digitalWrite(D11, false);
  } else {
    digitalWrite(D11, true);
  }

  //if ((timer0_count+val_c % 72 > 7 && timer0_count+val_c % 72 < 10 && hack) || (timer0_count+val_c % 72 > 35+7 && timer0_count+val_c % 72 < 35+10)) {
  /*
  if ((timer0_count+val_c % 72 > 0 && timer0_count+val_c % 72 < 3 && hack) || (timer0_count+val_c % 72 > 35 && timer0_count+val_c % 72 < 35+3)) {
    digitalWrite(D10, true);
  } else {
    digitalWrite(D10, false);
  }
  */
  /*
  if ((((timer0_count+val_c) % 72 > 0 || (timer0_count+val_c) % 72 < 3) && hack) || ((timer0_count+val_c) % 72 > 35 || (timer0_count+val_c) % 72 < 35+3)) {
    digitalWrite(D10, true);
  } else {
    digitalWrite(D10, false);
  }
  */
if (!hack) {
if ((timer0_count == val_c) || (timer0_count == (1+val_c % 72)) || (timer0_count == (35+val_c % 72)) || (timer0_count == (36+val_c % 72))) {
  digitalWrite(D10, true);
} else {
  digitalWrite(D10, false);
}
} else {
if ((timer0_count == (35+val_c % 72)) || (timer0_count == (36+val_c % 72))) {
  digitalWrite(D10, true);
} else {
  digitalWrite(D10, false);
}  
}
  /*
  int hack2 = (timer0_count-val_c) % 72;
  switch (hack2) {
    case 0:
      digitalWrite(D10, true);
      break;
    case 1:
      digitalWrite(D10, true);
      break;
    case 2:
      digitalWrite(D10, true);
      break;
    case 35:
      digitalWrite(D10, true);
      break;
    case 36:
      digitalWrite(D10, true);
      break;
    case 37:
      digitalWrite(D10, true);
      break;
    default:
      digitalWrite(D10, false);
      break;   
  }
  */
  
  timer0_count++;
  if (timer0_count>71) {
    timer0_count=0;
    hack = !hack;
  }
  digitalWrite(D9, 0);
  //digitalWrite(D10, 0);
}