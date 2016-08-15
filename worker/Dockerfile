FROM python:2.7.11

# copy sources
WORKDIR /root
ADD worker.py /root

# run
RUN pip install redis
CMD ["python", "worker.py"]
