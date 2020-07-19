int pot1 = 0;
int t1 = 11;

void setup() {
  // put your setup code here, to run once:
  pinMode(PB0, OUTPUT);
  pinMode(PB1, OUTPUT);
}


void loop() {
  loop1();
}

void loop1() {
  digitalWrite(PB1, LOW);
  digitalWrite(PB0, LOW);
  pot1 = analogRead(PB3);
  delay(t1);
  digitalWrite(PB0, HIGH);
  delay(t1);
  digitalWrite(PB0, LOW);
  for (int k=0;k<10;k++) {
    if ((pot1 & ( 1 << k )) >> k == 1) {
      digitalWrite(PB0, HIGH);
      digitalWrite(PB1, HIGH);
      delay(t1);
      digitalWrite(PB0, LOW);
      digitalWrite(PB1, LOW);
      delay(t1);
    } else {
      digitalWrite(PB0, HIGH);
      digitalWrite(PB1, LOW);
      delay(t1);
      digitalWrite(PB0, LOW);
      digitalWrite(PB1, LOW);
      delay(t1);      
    }
  }
  pot1 = pot1/1024*10;
  digitalWrite(PB0, HIGH);
  delay(pot1);
}

void loop2() {
  // put your main code here, to run repeatedly:
  /*
  digitalWrite(PB0, LOW);
  digitalWrite(PB1, HIGH);
  delay(10);
  digitalWrite(PB0, HIGH);
  digitalWrite(PB1, LOW);
  delay(10);
  */
  digitalWrite(PB0, LOW);
  pot1 = analogRead(PB3);
  pot1 / 4;
  //digitalWrite(PB1, HIGH);
  delay(10);
  digitalWrite(PB0, HIGH);
  //digitalWrite(PB1, LOW);
  delay(pot1);
  digitalWrite(PB0, LOW);
  


}
