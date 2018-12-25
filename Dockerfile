FROM docker.io/centos
RUN yum install -y python-IPy bind ; yum clean all ; rm -fR /var/cache/yum /etc/yum.repos.d/epel.repo
COPY bind_config.py /bind_config.py
EXPOSE "53" 
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ] 
