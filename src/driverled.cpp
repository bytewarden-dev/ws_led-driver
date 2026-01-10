#include <stdafx.h>
#include <driverled.h>

DriverLED::DriverLED(uint8_t pin, uint8_t count)
{
	strip = new Adafruit_NeoPixel(count, pin, NEO_GRB + NEO_KHZ800);

}


void DriverLED::begin() {
	strip->begin();
	strip->show();
}


void DriverLED::update()
{

}


void DriverLED::setMode()
{
}
