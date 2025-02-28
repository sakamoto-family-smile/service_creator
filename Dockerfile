FROM python:3.10

WORKDIR /work
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY app ./app

ENTRYPOINT [ "chainlit", "run", "app/ui.py" ]
