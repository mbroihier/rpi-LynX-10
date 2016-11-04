#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <sys/time.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>

#define PORT            2222
#define MSGSIZE         256
#define BAUDRATE        B1200
#define MODEMDEVICE     "/dev/ttyUSB0"
#define _POSIX_SOURCE   1           /* POSIX compliant source */
//********************************************************************************************************************//
//--------------------------------------------------------------------------------------------------------------------//
// DESCRIPTION: x10_server                                                                                            //
//                                                                                                                    //
//    The x10_server receives x10 commands from a client process and tranmits the commands to the x10 transmitter.    //
// Replies from the transmitter are sent back to the client.
//--------------------------------------------------------------------------------------------------------------------//
//--------------------------------------------------------------------------------------------------------------------//
// PROCESSING:                                                                                                        //
// if running as a deamon (-d argument) {                                                                             //
//   fork a child and in the child, close all standard files                                                          //
// }                                                                                                                  //
// setup socket for clients;                                                                                          //
// do forever {                                                                                                       //
//   fork another child                                                                                               //
//   if child {                                                                                                       //
//     do until told to stop{                                                                                         //
//       accept a connection;                                                                                         //
//       read the desired command;                                                                                    //
//       if it isn't a terminate request, send it to the x10 transmitter;                                             //
//     }                                                                                                              //
//     terminate;                                                                                                     //
//   else                                                                                                             //
//     wait for child termination;                                                                                    //
// }                                                                                                                  //
//--------------------------------------------------------------------------------------------------------------------//
//********************************************************************************************************************//

int main(int argc, char* argv[]) {
  char     msg[MSGSIZE];  /* used for message */

  int      sd, currentSd, cc, exitClient, i, j, msgSize;
  int      addrlen;
  struct   sockaddr_in sin;
  struct   sockaddr_in clientConnection;
  fd_set   inputReady;
  fd_set   inputReadyCopy;
  struct   timeval delay;

  int x10Fd, res, offset;

  struct termios serialIOSettings;
  char buf[255];

  pid_t pid;
  int   status;

  if ((argc == 2) && strstr(argv[1],"-d")) {
    pid = fork(); // if this is to run as a daemon, fork, close standard files in the child process, and
                  // terminate the current process
      if (pid == 0) {
	close(0);
	close(1);
	close(2);
      } else {
	return(0);
      }
  }
  
  offset = 0;

  if ((sd = socket(PF_INET, SOCK_STREAM, 6)) == -1) {
    perror("socket");
    return(1);
  }

  memset(&sin, 0, sizeof(sin));
  sin.sin_family = PF_INET;
  sin.sin_addr.s_addr = INADDR_ANY;
  sin.sin_port = htons(PORT);

  if (bind(sd, (struct sockaddr *) &sin, sizeof(sin)) == -1) {
    perror("bind");
    return(1);
  }

  /* listen on the socket for "x10 clients"  */
  if (listen(sd, 1) == -1) {
    perror("listen");
    return(1);
  }

  addrlen = sizeof(clientConnection);

  while (1 == 1) { // do forever - note there is only one serial device so servicing clients in parallel should not be done
    pid = fork();
    if (pid == 0) { /* this is the child process - do the work */
      while (1==1) {
        if ((currentSd = accept(sd, (struct sockaddr *)  &clientConnection, &addrlen)) == -1) {
          perror("accept");
          return(1);
        }

        exitClient = 0;
        printf ("Client attached\n");

        x10Fd = open(MODEMDEVICE, O_RDWR | O_NOCTTY ); 
        if (x10Fd <0) {perror(MODEMDEVICE); close(currentSd); return(-1); }
  
        bzero(&serialIOSettings, sizeof(serialIOSettings));
        serialIOSettings.c_cflag = CS8 | CLOCAL | CREAD;
        serialIOSettings.c_iflag = IGNPAR;
        serialIOSettings.c_oflag = 0;
  
        /* set input mode (non-canonical, no echo,...) */
        serialIOSettings.c_lflag = 0;
   
        serialIOSettings.c_cc[VTIME]    = 0;   /* inter-character timer unused */
        serialIOSettings.c_cc[VMIN]     = 0;   /* nonblocking read  */
 
        tcflush(x10Fd, TCIFLUSH);
        cfsetispeed(&serialIOSettings, BAUDRATE);
        cfsetospeed(&serialIOSettings, BAUDRATE);
        if (tcsetattr(x10Fd,TCSANOW,&serialIOSettings)) {
          printf("Error setting attributes\n");
	  close(currentSd); close(x10Fd);
          return(-1);
        }

        FD_ZERO(&inputReadyCopy);
        FD_SET(currentSd, &inputReadyCopy);
        FD_SET(x10Fd,     &inputReadyCopy);

        while (!exitClient) { /* get a message from the client or x10 hardware */
          delay.tv_sec = 1;
          delay.tv_usec = 0;
          inputReady = inputReadyCopy;
          select(16,&inputReady,NULL,NULL,&delay);
          if (FD_ISSET(currentSd,&inputReady)) { 
            if ((msgSize = recv(currentSd, msg, sizeof(msg), 0)) == -1) {
              perror("recv");
              exitClient = 1;
            }
	    if (msgSize) {
              printf ("command received from socket, packet size = %d\n",msgSize);
	    } else {
	      exitClient = 1;
	    }

	    if (!exitClient) {
              /* echo the message */
              msg[msgSize] = 0;
              printf ("%s\n", msg);
              if (write(x10Fd, &msg, msgSize) == -1) {
                perror("write");
	        close(currentSd); close(x10Fd);
                return(1);
              }
	    }
          }
          if (FD_ISSET(x10Fd, &inputReady)) {
            printf ("response received from x10\n");
            res = read(x10Fd,&buf[offset],sizeof(buf)- offset);
	    offset += res;
            for (j=0;j<offset;j++){ // print all that will be sent
	      printf ("%c ",buf[j]); 
            }
	    if (offset > 0) {
              printf (" size:%d\n",res);
              if (buf[j-1] == '*') {
	        /* whole message received - sending to client */
                send(currentSd, &buf, j , 0);
	        printf ("Sending x10 reply packet to client\n");
                offset = 0  ;
	      } 
	    } else {
	      printf ("serial input was ready but no characters were read!!\n");
	    }
	  }
        }
        /* close incoming socket/files */
        printf ("Client terminated\n",msgSize);
        close(currentSd); close(x10Fd);
      }
    } else {
      waitpid(pid, &status, 0);
    }
  }  
}
