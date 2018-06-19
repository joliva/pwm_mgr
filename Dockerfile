FROM py3-pigpio
ENTRYPOINT []

WORKDIR /root
ADD src /root
ADD requirements.txt /root
RUN pip3 install -r requirements.txt

CMD ["/usr/bin/python3", "/root/app.py"]

