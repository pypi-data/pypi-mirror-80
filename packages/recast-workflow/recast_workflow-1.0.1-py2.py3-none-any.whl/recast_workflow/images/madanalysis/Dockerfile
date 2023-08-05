# Dockerfile

# Base image made by Samuel Meehan
FROM gitlab-registry.cern.ch/meehan/docker-lhcdmwg-april2020:latest

WORKDIR /LHC-DMWG/MG5_aMC_v2_7_2/madanalysis5
COPY ma5_install.dat .
COPY installer.sh .

RUN yum install -y tcl
RUN chmod +x /LHC-DMWG/MG5_aMC_v2_7_2/madanalysis5/installer.sh
RUN /LHC-DMWG/MG5_aMC_v2_7_2/madanalysis5/installer.sh
