FROM python:3
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD ./src /code
WORKDIR /code

# Run container as user `randyjp` with UID `1000`, which should match
# current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' randyjp && \
    chown -R randyjp:randyjp /code
USER randyjp

#EXPOSE 5000
CMD ["python", "app.py"]