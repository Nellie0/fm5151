    FROM ubuntu AS base

COPY information.py /app/
COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y python3 \
    && apt-get install -y pip \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

WORKDIR /app

ENTRYPOINT [ "python3", "information.py" ]

CMD [ "jupyter", \
    "lab", \
    "--port=8080", \
    "--no-browser", \
    "--ip=0.0.0.0", \
    "--allow-root" ]