FROM neo4j:4.4.15-community
FROM continuumio/anaconda3:2022.10
ENV NEO4J_AUTH=neo4j/1234
RUN conda env create -f environment.yml
RUN conda activate kcubeExecute
ENV FLASK_APP="app:create_app('default')"
ENV FLASK_SETTING=./standalone/config
RUN flask init-neo4j
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=9000"]
EXPOSE 9000