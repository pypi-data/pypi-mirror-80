FROM fedora

RUN dnf update -y
RUN dnf -y install httpd
RUN dnf clean all
# RUN systemctl enable httpd

EXPOSE 80

CMD [ "/sbin/init" ]