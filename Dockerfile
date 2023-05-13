FROM python:3.9
WORKDIR /DreamJane
COPY requirements.txt /DreamJane/
RUN pip install -r requirements.txt
COPY . /DreamJane
CMD python main.py
