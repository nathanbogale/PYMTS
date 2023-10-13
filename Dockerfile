FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

#FROM python:3.10

#COPY --from=build . .

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
