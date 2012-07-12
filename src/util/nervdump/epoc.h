/* most of this is functionality, and some of this code, is taken from
   emokit by Kyle Machulis. I can't get emokit working with my hardware,
   so for now I'm adapting instead of linking the library.
*/
  
#ifndef EPOC_H
#define EPOC_H

#define GYRO_X_ZERO 106
#define GYRO_Y_ZERO 105

typedef struct epoc_sensor_data {
	int F3, FC6, P7, T8, F7, F8, T7, P8, AF4, F4, AF3, O2, O1, FC5;
} epoc_sensor_data;

typedef struct epoc_contact_quality {
	int F3, FC6, P7, T8, F7, F8, T7, P8, AF4, F4, AF3, O2, O1, FC5;
} epoc_contact_quality;

typedef struct epoc_gyro {
	char x, y;
} epoc_gyro;

typedef struct epoc_pkt {
	unsigned char counter;
	char battery;
	epoc_sensor_data sensor_data;
	epoc_gyro gyro;
	unsigned char raw_pkt[32];
} epoc_pkt;

typedef struct epoc_headset {
	epoc_pkt current_pkt;
	epoc_contact_quality quality;
	char battery;
} epoc_headset;

void epoc_load_pkt(unsigned char buf[], epoc_headset *headset);

#endif 
