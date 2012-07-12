#define FIFO_PATH "/dev/nervend"
#define HEADSET_TYPE "developer"

#define ND_CHANNELS 16 /* 14 electrodes plus two gyro */
#define ND_EEG_CHANNELS 14
#define ND_GYRO_CHANNELS 2
#define ND_EEG_FREQ 128 /* sensor sample frequency = 128hz */
#define ND_GYRO_FREQ 128
#define ND_EEG_PHYS_MAX 16.7
#define ND_EEG_PHYS_MIN -(ND_EEG_PHYS_MAX)
#define ND_EEG_DIG_MAX 8192
#define ND_EEG_DIG_MIN -(ND_EEG_DIG_MAX)
#define ND_GYRO_PHYS_MAX 128.0 /* same as digital max for now */
#define ND_GYRO_PHYS_MIN -(ND_GYRO_PHYS_MAX)
#define ND_GYRO_DIG_MAX 128
#define ND_GYRO_DIG_MIN -(ND_GYRO_DIG_MAX)
#define ND_EEG_DIM "mV"
#define ND_GYRO_DIM "mV"

#ifndef DEBUG
#define DEBUG 1
#endif
