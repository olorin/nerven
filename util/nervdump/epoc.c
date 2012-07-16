#include "epoc.h"

const unsigned char F3_MASK[14] = {10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7}; 
const unsigned char FC6_MASK[14] = {214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195};
const unsigned char P7_MASK[14] = {84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65};
const unsigned char T8_MASK[14] = {160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157};
const unsigned char F7_MASK[14] = {48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45};
const unsigned char F8_MASK[14] = {178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175};
const unsigned char T7_MASK[14] = {66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63};
const unsigned char P8_MASK[14] = {158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139};
const unsigned char AF4_MASK[14] = {196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177};
const unsigned char F4_MASK[14] = {216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213};
const unsigned char AF3_MASK[14] = {46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27};
const unsigned char O2_MASK[14] = {140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121};
const unsigned char O1_MASK[14] = {102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83};
const unsigned char FC5_MASK[14] = {28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9};
const unsigned char QUAL_MASK[14] = {106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119};

int get_level(unsigned char pkt[32], const unsigned char mask[14]) {
	int i, byte, offset, level;
	level = 0;
	for (i=13; i >= 0; --i) {
		level <<= 1;
		byte = (mask[i] / 8) + 1;
		offset = mask[i] % 8;
		level |= (pkt[byte] >> offset) & 1;
	}
	return level;
}

int *get_measured_sensor(epoc_headset *headset) {
	int c;
	epoc_contact_quality s = headset->quality;
	int *sensors[] = {&s.F3, &s.FC5, &s.AF3, &s.F7, &s.T7, &s.P7, &s.O1, &s.O2, &s.P8, &s.T8, &s.F8, &s.AF4, &s.FC6, &s.F4, &s.F8, &s.AF4};
	c = headset->current_pkt.counter;
	if (c >= 64 && c < 64+14) 
		c -= 64;
	if (c > 15)
		return 0;
	return sensors[c];
}

void epoc_load_pkt(unsigned char buf[], epoc_headset *headset) {
	int *measured_sensor;
	headset->current_pkt.sensor_data.F3 = get_level(buf, F3_MASK);
	headset->current_pkt.sensor_data.FC6 = get_level(buf, FC6_MASK);
	headset->current_pkt.sensor_data.P7 = get_level(buf, P7_MASK);
	headset->current_pkt.sensor_data.T8 = get_level(buf, T8_MASK);
	headset->current_pkt.sensor_data.F7 = get_level(buf, F7_MASK);
	headset->current_pkt.sensor_data.F8 = get_level(buf, F8_MASK);
	headset->current_pkt.sensor_data.T7 = get_level(buf, T7_MASK);
	headset->current_pkt.sensor_data.P8 = get_level(buf, P8_MASK);
	headset->current_pkt.sensor_data.AF4 = get_level(buf, AF4_MASK);
	headset->current_pkt.sensor_data.F4 = get_level(buf, F4_MASK);
	headset->current_pkt.sensor_data.AF3 = get_level(buf, AF3_MASK);
	headset->current_pkt.sensor_data.O2 = get_level(buf, O2_MASK);
	headset->current_pkt.sensor_data.O1 = get_level(buf, O1_MASK);
	headset->current_pkt.sensor_data.FC5 = get_level(buf, FC5_MASK);
	headset->current_pkt.gyro.x = buf[29] - GYRO_X_ZERO;
	headset->current_pkt.gyro.y = buf[30] - GYRO_Y_ZERO;
	headset->current_pkt.counter = buf[0];
	/* if the MSB of the counter is set, the remaining bits are a
	   battery value. */
	if (headset->current_pkt.counter & 128) 
		headset->battery = headset->current_pkt.counter & 127;
	measured_sensor = get_measured_sensor(headset);
	if (measured_sensor)
		*measured_sensor = get_level(buf, QUAL_MASK);
}
