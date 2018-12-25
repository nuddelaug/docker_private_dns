#!/bin/bash

python /bind_config.py > /etc/generated.conf
cat <<EOF> /etc/named.conf
options {
    directory       "/var/named";
    dump-file       "/var/named/data/cache_dump.db";
    statistics-file "/var/named/data/named_stats.txt";
    memstatistics-file "/var/named/data/named_mem_stats.txt";
    recursing-file  "/var/named/data/named.recursing";
    secroots-file   "/var/named/data/named.secroots";
    allow-query     { any; };
    recursion ${DNS_RECURSION:-no};
    dnssec-enable yes;
    dnssec-validation yes;
    bindkeys-file "/etc/named.iscdlv.key";
    managed-keys-directory "/var/named/dynamic";
    pid-file "/run/named/named.pid";
    session-keyfile "/run/named/session.key";
};

zone "." IN {
        type hint;
        file "named.ca";
};

zone "${DNS_DOMAIN}" {
        type master;
        file "/etc/generated.conf";
};
EOF

/usr/sbin/named -fg -u named 
