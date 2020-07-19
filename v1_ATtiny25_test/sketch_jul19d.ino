
int analogPin = PB3; 
int val = 1;


void setup() {
  // put your setup code here, to run once:
  pinMode(PB0, OUTPUT);
  pinMode(PB1, OUTPUT);
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
  
  
}
