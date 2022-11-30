FROM continuumio/anaconda3:2022.10

COPY . /repo
WORKDIR /repo
RUN conda env create -f /repo/environment.yml
EXPOSE 9000