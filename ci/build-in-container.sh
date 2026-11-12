#!/bin/bash
# Builds fontmaster.spec inside the ALT container (runs as root).
# ALT's rpmbuild refuses to run as root, so the build itself is done as an
# unprivileged user.
set -euxo pipefail

apt-get update
apt-get install -y \
    rpm-build cmake gcc-c++ make pkg-config git curl \
    shadow-utils util-linux \
    libharfbuzz-devel libpng-devel libcairo-devel librsvg-devel \
    libjpeg-devel libtiff-devel libxml2-devel zlib-devel \
    qt5-base-devel desktop-file-utils

useradd -m -s /bin/bash builder
chown -R builder:builder /work/rpmbuild

setpriv --reuid=builder --regid=builder --init-groups \
    env HOME=/home/builder USER=builder \
    rpmbuild --define "_topdir /work/rpmbuild" -ba /work/rpmbuild/SPECS/fontmaster.spec
