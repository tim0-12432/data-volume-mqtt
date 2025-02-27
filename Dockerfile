
# Requirements
FROM python:3.12-slim
COPY /requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Run App
COPY /static /app/static
COPY /templates /app/templates
COPY /run.py /app/run.py
COPY /healthcheck.py /app/healthcheck.py
ENTRYPOINT [ "python" ]
CMD ["run.py"]
HEALTHCHECK --interval=12s --timeout=12s --start-period=30s --retries=3 CMD python healthcheck.py
