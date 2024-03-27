# Install application dependencies
FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./ /app

RUN addgroup -g 1001 -S flask
RUN adduser -S flask -u 1001
RUN chown -R flask:flask /app

USER flask

EXPOSE 8000

# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn", "-w 3", "--bind", "0.0.0.0:8000", "app:app"]