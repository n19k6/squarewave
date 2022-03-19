/*
 * arduino nano v3 + 3 potentiometer
 * 
 * sketch_20210208a
 * 
 * aim: generate lambda-sonde signal -> check timer values against osciloscope
 * 
 * generate two squarewave signals using timer1 (16-bit) and timer2 (8-bit)
 * check delay function
 * 
 * https://www.robotshop.com/community/forum/t/arduino-101-timers-and-interrupts/13072
 * https://www.teachmemicro.com/arduino-timer-interrupt-tutorial/
 * https://www.heise.de/developer/artikel/Timer-Counter-und-Interrupts-3273309.html
 * 
 */

#define D7 7 // timer0 isr
#define D8 8 // timer0 squarewave
#define D9 9 // timer1 isr
#define D10 10 // timer1 squarewave
#define D11 11 // loop


//volatile boolean buffer_D12;
//volatile boolean buffer_D8;

unsigned int val_a;
unsigned int val_b;
unsigned int val_c;

unsigned long loops;
unsigned long changes;

unsigned int last_a;
unsigned int last_b;
unsigned int last_c;

float tar_a;
float tar_b;
float tar_c;

//volatile unsigned long timer0_count = 0;
//volatile boolean hack = false;
//volatile unsigned long timer2_count = 0;

void setup() {
  Serial.begin(9600);
  //buffer_D12 = false;
  //buffer_D8 = false;
  
  val_a = 0;
  val_b = 0;
  val_c = 0;

  loops = 0;
  changes = 0;
  
  tar_a = 0;
  tar_b = 0;
  tar_c = 0;
  
  last_a = 0;
  last_b = 0;
  last_c = 0;
  
  pinMode(D7, OUTPUT);
  pinMode(D8, OUTPUT);
  pinMode(D9, OUTPUT);  
  pinMode(D10, OUTPUT); 
  pinMode(D11, OUTPUT);

  //timer0_count = 0;
  //timer2_count = 0;
  digitalWrite(D7, 0);
  digitalWrite(D8, 0);
  digitalWrite(D9, 0);
  digitalWrite(D10, 0);
  digitalWrite(D11, 0);

  noInterrupts();           // disable all interrupts temporarily
  TCCR1A = 0;
  TCCR1B = 0;

  TCNT1 = 34286;            // Timer nach obiger Rechnung vorbelegen
  // https://www.heise.de/developer/artikel/Timer-Counter-und-Interrupts-3273309.html -> Konfiguration des Prescaler
  TCCR1B |= (1 << CS12);    // 256 als Prescale-Wert spezifizieren
  // ticks with 16us
  TIMSK1 |= (1 << TOIE1);   // Timer Overflow Interrupt aktivieren
   

  TCCR2A = 0;
  TCCR2B = 0;

  TCNT2 = 126;            // Timer nach obiger Rechnung vorbelegen
  // https://wolles-elektronikkiste.de/en/timer-and-pwm-part-1-8-bit-timer0-2 -> Setting the prescaler with the Clock Select bits for Timer2
  //TCCR2B |= (1 << CS22); TCCR2B |= (1 << CS21);    // 256 als Prescale-Wert spezifizieren
  // ticks with 16us
  TCCR2B |= (1 << CS22); TCCR2B |= (1 << CS21); TCCR2B |= (1 << CS20);   // 1024 als Prescale-Wert spezifizieren
  // ticks with 64us
  TIMSK2 |= (1 << TOIE2);   // Timer Overflow Interrupt aktivieren  
  
  interrupts();             // activate all interrupts
}


ISR(TIMER1_OVF_vect)          // timer1 overflow interrupt service routine
{
  TCNT1 = 34286; 
  TCNT1 = 0; // expected 1048.576 ms
  digitalWrite(D9, 1);
  digitalWrite(D10, digitalRead(D10) ^ 1);
  digitalWrite(D9, 0);
}

ISR(TIMER2_OVF_vect)          // timer2 overflow interrupt service routine
{
  TCNT2 = 0; // expected 16.384 ms (2**8*64/1000 = 16.384)
  digitalWrite(D7, 1);
  digitalWrite(D8, digitalRead(D8) ^ 1);
  digitalWrite(D7, 0);
}

void loop() {
  //Serial.println("<-- loop");
  digitalWrite(D11, 1);
  loops++;
  val_a = analogRead(2);
  val_b = analogRead(1);
  val_c = analogRead(0);

  if (abs(val_a-last_a)+abs(val_b-last_b)+abs(val_c-last_c) > 3) {
    changes++;
    loops = 0;
    last_a = val_a;
    last_b = val_b;
    last_c = val_c;
    val_a = map(val_a,0,1023,1,255);
    //OCR1A = val_a;
    val_b = map(val_b,0,1023,0,127);
    // 0 = off
    // 126 = 10 Hz
    // 127 = 0
    if (val_b != 127) {
      tar_b = 10.0/126*val_b;
    } else {
      tar_b = 999;
    }
    val_c = map(val_c,0,1023,0,20);
    // 0 = off
    // 1 = 5% duty
    // 20 = 100% duty
    tar_c = 100.0/20*val_c;

    Serial.println();
    Serial.print("[");
    Serial.print(changes);
    Serial.print("] ");
    Serial.print("[");
    Serial.print(val_a);
    Serial.print("->");
    Serial.print(OCR1A);
    Serial.print(",");
    Serial.print(val_b);
    Serial.print("->");
    Serial.print(tar_b);
    Serial.print(",");
    Serial.print(val_c);
    Serial.print("->");
    Serial.print(tar_c);
    Serial.print("]");
    //Serial.println();
  }
  digitalWrite(D11, 0);
  //Serial.println("loop -->");
  delay(250);
  if (loops == 4) {
    Serial.print("[");
  }
  if (loops == 20) {
    Serial.print("]");
  }
  if (loops > 4 && loops < 20) {
    Serial.print("*");
  }
  
  //digitalWrite(D11, 1);
  //delay(100);
  //digitalWrite(D11, 0);
}
