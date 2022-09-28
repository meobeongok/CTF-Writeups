FROM ubuntu:20.04

RUN /usr/sbin/useradd -u 1000 user

RUN apt-get update && apt-get install -y socat

WORKDIR /home/user/

USER user

COPY ./shared/ .

COPY flag.txt .

EXPOSE 13337

CMD socat \
      TCP-LISTEN:13337,reuseaddr,fork \
      EXEC:"/home/user/game"

# docker build . -t ubuntu20.04:game
# docker run -d -p 15000:13337 ubuntu20.04:game
