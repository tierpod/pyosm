FROM oraclelinux:9

ARG USERID
ENV USERID $USERID

# Install main dependencies
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm \
        rpmdevtools make yum-utils '@Development Tools' python3-devel \
    && dnf clean all

# Create builder group and user
RUN groupadd -g $USERID builder && \
    useradd -m -s /bin/bash -u $USERID -g $USERID builder

USER builder
RUN rpmdev-setuptree
WORKDIR /home/builder/rpmbuild
VOLUME [ "/host" ]
CMD rpmbuild -ba
