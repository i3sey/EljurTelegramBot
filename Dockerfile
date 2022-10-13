FROM python:3.10.7-buster
RUN git clone https://github.com/i3sey/EljurTelegramBot /Seishun
WORKDIR /Seishun
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
CMD ["python3", "run.py"]