#define D11 11 // used to output signal
#define D12 12 // used to output interrupt handler processing time

/*
 * to compile for arduino clone "Nano V3.0 CH340" set:
 * board = Arduino Nano
 * processor = ATmega328P (Old Bootloader)
 * 
 * version of arduino IDE is 1.8.9
 * 
 * calculations: 
 * 
 * minimum interrupt frequency is 244.14 Hz (16 Mhz, 2**16)
 * 
 * maximum frequency is restricted due to cycle consumption in handler routine 
 * 
 * if you look with a oscilloscope at signal D12 your realize that the interupt
 * service routinie consumes at least 10 us, i.e. 160 cpu cycles
 * 
 * so we set OCR1A to 320 and check what happens
 * signal frequency is 21.91 kHz (period 45.64 us)
 * interrupt frequency is 43.72 kHz (period 22.87 us)
 * 
 * wheel frequency is 21.91/64 kHz = 342 Hz (~ 20000 rpm)
 * 
 * now we want a wheel frequency of 1000 rpm (~ 16.667 Hz).
 * i.e. signal frequency is 16.667 Hz * 64 ~ 1066.67 Hz.
 * i.e. interrupt frequency is 16.667 Hz * 2 ~ 2133.33 Hz.
 * i.e. 2133.33 Hz / 16 Mhz ~ 7500 cpu cycles 
 * 
 * -> OCR1A = 7500
 * 
 * check that signal frequency is ~ 2133 Hz and wheel period ~ 60 ms
 */
 
volatile byte count;
volatile boolean value;


void setup() {
  pinMode(D11, OUTPUT);  // generated signal
  pinMode(D12, OUTPUT);  // estimate regarding cpu time consumption of interrupt service routine   

  digitalWrite(D11, 0);
  digitalWrite(D12, 0);
  // Timer 1
  noInterrupts();           // disable all interrupts temporarily
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;                // initialize register with 0
  OCR1A = 7500;            // initialize match compare register (16Mhz/interrupt frequency)
                            // 65535 = 2**16-1
  TCCR1B |= (0 << CS12) | (0<< CS11) | (1>> CS10); // no prescale
  TIMSK1 |= (1 << OCIE1A);  // activate timer compare interrupt
  interrupts();             // activate all interrupts
}

ISR(TIMER1_COMPA_vect)        
{
  TCNT1 = 0;
  digitalWrite(D12, 1);
  digitalWrite(D11, value);
  if (count % 2 == 0 && count < 124) {
    value = 1;
  } else {
    value = 0;
  }
  count++;  
  count = count % 128;
  digitalWrite(D12, 0);
}

void loop() {
}
