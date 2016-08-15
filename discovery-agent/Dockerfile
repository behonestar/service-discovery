FROM python:2.7.11

# install haproxy
WORKDIR /tmp
RUN wget http://www.haproxy.org/download/1.5/src/haproxy-1.5.1.tar.gz
RUN tar -zxvf haproxy-1.5.1.tar.gz
RUN cd haproxy-1.5.1 && make TARGET=generic && make install
RUN touch /var/run/haproxy.pid

# copy sources
WORKDIR /root
ADD main.py /root
ADD reload-haproxy.sh /root
ADD haproxy /root/haproxy


# run
RUN pip install python-etcd Jinja2
CMD ["python", "main.py"]
