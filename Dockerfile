FROM python:3.10

COPY requirements.txt /temp/requirements.txt

COPY MelodyMasterQuiz /MelodyMasterQuiz

WORKDIR /MelodyMasterQuiz

EXPOSE 8000

RUN pip install --no-cache-dir -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
