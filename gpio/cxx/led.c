#include <iostream>
#include <cstdlib>
#include <wiringPi.h>

const int LEDRED = 5,
      LEDGREEN = 6;

int main(void) {

    std::cout << "this pi version is " << piBoardRev()
        << std::endl;
    if (-1 == wiringPiSetup()) {
        std::cerr << "setup pi error"
            << std::endl;
        return -1;
    }

    pwmSetMode(PWM_MODE_BAL);

    // 设置针脚及模式
    pinMode(LEDRED, OUTPUT);
    pinMode(LEDGREEN, OUTPUT);

    for(auto i = 0; i < 15; i++) {
        digitalWrite(LEDRED, HIGH);
        delay(500);
        digitalWrite(LEDRED, LOW);
        digitalWrite(LEDGREEN, HIGH);
        delay(500);
        digitalWrite(LEDGREEN, LOW);
    }

    std::cout << "---------------- endl"
        << std::endl;

    return 0;
}
