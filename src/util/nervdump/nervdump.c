#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <errno.h>
#include "edflib.h"
#include "epoc.h"
#include "nervdump.h"

int edf_hdl;

void exit_usage(char *exec) {
	printf("usage: %s <path to data stream> <file to write>\n", exec);
	exit(1);
}

void exit_err(char *err) {
	printf("%s\n", err);
	exit(1);
}

void exit_init_err() {
	exit_err("error during EDF initialisation.\n");
}

void set_channel_freq(int hdl, int chan, int freq) {
	if (edf_set_samplefrequency(hdl, chan, freq) != 0) 
		exit_init_err();
}

void set_channel_phys_max(int hdl, int chan, double val) {
	if (edf_set_physical_maximum(hdl, chan, val) != 0) 
		exit_init_err();
}

void set_channel_dig_max(int hdl, int chan, int val) {
	if (edf_set_digital_maximum(hdl, chan, val) != 0) 
		exit_init_err();
}

void set_channel_dig_min(int hdl, int chan, int val) {
	if (edf_set_digital_minimum(hdl, chan, val) != 0) 
		exit_init_err();
}

void set_channel_phys_min(int hdl, int chan, double val) {
	if (edf_set_physical_minimum(hdl, chan, val) != 0) 
		exit_init_err();
}

void set_channel_label(int hdl, int chan, const char *label) {
	if (edf_set_label(hdl, chan, label)) 
		exit_init_err();
}

void set_dimension(int hdl, int chan, const char *dim) {
	if (edf_set_physical_dimension(hdl, chan, dim)) 
		exit_init_err();
}

void init_channels(int hdl) {
	int i;
	for (i=0; i < ND_EEG_CHANNELS; ++i) 
		set_channel_freq(hdl, i, ND_EEG_FREQ);
	for ( ; i < ND_EEG_CHANNELS + ND_GYRO_CHANNELS; ++i) 
		set_channel_freq(hdl, i, ND_GYRO_FREQ);
	for (i=0; i < ND_EEG_CHANNELS; ++i) 
		set_channel_phys_max(hdl, i, ND_EEG_PHYS_MAX);
	for ( ; i < ND_EEG_CHANNELS + ND_GYRO_CHANNELS; ++i) 
		set_channel_phys_max(hdl, i, ND_GYRO_PHYS_MAX);
	for (i=0; i < ND_EEG_CHANNELS; ++i) 
		set_channel_dig_max(hdl, i, ND_EEG_DIG_MAX);
	for ( ; i < ND_EEG_CHANNELS + ND_GYRO_CHANNELS; ++i) 
		set_channel_dig_max(hdl, i, ND_GYRO_DIG_MAX);
	for (i=0; i < ND_EEG_CHANNELS; ++i) 
		set_channel_dig_min(hdl, i, ND_EEG_DIG_MIN);
	for ( ; i < ND_EEG_CHANNELS + ND_GYRO_CHANNELS; ++i) 
		set_channel_dig_min(hdl, i, ND_GYRO_DIG_MIN);
	for (i=0; i < ND_EEG_CHANNELS; ++i) 
		set_channel_phys_min(hdl, i, ND_EEG_PHYS_MIN);
	for ( ; i < ND_EEG_CHANNELS + ND_GYRO_CHANNELS; ++i) 
		set_channel_phys_min(hdl, i, ND_GYRO_PHYS_MIN);
	set_channel_label(hdl, 0, "F3");
	set_channel_label(hdl, 1, "FC6");
	set_channel_label(hdl, 2, "P7");
	set_channel_label(hdl, 3, "T8");
	set_channel_label(hdl, 4, "F7");
	set_channel_label(hdl, 5, "F8");
	set_channel_label(hdl, 6, "T7");
	set_channel_label(hdl, 7, "P8");
	set_channel_label(hdl, 8, "AF4");
	set_channel_label(hdl, 9, "F4");
	set_channel_label(hdl, 10, "AF3");
	set_channel_label(hdl, 11, "O2");
	set_channel_label(hdl, 12, "O1");
	set_channel_label(hdl, 13, "FC5");
	set_channel_label(hdl, 14, "gyroX");
	set_channel_label(hdl, 15, "gyroY");
	for (i=0; i < ND_EEG_CHANNELS; ++i) 
		set_dimension(hdl, i, ND_EEG_DIM);
	for ( ; i < ND_EEG_CHANNELS + ND_GYRO_CHANNELS; ++i) 
		set_dimension(hdl, i, ND_GYRO_DIM);
	
}

