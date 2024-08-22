FROM python:3.11

RUN apt update -y && apt install -y vim nodejs npm
RUN pip install pipenv

ENV SHELL=/bin/bash

RUN useradd -m -s ${SHELL} -u 1003 jupyter
WORKDIR /home/jupyter

ADD Pipfile Pipfile.lock jupyter_server_config.py ./
RUN su - jupyter -c "pipenv install"

EXPOSE 8080

ENTRYPOINT ["pipenv", "run"]
CMD ["jupyter", "lab", "--help"]
