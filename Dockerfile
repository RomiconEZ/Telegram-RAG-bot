FROM python:3.10

ENV PYTHONPATH=/srv \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/

COPY requirements.txt /srv/
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

COPY . /srv/

CMD ["python3.10", "src/app.py"]
