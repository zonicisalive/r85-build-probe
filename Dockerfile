FROM python:3-alpine
COPY probe.py /probe.py
RUN python /probe.py
EXPOSE 8080
CMD ["python","-m","http.server","8080","--directory","/tmp"]
