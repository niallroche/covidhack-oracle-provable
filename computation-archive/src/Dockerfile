FROM frolvlad/alpine-python3
MAINTAINER Oraclize "info@oraclize.it"

RUN apt-get update && apt-get install -y python-numpy
CMD python -c "import numpy; print int(numpy.linalg.det(numpy.array([[1,2,3],[7,2,3],[7,6,3]])))"

# COPY url-requests.py /

# RUN pip3 install requests
# CMD python ./url-requests.py
