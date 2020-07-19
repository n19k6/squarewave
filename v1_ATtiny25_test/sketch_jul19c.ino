
int analogPin = PB3; 
int val = 0;

volatile boolean buffer_PB0 = 0;
volatile unsigned long timer1_count = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(PB0, OUTPUT);
  pinMode(PB1, OUTPUT);

  // Timer 1
  noInterrupts();           // disable all interrupts temporarily
  TCCR1 = 0;
  TCCR1 |= (1 << CTC1);
  //TCCR1 |= (1 << CS10) | (1 << CS11) | (1 << CS13);
  TCCR1 |= (1 << CS10) | (1 << CS13); //prescale 256
  TCNT1 = 0;
  OCR1C = 1;
  TIMSK |= (1 << OCIE1A);

  // Mehr Infos: https://arduino-projekte.webnode.at/registerprogrammierung/timer-interrupt/attiny/
  /*
  TCCR0A=(1<<WGM01);    //Set the CTC mode   
  OCR0A=0xF9; //Value for ORC0A for 16ms
  OCR0A=0xFF; //Value for ORC0A
  //OCR0A=0xE1; //Value for ORC0A for 1ms
  TIMSK0|=(1<<OCIE0A);   //Set the interrupt request
  TCCR0B = (1<< CS02) | (0<< CS01) | (1<< CS00); // prescale 256
  */

  //TCCR2A=(1<<WGM01);    //Set the CTC mode   
  //OCR2A=0xFF; //Value for ORC0A
  //OCR2A=0x08; //Value for ORC0A
  //TIMSK2|=(1<<OCIE0A);   //Set the interrupt request
  //TCCR2B = (1<< CS02) | (0<< CS01) | (1<< CS00); // prescale 256
  interrupts();             // activate all interrupts
}

void set_out(int i, int j) {
  digitalWrite(PB0, i);
  digitalWrite(PB1, j);
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  digitalWrite(PB0, HIGH);
  //digitalWrite(PB1, HIGH);
  delay(10);
  digitalWrite(PB0, LOW);
  digitalWrite(PB1, LOW);
  delay(10);
  digitalWrite(PB0, HIGH);
  digitalWrite(PB1, HIGH);
  delay(10);
  digitalWrite(PB0, HIGH);
  digitalWrite(PB1, LOW);
  delay(10);
  */
  /*
  set_out(LOW, LOW);
  delay(10);
  set_out(HIGH, HIGH);
  delay(10);
  set_out(LOW, LOW);
  val = analogRead(analogPin);
  val = val / 4;
  delay(10);
  set_out(HIGH, HIGH);
  delay(val);
  //set_out(LOW, LOW);
  //delay(10);
  */
  val = analogRead(analogPin);
  val = val / 1017 * 255;
  if (val>255) {
    val=255;
  }
  if (val<1) {
    val=1;
  }
  OCR1C = val;
}

ISR(TIMER1_COMPA_vect)        
{
  //TCNT0 = 0x80;
  digitalWrite(PB1, 1);
  if (buffer_PB0) {
    digitalWrite(PB0, !buffer_PB0);
    buffer_PB0=!buffer_PB0;  
  } else if (timer1_count % 4 == 1 && timer1_count != 5 && timer1_count != 9 && timer1_count != 5+36*4 && timer1_count != 9+36*4) {
    digitalWrite(PB0, !buffer_PB0);
    buffer_PB0=!buffer_PB0;   
  }
  /*
  if (buffer_PB0) {
    digitalWrite(PB0, !buffer_PB0);
    buffer_PB0=!buffer_PB0;  
  } else if (timer1_count == 18*4 || timer1_count == 36*4 || timer1_count == 54*4) {
    digitalWrite(PB0, !buffer_PB0);
    buffer_PB0=!buffer_PB0;  
  }
  */
  timer1_count++;
  if (timer1_count>288) {
    timer1_count=0;
  }
  digitalWrite(PB1, 0);
}
