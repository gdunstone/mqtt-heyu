FROM alpine
MAINTAINER Gareth Dunstone <freedom.2.the.leetle.people@gmail.com>

RUN apk -U add curl build-base python3 py3-pip && pip3 install paho-mqtt

RUN curl -LsSO https://github.com/HeyuX10Automation/heyu/archive/v2.11-rc3.tar.gz \
 && tar xzf v2.11-rc3.tar.gz \
 && cd heyu-2.11-rc3 \
 # && export OPTIONS="--disable-cm17a --disable-ext0 --disable-rfxs --disable-rfxm --disable-dmx --disable-kaku --disable-rfxlan" \
 && ./configure --sysconfdir=/etc \
 && make -j$(nproc) \
 && make install \
 && cd / \
 && apk --purge del curl build-base \
 && rm -rf /build /etc/ssl /var/cache/apk/* /lib/apk/db/*

RUN cp -r /etc/heyu /etc/heyu.default \
 && mkdir -p /usr/local/var/tmp/heyu \
 && mkdir -p /usr/local/var/lock \
 && chmod 777 /usr/local/var/tmp/heyu \
 && chmod 777 /usr/local/var/lock


COPY heyu-run.sh /usr/local/bin/heyu-run
COPY mqtt-client.py /mqtt-client.py 
COPY x10.conf /etc/heyu/x10.conf
CMD heyu-run