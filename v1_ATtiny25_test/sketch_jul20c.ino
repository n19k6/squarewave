
int analogPin = PB3; 
int val = 1;

volatile boolean buffer_PB0 = 0;
volatile unsigned long timer1_count = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(PB0, OUTPUT);
  pinMode(PB1, OUTPUT);
  digitalWrite(PB1, LOW);
  // Timer 1
  noInterrupts();           // disable all interrupts temporarily
  TCCR1 = 0;
  TCCR1 |= (1 << CTC1);
  //TCCR1 |= (1 << CS10) | (1 << CS11) | (1 << CS13);
  //TCCR1 |= (1 << CS10) | (1 << CS13); //prescale 256
  TCCR1 |= (1 << CS11) | (1 << CS12); //prescale 32
  TCNT1 = 0;
  OCR1C = 255;
  TIMSK |= (1 << OCIE1A);
  interrupts();
  // Mehr Infos: https://arduino-projekte.webnode.at/registerprogrammierung/timer-interrupt/attiny/
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
  timer1_count++;
  if (timer1_count>288) {
    timer1_count=0;
  }
  digitalWrite(PB1, 0);  
}

void loop() {

}
