#Retrieve 3.9 python version
FROM python:3.9

#Create code directory in docker container
WORKDIR /code

#Define environment variables
ARG APP_PORT=5000

#Copy all project files and directories in docker container
COPY ./ai /code/ai
COPY ./ai/pickle /code/ai/pickle
COPY ./entities /code/entities
COPY ./entities/data /code/entities/data
COPY ./entities/models /code/entities/models
COPY ./repositories /code/repositories
COPY ./routes /code/routes
COPY ./services /code/services
COPY ./.env /code/.env
COPY ./app.py /code/app.py
COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

#Download poetry package manager
#RUN pip install --user poetry
RUN pip install poetry

#Applying suggested change to fix poetry installation
#ENV PATH="${PATH}:/root/.local/bin"

#Install project dependencies
RUN poetry install

#Define application running port
EXPOSE $APP_PORT

#Lauch app after container is instanciated
CMD ["poetry", "run", "flask", "run"]