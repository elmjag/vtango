FROM ubuntu:20.04
ENV PYTHONUNBUFFERED 1
ARG DEBIAN_FRONTEND=noninteractive

RUN echo "deb-src http://archive.ubuntu.com/ubuntu/ focal universe\n" > /etc/apt/sources.list.d/tango.list
RUN apt-get update
RUN apt-get -y install libtango-dev gcc g++ curl less nano git
RUN wget https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init
RUN chmod +x ./rustup-init
RUN ./rustup-init -y

RUN git clone https://github.com/SKAJohanVenter/tango-controls-tui.git
RUN cd tango-controls-tui && /root/.cargo/bin/cargo build
RUN cp /tango-controls-tui/target/debug/tango-controls-tui /bin

COPY loopy.py .
CMD [ "/loopy.py" ]
