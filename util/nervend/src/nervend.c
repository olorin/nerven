#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <syslog.h>
#include <signal.h>
#include <pthread.h>
#include <sys/resource.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "emokit/emokit.h"

#include "nervend.h"

sigset_t mask;

void fatal_err(const char *msg) {
  syslog(LOG_INFO, msg);
  exit(1);
}

void init_fatal_err(const char *msg) {
  printf("Fatal: %s\n", msg);
  exit(1);
}

void *thr_signal_handler(void *arg) {
  int sig;
  for (;;) {
    if (sigwait(&mask, &sig) != 0) {
      fatal_err("sigwait failed.");
    }
    switch (sig) {
    case SIGTERM:
      syslog(LOG_INFO, "Caught SIGTERM. Exiting.");
      remove(FIFO_PATH);
      exit(0);
      
    case SIGPIPE:
      syslog(LOG_INFO, "Reader exited; blocking.");
      break;

    default:
      syslog(LOG_INFO, "Caught unexpected signal: %d", sig);
      }
  }
}

int daemon_running() {
  int fd;
  char buf[16];
  struct flock fl;
  fd = open(PIDFILE, O_RDWR|O_CREAT, LOCKMODE);
  if (fd < 0) 
    fatal_err("cannot open pidfile.");
  fl.l_type = F_WRLCK;
  fl.l_start = 0;
  fl.l_whence = SEEK_SET;
  fl.l_len = 0;
  fl.l_pid = getpid();
  if (fcntl(fd, F_SETLK, &fl) < 0) {
    if (errno == EACCES || errno == EAGAIN) {
      close(fd);
      return 1;
    }
    fatal_err("cannot lock pidfile.");
  }
  ftruncate(fd, 0);
  sprintf(buf, "%ld", (long) getpid());
  write(fd, buf, strlen(buf)+1);
  return 0;
}

void daemonize() {
  int i, fd0, fd1, fd2;
  pid_t pid;
  struct rlimit rl;
  struct sigaction sa;
  umask(0);
  if (getrlimit(RLIMIT_NOFILE, &rl) < 0) 
    init_fatal_err("Fatal: can't get file limit.");

  if ((pid = fork()) < 0) 
    init_fatal_err("Fatal: can't fork.");
  else if (pid != 0)
    exit(0);
  setsid();
  
  sa.sa_handler = SIG_IGN;
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = 0;
  if (sigaction(SIGHUP, &sa, NULL) < 0) 
    init_fatal_err("Fatal: can't ignore SIGHUP.");
  if ((pid = fork()) < 0)
    init_fatal_err("Fatal: can't fork.\n");
  else if (pid != 0)
    exit(0);

  /* switch working directory to / so we're not preventing
     anything from unmounting */
  if (chdir("/") < 0)
    init_fatal_err("Fatal: can't chdir to /.");

  if (rl.rlim_max == RLIM_INFINITY)
    rl.rlim_max = 1024;
  for (i=0; i < rl.rlim_max; ++i) 
    close(i);

  /* so we can't spew into standard streams */
  fd0 = open("/dev/null", O_RDWR);
  fd1 = dup(fd0);
  fd2 = dup(fd0);

  openlog(DAEMON_IDENT, LOG_CONS, LOG_DAEMON);
  syslog(LOG_INFO, "nervend running; decrypted EEG data will be written to %s.", FIFO_PATH);

}

void dbg_stream(emokit_device *eeg) {
  int i;
  for (;;) {
    if (emokit_read_data(eeg)) {
      emokit_get_next_frame(eeg);
      for (i=0; i < 32; ++i) {
	printf("%d ", eeg->raw_unenc_frame[i]);
      }
      putchar('\n');
      fflush(stdout);
    }
  }
}

void decrypt_loop(emokit_device *eeg) {
  int i;
  FILE *nervend_fifo;
  nervend_fifo = fopen(FIFO_PATH, "wb");
  if (!nervend_fifo) {
    fatal_err("cannot open FIFO for writing.");
  }
  for (;;) {
    if (emokit_read_data(eeg)) {
      emokit_get_next_frame(eeg);
      fwrite(eeg->raw_unenc_frame, 1, EMOKIT_PKT_SIZE, nervend_fifo);
    }
  }
}

void exit_usage(char *exec_name) {
  printf("Usage: %s consumer|developer\n", exec_name);
  exit(1);
}

int main(int argc, char **argv) {
  int i;
  unsigned char dev_type;
  pthread_t tid;
  struct sigaction sa;
  emokit_device *eeg;
  if (argc < 2) {
    exit_usage(argv[0]);
  }
  if (strcmp(argv[1], "consumer") == 0) 
    dev_type = EMOKIT_CONSUMER;
  else if (strcmp(argv[1], "developer") == 0)
    dev_type = EMOKIT_DEVELOPER;
  else 
    exit_usage(argv[0]);
  if (!DEBUG) {
    daemonize();
    if (daemon_running()) {
      syslog(LOG_INFO, "Looks like nervend is already running.\n");
      exit(1);
    }
  }
  eeg = emokit_create(dev_type);
  if (emokit_open(eeg, EMOKIT_VID, EMOKIT_PID, 0) != 0) {
    fatal_err("cannot access device. Are you root?");
    return 1;
  }
  if ((access(FIFO_PATH, W_OK) < 0) && mkfifo(FIFO_PATH, 0666) != 0) {
    fatal_err("cannot create FIFO.");
  }
  sa.sa_handler = SIG_DFL;
  sigemptyset(&sa.sa_mask);
  if (sigaction(SIGHUP, &sa, NULL) < 0)
    fatal_err("cannot restore SIGHUP.");
  sigfillset(&mask);
  if (pthread_sigmask(SIG_BLOCK, &mask, NULL) != 0)
    fatal_err("SIG_BLOCK error.");
  if (pthread_create(&tid, NULL, thr_signal_handler, 0) != 0) 
    fatal_err("cannot create thread.");
  decrypt_loop(eeg);
  return 0;
}
