FROM continuumio/anaconda3:2022.10

COPY . /repo
WORKDIR /repo

RUN conda env create -f /repo/environment.yml
SHELL ["conda", "run", "-n", "kcubeExecute", "/bin/bash", "-c"]
RUN export FLASK_APP="app:create_app('default')" && \
    export FLASK_SETTING=../docker/standalone/config && \
    flask init-neo4j

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=9000"]
EXPOSE 9000