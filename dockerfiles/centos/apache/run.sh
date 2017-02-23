#!/bin/bash
set -x

# re-create the dummy cert with the correct hostname
pushd /etc/pki/tls/certs/
if [ ! -e localhost.crt ]; then
rm localhost.crt
cat << EOF | make testcert
.
.
.
.
.
pulpapi
.
EOF
fi
popd

exec httpd -D FOREGROUND
