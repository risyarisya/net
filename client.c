#include <netinet/in.h>
#include <stdio.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>

struct header {
  char type;
  unsigned long length;
};

int main()
{
  int sockfd;
  struct sockaddr_in client_addr = { 0 };
  
  int err;
  unsigned long width = 4240;
  unsigned long height = 2832;
  int size = 0;
  int sent = 0;
  int recved = 0;
  int chnum = 0;
  FILE *fp;
  unsigned char buf[1024] = { 0 };
  struct header packet = { 0 };
  struct header recv = { 0 };

  packet.type = 7;
  packet.length = width*height*3;
  
  if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
    printf("err\n");
    return 0;
  }

  client_addr.sin_family = PF_INET;
  client_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
  client_addr.sin_port = htons(12345);

  if (connect(sockfd, (struct sockaddr *)&client_addr,
	      sizeof(client_addr)) > 0) {
    printf("err1\n");
    close(sockfd);
    return 0;
  }

  write(sockfd, &packet, sizeof(packet));
  write(sockfd, &width, sizeof(width));
  write(sockfd, &height, sizeof(height));

  fp = fopen("DSC00568.data", "rb");

  while(1) {
    size = fread(buf, sizeof(unsigned char), 1024, fp);
    sent += size*sizeof(unsigned char);
    printf("file size=%d\n", sent);
    if (size > 0) {
      write(sockfd, buf, size*sizeof(unsigned char));
    } else {
      break;
    }
  }
  fclose(fp);

  read(sockfd, &recv, sizeof(recv));
  printf("ack!\n");
  chnum = 0;
  while(1) {
    read(sockfd, &recv, sizeof(recv));
    switch (recv.type) {
    case 1:
      fp = fopen("y.bin", "wb");
      break;
    case 2:
      fp = fopen("m.bin", "wb");
      break;
    case 3:
      fp = fopen("c.bin", "wb");
      break;
    case 4:
      fp = fopen("k.bin", "wb");
      break;
    default:
      break;
    }
    recved = 0;
    printf("ch=%d length=%lu\n", recv.type, recv.length);
    while(recved < recv.length) {
      size = read(sockfd, buf, sizeof(buf));
      fwrite(buf, sizeof(unsigned char), size, fp);
      recved += size;
      
    }
    chnum += 1;
    fclose(fp);
    packet.type = recv.type;
    packet.length = 0;
    write(sockfd, &packet, sizeof(packet));
    if (chnum==4) break;
  }
  close(sockfd);

  return 0;
}
