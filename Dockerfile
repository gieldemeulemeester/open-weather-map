FROM python:3-alpine

WORKDIR /user/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
RUN chmod u+x ./*.py

HEALTHCHECK --interval=5m CMD python healthcheck.py
ENTRYPOINT [ "python", "owm.py", "-L" ]
