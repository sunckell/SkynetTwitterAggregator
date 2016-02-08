FROM fedora:latest

# Install Python pip and Setuptools
RUN dnf install -y python3-pip python3-setuptools

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip3 install -r requirements.txt

# Bundle app source
ADD . /src

# Run
CMD ["python", "/src/skynet-twitter-aggregator.py"]