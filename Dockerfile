FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords
RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]