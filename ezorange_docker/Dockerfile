FROM ubuntu:focal

RUN apt-get update
RUN apt-get install -y xinetd
RUN apt-get clean
RUN useradd -m orangeworld

ADD share/ /home/orangeworld/
ADD xinetd /etc/xinetd.d/orangeworld


RUN chown -R orangeworld:orangeworld /home/orangeworld
RUN chown root:root /home/orangeworld/flag.txt
RUN chown orangeworld:root /home/orangeworld/ezorange
RUN chmod 444 /home/orangeworld/flag.txt
RUN chmod +x /home/orangeworld/ezorange
RUN chmod +x /home/orangeworld/ld-2.32.so
RUN chmod +x /home/orangeworld/libc.so.6
RUN chmod +x /home/orangeworld/run.sh

USER orangeworld
WORKDIR /home/orangeworld

CMD ["/usr/sbin/xinetd", "-dontfork"]