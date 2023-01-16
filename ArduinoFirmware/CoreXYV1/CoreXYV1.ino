int test = 10;
void setup(){
  Serial.begin(9600);
  pinMode(test, OUTPUT);
  digitalWrite(test, LOW);
}

void loop(){
  while (!Serial.available());
  int x = Serial.readString().toInt();
  analogWrite(test, x);
  
}
