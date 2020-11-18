#define BLYNK_PRINT stdout
 
#ifdef RASPBERRY
#include <BlynkApiWiringPi.h>
#else
#include <BlynkApiLinux.h>
#endif
#include <BlynkSocket.h>
#include <BlynkOptionsParser.h>

#include <wiringPi.h>
#include <softPwm.h>

static BlynkTransportSocket _blynkTransport;
BlynkSocket Blynk(_blynkTransport);
#include <BlynkWidgets.h>


BLYNK_WRITE(V0) {
  printf("Got a value: %s\n", param[0].asStr());
  softPwmWrite (18, param.asInt()) ;
  delay (10) ;
}
 

void setup(){
  wiringPiSetup();
  softPwmCreate (18, 0, 1000); //(pin, iniValue, Range)
}


void loop(){
  Blynk.run();
}

int main(int argc, char* argv[]){
  const char *auth, *serv;
  uint16_t port;
  parse_options(argc, argv, auth, serv, port);
  Blynk.begin(auth, serv, port);
    
  setup();
  while(true) {
    loop();
  }
    
  return 0;
}
