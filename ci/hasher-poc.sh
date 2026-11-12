#!/bin/bash
# Proof of concept: run hasher inside a privileged ALT container.
# Expects /work/src.tar.gz (upstream source, named after Source0 basename)
# and /work/fontmaster.spec. Results are copied to /work/hasher-repo.
set -euxo pipefail

apt-get update
apt-get install -y gear hasher hasher-priv rpm-build shadow-utils util-linux sudo procps

echo '=== package contents (diagnostics) ==='
rpm -ql hasher-priv | head -40 || true
rpm -ql hasher | head -40 || true
systemctl --version 2>/dev/null | head -1 || echo 'no systemd'

# Unprivileged build user
useradd -m -s /bin/bash builder
printf 'builder ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/builder
chmod 0440 /etc/sudoers.d/builder

# Helper users: builder_a (pseudo-root R) and builder_b (builder U)
/usr/sbin/hasher-useradd builder

# Start the privileged helper daemon (no systemd in the container)
if ! pgrep -x hasher-privd >/dev/null 2>&1; then
    /usr/sbin/hasher-privd || true
    sleep 2
fi
pgrep -a hasher-privd || echo 'WARNING: hasher-privd is not running'

# rpmbuild tree for the build user
install -d -o builder -g builder \
    /home/builder/rpmbuild/SOURCES /home/builder/rpmbuild/SPECS \
    /home/builder/rpmbuild/BUILD /home/builder/rpmbuild/BUILDROOT \
    /home/builder/rpmbuild/RPMS /home/builder/rpmbuild/SRPMS
cp /work/src.tar.gz /home/builder/rpmbuild/SOURCES/
cp /work/fontmaster.spec /home/builder/rpmbuild/SPECS/
chown -R builder:builder /home/builder/rpmbuild

# Build the SRPM as the unprivileged user (rpmbuild refuses root)
setpriv --reuid=builder --regid=builder --init-groups \
    env HOME=/home/builder USER=builder \
    rpmbuild --define '_topdir /home/builder/rpmbuild' \
    -bs /home/builder/rpmbuild/SPECS/fontmaster.spec

srpm=$(find /home/builder/rpmbuild/SRPMS -name '*.src.rpm' -print -quit)
echo "SRPM: $srpm"

# hasher workdir and config
install -d -o builder -g builder /home/builder/hasher /home/builder/.hasher
printf 'workdir="/home/builder/hasher"\nnprocs=2\n' > /home/builder/.hasher/config
chown -R builder:builder /home/builder/.hasher /home/builder/hasher

set +e
setpriv --reuid=builder --regid=builder --init-groups \
    env HOME=/home/builder USER=builder \
    hsh /home/builder/hasher "$srpm" 2>&1 | tee /work/hasher.log
status=${PIPESTATUS[0]}
set -e

mkdir -p /work/hasher-repo
find /home/builder/hasher/repo -name '*.rpm' -exec cp -v {} /work/hasher-repo/ \; || true

exit "$status"
