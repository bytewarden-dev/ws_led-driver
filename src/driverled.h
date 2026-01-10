#ifndef __DRIVERLED_H__
#define __DRIVERLED_H__

#include <Adafruit_NeoPixel.h>

enum T_STATE {
	INIT,
	SCANNER,
	RAINBOW,	
	STATIC,
	STOPPED,
	SHUTDOWN
};


class DriverLED {
private:
	Adafruit_NeoPixel *strip;

public:
	DriverLED(uint8_t pin, uint8_t count);

	void begin();

	void update();

	void setMode();
};

#endif // ! __DRIVERLED_H__