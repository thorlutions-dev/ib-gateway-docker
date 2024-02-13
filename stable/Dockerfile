
#
# Setup Stage: install apps
#
# This is a dedicated stage so that donwload archives don't end up on 
# production image and consume unnecessary space.
#

FROM ubuntu:22.04 as setup

ENV IB_GATEWAY_REPO=github.com/thorlutions-dev/ib-gateway-docker
ENV IB_GATEWAY_NAME=tws
ENV IB_GATEWAY_VERSION=10.19.2i
ENV IB_GATEWAY_RELEASE_CHANNEL=stable
ENV IBC_VERSION=3.18.0
ENV IBC_TAG_VERSION=3.18.0-Update.1

# Prepare system
RUN apt-get update -y
RUN apt-get install --no-install-recommends --yes \
  curl \
  ca-certificates \
  unzip

WORKDIR /tmp/setup

# Install IB Gateway
# Use this instead of "RUN curl .." to install a local file:
#COPY ${IB_GATEWAY_NAME}-${IB_GATEWAY_VERSION}-standalone-linux-x64.sh .
RUN curl -sSL https://${IB_GATEWAY_REPO}/releases/download/${IB_GATEWAY_NAME}-${IB_GATEWAY_RELEASE_CHANNEL}%40${IB_GATEWAY_VERSION}/${IB_GATEWAY_NAME}-${IB_GATEWAY_VERSION}-standalone-linux-x64.sh \
  --output ${IB_GATEWAY_NAME}-${IB_GATEWAY_VERSION}-standalone-linux-x64.sh
RUN curl -sSL https://${IB_GATEWAY_REPO}/releases/download/${IB_GATEWAY_NAME}-${IB_GATEWAY_RELEASE_CHANNEL}%40${IB_GATEWAY_VERSION}/${IB_GATEWAY_NAME}-${IB_GATEWAY_VERSION}-standalone-linux-x64.sh.sha256 \
  --output ${IB_GATEWAY_NAME}-${IB_GATEWAY_VERSION}-standalone-linux-x64.sh.sha256
RUN sha256sum --check ./${IB_GATEWAY_NAME}-${IB_GATEWAY_VERSION}-standalone-linux-x64.sh.sha256
RUN chmod a+x ./${IB_GATEWAY_NAME}-${IB_GATEWAY_VERSION}-standalone-linux-x64.sh
RUN ./${IB_GATEWAY_NAME}-${IB_GATEWAY_VERSION}-standalone-linux-x64.sh -q -dir /root/Jts/${IB_GATEWAY_NAME}/${IB_GATEWAY_VERSION}
COPY ./config/${IB_GATEWAY_NAME}/jts.ini /root/Jts/jts.ini

# Install IBC
RUN curl -sSL https://github.com/IbcAlpha/IBC/releases/download/${IBC_TAG_VERSION}/IBCLinux-${IBC_VERSION}.zip --output IBCLinux-${IBC_VERSION}.zip
RUN mkdir /root/ibc
RUN unzip ./IBCLinux-${IBC_VERSION}.zip -d /root/ibc
RUN chmod -R u+x /root/ibc/*.sh 
RUN chmod -R u+x /root/ibc/scripts/*.sh
COPY ./config/ibc/config.ini.tmpl /root/ibc/config.ini.tmpl

# Copy scripts
COPY ./scripts /root/scripts

#
# Build Stage: build production image
#

FROM ubuntu:22.04

ENV IB_GATEWAY_VERSION=10.19.2i
ENV IB_GATEWAY_NAME=tws

WORKDIR /root

# Prepare system
RUN apt-get update -y
RUN apt-get install --no-install-recommends --yes \
  gettext \
  xvfb \
  libxslt-dev \
  libxrender1 \
  libxtst6 \
  libxi6 \
  libgtk2.0-bin \
  libgtk-3-0 \
  socat \
  x11vnc

# Copy files
COPY --from=setup /root/ .
RUN chmod a+x /root/scripts/*.sh
COPY --from=setup /usr/local/i4j_jres/ /usr/local/i4j_jres

# IBC env vars
ENV TWS_MAJOR_VRSN ${IB_GATEWAY_VERSION}
ENV TWS_PATH /root/Jts/${IB_GATEWAY_NAME}
ENV TWS_SETTINGS_PATH /root/Jts
ENV IBC_PATH /root/ibc
ENV IBC_INI /root/ibc/config.ini
ENV TWOFA_TIMEOUT_ACTION exit

# Start run script
CMD ["/root/scripts/run.sh"]
