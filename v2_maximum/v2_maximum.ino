#define D12 12 // pwm signal
#define D11 11 // used to output signal
#define D10 10 // used to output signal
#define D09 9 // used to output signal

//https://www.heise.de/developer/artikel/ATtiny-Winzlinge-ganz-gross-3329007.html
//http://ww1.microchip.com/downloads/en/Appnotes/Atmel-2505-Setup-and-Use-of-AVR-Timers_ApplicationNote_AVR130.pdf
//https://www.exp-tech.de/blog/arduino-tutorial-timer

/*
 * to compile for arduino clone "Nano V3.0 CH340" set:
 * board = Arduino Nano
 * processor = ATmega328P (Old Bootloader)
 * 
 * version of arduino IDE is 1.8.9
 * 
 * this example uses two 8-bit timers to generate independent wave signals
 */

//parameter for pwm signal
//change TCNT0 in interrupt routine or OCR0A for different frequency
unsigned int pwm_low = 5;
unsigned int pwm_high = 2;

//parameter for wheel signal
//change TCNT1 in interrupt routine or OCR1A for different frequency

volatile boolean buffer_D10;
volatile boolean buffer_D11;
volatile boolean buffer_D12;

volatile unsigned long timer0_count;
volatile unsigned long timer2_count;


void setup() {
  pinMode(D09, OUTPUT);  
  pinMode(D10, OUTPUT);  
  pinMode(D11, OUTPUT);  // generated signal
  pinMode(D12, OUTPUT);  // 

  timer0_count = 0;
  timer2_count = 0;

  digitalWrite(D10, 0);
  digitalWrite(D11, 0);
  digitalWrite(D12, 0);
  buffer_D12 = 0;
  buffer_D11 = 0;
  buffer_D10 = 0;
  
  // Timer 0
  noInterrupts();           // disable all interrupts temporarily
  TCCR0A=(1<<WGM01);    //Set the CTC mode   
  OCR0A=0xF9; //Value for ORC0A for 16ms
  OCR0A=0xFF; //Value for ORC0A
  //OCR0A=0xE1; //Value for ORC0A for 1ms
  TIMSK0|=(1<<OCIE0A);   //Set the interrupt request
  TCCR0B = (1<< CS02) | (0<< CS01) | (1<< CS00); // prescale 256

  TCCR2A=(1<<WGM01);    //Set the CTC mode   
  OCR2A=0xFF; //Value for ORC0A
  OCR2A=0x08; //Value for ORC0A
  TIMSK2|=(1<<OCIE0A);   //Set the interrupt request
  TCCR2B = (1<< CS02) | (0<< CS01) | (1<< CS00); // prescale 256
  interrupts();             // activate all interrupts
}


ISR(TIMER0_COMPA_vect)        
{
  //TCNT0 = 0x80;
  //digitalWrite(D11, 1);
  if ((buffer_D12 && timer0_count > pwm_high) or (!buffer_D12 && timer0_count > pwm_low)) {
    digitalWrite(D12, !buffer_D12);
    buffer_D12=!buffer_D12;
    timer0_count=1;
  }
  timer0_count++;
  //digitalWrite(D11, 0);
}



ISR(TIMER2_COMPA_vect)        
{
  //TCNT0 = 0x80;
  digitalWrite(D09, 1);
  if (buffer_D11) {
    digitalWrite(D11, !buffer_D11);
    buffer_D11=!buffer_D11;  
  } else if (timer2_count % 4 == 1 && timer2_count != 5 && timer2_count != 9 && timer2_count != 5+36*4 && timer2_count != 9+36*4) {
    digitalWrite(D11, !buffer_D11);
    buffer_D11=!buffer_D11;  
  }
  if (buffer_D10) {
    digitalWrite(D10, !buffer_D10);
    buffer_D10=!buffer_D10;  
  } else if (timer2_count == 18*4 || timer2_count == 36*4 || timer2_count == 54*4) {
    digitalWrite(D10, !buffer_D10);
    buffer_D10=!buffer_D10;  
  }
  timer2_count++;
  if (timer2_count>288) {
    timer2_count=0;
  }
  digitalWrite(D09, 0);
}


void loop() {
}
