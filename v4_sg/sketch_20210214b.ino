/*
 * arduino nano v3 + 3 potentiometer
 * 
 * sketch_20210214b
 * 
 * aim: max kurbelwelle ~ 430 Hz ~ 25000 U/min (aber interrupt ist knapp, aber kurbelwelle ist 50-50 nicht 25-75)
 * 
 * generate two squarewave signals using timer1 (16-bit) and timer2 (8-bit)
 * check delay function
 * 
 * https://www.robotshop.com/community/forum/t/arduino-101-timers-and-interrupts/13072
 * https://www.teachmemicro.com/arduino-timer-interrupt-tutorial/
 * https://www.heise.de/developer/artikel/Timer-Counter-und-Interrupts-3273309.html
 * 
 * todos:
 * - set default values if no poties are present
 * - change settings only after period end
 * 
 */

//D12-D2 are available

#define D7 7 // timer2 isr
#define D8 8 // timer2 squarewave - lambda-sonde
#define D9 9 // timer1 isr
#define D10 10 // timer1 squarewave - kurbelwelle
#define D11 11 // loop
#define D11 11 // timer1 squarewave - nockenwelle
#define D12 12 // timer1 squarewave - zuendsignal


//volatile boolean buffer_D12;
//volatile boolean buffer_D8;

const unsigned int stability = 3;

//precalculated values for lambda-signal

//[30-10] = [177, 001->  10.016   0.016]
//3,88,87,38,38,130,171,69,38,38,113,38,11,38,184,38,69,11,38,184,99,165,25,60,85,110,131,149,164,177,
//31,36,31,20,18,25,31,12,9,8,10,6,4,4,11,3,3,2,2,5,2,3,1,1,1,1,1,1,1,1,
//   16.13,   10.69,   10.75,   13.89,   13.89,    8.00,    5.38,   11.90,   13.89,   13.89,    9.09,   13.89,   15.62,   13.89,    4.54,   13.89,   11.90,   15.62,   13.89,    4.54,    9.98,    5.76,   14.72,   12.48,   10.88,    9.28,    7.94,    6.78,    5.82,    4.99,
//    0.10,    0.13,    0.15,    0.18,    0.20,    0.25,    0.30,    0.35,    0.40,    0.45,    0.55,    0.60,    0.80,    0.90,    1.00,    1.20,    1.40,    1.60,    1.80,    2.20,    2.50,    2.89,    3.40,    4.01,    4.60,    5.39,    6.30,    7.37,    8.59,   10.02,

const byte lambda_start_timer[32] = {0,3,88,87,38,38,130,171,69,38,38,113,38,11,38,184,38,69,11,38,184,99,165,25,60,85,110,131,149,164,177};
const byte lambda_multiplier[32] = {0,31,36,31,20,18,25,31,12,9,8,10,6,4,4,11,3,3,2,2,5,2,3,1,1,1,1,1,1,1,1};
const float lambda_tick[32] = {0,16.13,   10.69,   10.75,   13.89,   13.89,    8.00,    5.38,   11.90,   13.89,   13.89,    9.09,   13.89,   15.62,   13.89,    4.54,   13.89,   11.90,   15.62,   13.89,    4.54,    9.98,    5.76,   14.72,   12.48,   10.88,    9.28,    7.94,    6.78,    5.82,    4.99};
const float lambda_predication[32] = {0,0.10,    0.13,    0.15,    0.18,    0.20,    0.25,    0.30,    0.35,    0.40,    0.45,    0.55,    0.60,    0.80,    0.90,    1.00,    1.20,    1.40,    1.60,    1.80,    2.20,    2.50,    2.89,    3.40,    4.01,    4.60,    5.39,    6.30,    7.37,    8.59,   10.02};