void write_sample(int hdl, int *buf) {
	if (edfwrite_digital_samples(hdl, buf)) {
		printf("error writing sample.\n");
		exit(1);
	}
}

void close_recording(int hdl) {
	if (edfclose_file(hdl)) {
		printf("error closing file.\n");
		exit(1);
	}
}

void sigint(int signo) {
	printf("Cleaning up...\n");
	close_recording(edf_hdl);
	printf("Done.\n");
	exit(0);
}

int main(int argc, char **argv) {
	int i;
	long long nrecords;
	int sample_count;
	FILE *fifo;
	struct sigaction sa;
	unsigned char pkt_buf[32];
	int signal_buf[ND_CHANNELS][ND_EEG_FREQ];
	epoc_headset headset;

	if (argc < 3) 
		exit_usage(argv[0]);
	if ((fifo = fopen(argv[1], "rb")) < 0) {
		printf("cannot open fifo %s: %s.\n", argv[1], strerror(errno));
		exit(1);
	}

	if ((edf_hdl=edfopen_file_writeonly(argv[2], EDFLIB_FILETYPE_EDFPLUS, ND_CHANNELS)) < 0) {
		printf("cannot open EDF file for writing: %s", argv[2]);
		exit(1);
	}

	init_channels(edf_hdl);

	sa.sa_handler = sigint;
	sigemptyset(&sa.sa_mask);
	sigaddset(&sa.sa_mask, SIGHUP);
	sa.sa_flags = 0;
	if (sigaction(SIGINT, &sa, NULL) < 0) {
		printf("can't catch SIGINT: %s", strerror(errno));
		exit(1);
	}
	
	sample_count = 0;
	nrecords = 0;
	while (fread(pkt_buf, 1, 32, fifo) == 32) {
		epoc_load_pkt(pkt_buf, &headset);
		if (DEBUG)
			printf("%d %d %d %d\n", headset.quality.F3, headset.quality.FC6, headset.quality.P7, headset.quality.P8);
		signal_buf[0][sample_count] = headset.current_pkt.sensor_data.F3;
		signal_buf[1][sample_count] = headset.current_pkt.sensor_data.FC6;
		signal_buf[2][sample_count] = headset.current_pkt.sensor_data.P7;
		signal_buf[3][sample_count] = headset.current_pkt.sensor_data.T8;
		signal_buf[4][sample_count] = headset.current_pkt.sensor_data.F7;
		signal_buf[5][sample_count] = headset.current_pkt.sensor_data.F8;
		signal_buf[6][sample_count] = headset.current_pkt.sensor_data.T7;
		signal_buf[7][sample_count] = headset.current_pkt.sensor_data.P8;
		signal_buf[8][sample_count] = headset.current_pkt.sensor_data.AF4;
		signal_buf[9][sample_count] = headset.current_pkt.sensor_data.F4;
		signal_buf[10][sample_count] = headset.current_pkt.sensor_data.AF3;
		signal_buf[11][sample_count] = headset.current_pkt.sensor_data.O2;
		signal_buf[12][sample_count] = headset.current_pkt.sensor_data.O1;
		signal_buf[13][sample_count] = headset.current_pkt.sensor_data.FC5;
		signal_buf[14][sample_count] = headset.current_pkt.gyro.x;
		signal_buf[15][sample_count] = headset.current_pkt.gyro.y;

		++sample_count;
		if (sample_count == ND_EEG_FREQ) {
			for (i=0; i < ND_CHANNELS; ++i)
				write_sample(edf_hdl, signal_buf[i]);
			sample_count = 0;
			++nrecords;
		}
	}
	close_recording(edf_hdl);
	return 0;
}
