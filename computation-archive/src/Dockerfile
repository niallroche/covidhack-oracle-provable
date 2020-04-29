# The Oracle works on the basis that the last line writtent to Sys out is returned to the caller

FROM frolvlad/alpine-python3
#FROM ubuntu:14.04
MAINTAINER Oraclize "info@oraclize.it"

#RUN apt-get update && apt-get install -y python-numpy
#CMD python -c "import numpy; print int(numpy.linalg.det(numpy.array([[1,2,3],[7,2,3],[7,6,3]])))"
#
COPY url-requests.py /
COPY response_parser.py /

RUN pip3 install requests

ENV ARG0="GET"
ENV ARG1="https://www.gov.uk/government/publications/further-businesses-and-premises-to-close/further-businesses-and-premises-to-close-guidance"
ENV ARG2="{'headers': {'content-type': 'html'}}"

CMD python ./url-requests.py