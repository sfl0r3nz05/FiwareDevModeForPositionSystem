#! /bin/bash

mkdir certs
cd certs
HOSTNAME=$(hostname)
INTERFACE=$(ip route | grep default | awk '{print $5}')
IPADDRESS=$(ip addr show "$INTERFACE" | grep -oP 'inet \K[\d.]+')

# Create root CA & Private key
openssl req -x509 \
            -newkey rsa:2048 \
            -nodes \
            -sha256 \
            -days 356 \
            -subj "/C=ES/ST=Gipuzkoa/L=San Sebastian/O=CEIT/OU=DAIM/CN=${HOSTNAME}" \
            -keyout rootCA.key -out rootCA.crt

openssl x509 -outform pem -in rootCA.crt -out rootCA.pem

# Copy rootCA.crt certificate to /usr/share/ca-certificates/
#sudo cp rootCA.crt /usr/share/ca-certificates/
sudo cp rootCA.crt /usr/local/share/ca-certificates/

# Update certificates and local certificates
#sudo dpkg-reconfigure ca-certificates
sudo update-ca-certificates

for arg in "$@"; do
    DOMAIN=$arg

    # Generate Private key 
    openssl genrsa -out ${DOMAIN}.key 2048

    # Create csf conf
    cat > csr.conf << EOF
[ req ]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
C = ES
ST = Gipuzkoa
L = San Sebastian
O = CEIT
OU = DAIM
CN = ${HOSTNAME}

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = ${DOMAIN}
DNS.2 = ${HOSTNAME}
DNS.3 = localhost
IP.1 = 127.0.0.1 
IP.2 = ${IPADDRESS}
EOF

    # create CSR request using private key
    openssl req -new -key ${DOMAIN}.key -out ${DOMAIN}.csr -config csr.conf

    # Create a external config file for the certificate
    cat > openssl.cnf <<EOF
authorityKeyIdentifier=keyid:always, issuer:always
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = ${DOMAIN}
DNS.2 = ${HOSTNAME}
DNS.3 = localhost
IP.1 = 127.0.0.1 
IP.2 = ${IPADDRESS}
EOF

# Create SSl with self signed CA

    openssl x509 -req \
        -in ${DOMAIN}.csr \
        -CA rootCA.crt \
        -CAkey rootCA.key \
        -CAcreateserial \
        -out ${DOMAIN}.crt \
        -days 730 \
        -sha256 \
        -extfile openssl.cnf

# Certificate verification
openssl verify -CAfile rootCA.crt -verify_hostname ${DOMAIN} ${DOMAIN}.crt
openssl verify -CAfile rootCA.crt -verify_hostname ${HOSTNAME} ${DOMAIN}.crt

# Copy certificates
#sudo cp ${DOMAIN}.crt /usr/share/ca-certificates/
sudo cp ${DOMAIN}.crt /usr/local/share/ca-certificates/

# Update certificates and local certificates
#sudo dpkg-reconfigure ca-certificates
sudo update-ca-certificates

done

# Copy certificates
mkdir ../../nginx/certs/
cp -f api.crt ../../nginx/certs/nginx-selfsigned.crt
cp -f api.key ../../nginx/certs/nginx-selfsigned.key
openssl dhparam -out ../../nginx/certs/dhparam.pem 2048
chmod 664 -R *.key
chmod 664 -R *.crt