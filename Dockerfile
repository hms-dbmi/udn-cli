FROM ubuntu

RUN	apt-get -y update && \
	apt-get -y install python3 && \
	apt-get -y install python3-pip

RUN pip3 install --upgrade pip

RUN mkdir /udn_cli
COPY . /udn_cli
WORKDIR /udn_cli
RUN pip3 install .

RUN mkdir /root/.udn
COPY dev_config /root/.udn/config