const boolean kurbelwelle[144] = {1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0};
const boolean zuendsignal[144] = {1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
const boolean nockenwelle[144] = {0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

// raw poti values
unsigned int val_a;
unsigned int val_b;
unsigned int val_c;

unsigned long loops;
unsigned long changes;

// raw poti values
unsigned int last_a;
unsigned int last_b;
unsigned int last_c;

// normalized poti values
unsigned int norm_a;
unsigned int norm_b;
unsigned int norm_c;

// derived values
float width_a;


// signal parameters


byte isr2_tcnt2;
byte isr2_multiplier;
boolean isr2_out_of_range;
boolean isr2_value;
//volatile ????
volatile unsigned int isr2_cnt;
unsigned int isr2_cnt_on;

unsigned int isr1_tcnt1;
unsigned int isr1_cnt;

//volatile unsigned long timer0_count = 0;
//volatile boolean hack = false;
//volatile unsigned long timer2_count = 0; //0-4294967295 (2^32 - 1)
//volatile byte timer2_byte = 0;
// hack 3
//volatile unsigned int timer2_byte = 0;
//byte lambda_dc = 0;

void setup() {
  Serial.begin(9600);
  //buffer_D12 = false;
  //buffer_D8 = false;
  
  val_a = 0;
  val_b = 0;
  val_c = 0;

  loops = 0;
  changes = 0;
  
  last_a = 0;
  last_b = 0;
  last_c = 0;

  isr1_tcnt1 = 0;
  isr1_cnt = 10;

  isr2_tcnt2 = 0;
  isr2_multiplier = 1;
  isr2_out_of_range = false;
  isr2_value = false;
  isr2_cnt = 10;
  isr2_cnt_on = 5;
  
  pinMode(D7, OUTPUT);
  pinMode(D8, OUTPUT);
  pinMode(D9, OUTPUT);  
  pinMode(D10, OUTPUT); 
  pinMode(D11, OUTPUT);
  pinMode(D12, OUTPUT);

  //timer0_count = 0;
  //timer2_count = 0;
  digitalWrite(D7, 0);
  digitalWrite(D8, 0);
  digitalWrite(D9, 0);
  digitalWrite(D10, 0);
  digitalWrite(D11, 0);
  digitalWrite(D12, 0);

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
  //TCNT1 = 34286; 
  //TCNT1 = 0; // expected 1048.576 ms
  //TCNT1 = 0; // expected 1048.576 ms
  TCNT1 = 65536-16384; // expected 262.144 ms 
  TCNT1 = 65536-1024; // expected 16.384 ms
  TCNT1 = 65536-32; // expected 0.512 ms
  TCNT1 = 65536-4; // expected 0.064 ms
  TCNT1 = 65536-2; // expected 0.032 ms
  digitalWrite(D9, 1);
  digitalWrite(D10, kurbelwelle[isr1_cnt]);
  digitalWrite(D11, nockenwelle[isr1_cnt]);
  digitalWrite(D12, zuendsignal[isr1_cnt]);
  //digitalWrite(D12, digitalRead(D12) ^ 1);
  isr1_cnt++;
  if (isr1_cnt >= 144) {
    isr1_cnt = 0;
  }
  digitalWrite(D9, 0);
}

ISR(TIMER2_OVF_vect)          // timer2 overflow interrupt service routine
{
  TCNT2 = 0; // expected 16.384 ms ((2**8*64/1000 = 16.384)
  digitalWrite(D7, 1);
  //digitalWrite(D8, 0);
  if (not isr2_out_of_range) {
    TCNT2 = isr2_tcnt2;
    if (isr2_cnt < isr2_cnt_on) {
      digitalWrite(D8, 1);
    } else {
      digitalWrite(D8, 0);      
    }
    //sdfsdf
  } else {
    digitalWrite(D8, isr2_value);
  }
  //digitalWrite(D8, digitalRead(D8) ^ 1);
  isr2_cnt++;
  if (isr2_cnt >= 20*isr2_multiplier) {
    isr2_cnt = 0;
  }
  digitalWrite(D7, 0);
  //digitalWrite(D8, 1);
}

void loop() {
  //Serial.println("<-- loop");
  //digitalWrite(D11, 1);
  loops++;
  val_a = analogRead(2);
  val_b = analogRead(1);
  val_c = analogRead(0);

  if (abs(val_a-last_a)+abs(val_b-last_b)+abs(val_c-last_c) > stability) {
    
    changes++;
    
    loops = 0;
    last_a = val_a;
    last_b = val_b;
    last_c = val_c;
    
    norm_a = map(val_a,0,1023,1,255);
    //OCR1A = val_a;
    norm_b = map(val_b,0,1023,0,31);
    // 0 = off
    // 30 = 10 Hz
    // 31 = on
    //tar_b = 10.0/62*val_b;
    //tar_b = byte(5000.0/256*63/val_b);
    //tar_b2 = 5000.0/256/tar_b;
    norm_c = map(val_c,0,1023,0,20);
    // 0 = off
    // 1 = 5% duty
    // 20 = 100% duty
    //tar_c = 100.0/20*val_c;
    //lambda_dc = val_c;
    Serial.println();
    Serial.print("[");
    Serial.print(changes);
    Serial.print("] ");
    Serial.print("[");
    Serial.print(norm_a);
    Serial.print("->");
    Serial.print("1");
    Serial.print(", ");
    Serial.print(norm_b);
    Serial.print("->");
    switch (norm_b) {
      case 0:
        Serial.print("off");
        //isr2_tcnt2 = 0;
        //isr2_cnt = 0;
        isr2_out_of_range = true;
        isr2_value = false;
        break;
      case 31:
        Serial.print("on");
        isr2_out_of_range = true;
        isr2_value = true;
        break;
      default:
        isr2_out_of_range = false;
        isr2_tcnt2 = lambda_start_timer[norm_b];
        Serial.print(isr2_tcnt2);
        Serial.print("->");
        isr2_multiplier = lambda_multiplier[norm_b];
        Serial.print(isr2_multiplier);
        Serial.print("->");
        Serial.print(lambda_tick[norm_b]);
        Serial.print("->");
        Serial.print(lambda_predication[norm_b]);
        //Serial.print("->");
        isr2_cnt = 0;//20*isr2_multiplier;
        isr2_cnt_on = norm_c*isr2_multiplier;      
    }
    Serial.print(", ");
    Serial.print(norm_c);
    Serial.print("->");
    switch (norm_c) {
      case 0:
        Serial.print("off");
        //isr2_tcnt2 = 0;
        //isr2_cnt = 0;
        isr2_out_of_range = true;
        isr2_value = false;
        break;
      case 20:
        Serial.print("on");
        isr2_out_of_range = true;
        isr2_value = true;
        break;
      default:
        Serial.print(norm_c*5);
        Serial.print("%");
        isr2_cnt_on = norm_c*isr2_multiplier;      
    }
    Serial.print("]");
    //Serial.println();
  }
  //digitalWrite(D11, 0);
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
