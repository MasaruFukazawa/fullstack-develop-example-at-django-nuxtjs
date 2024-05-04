FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ワークディレクトリの作成
WORKDIR /src

# プロジェクトのファイルをコピー
COPY ./backend /src

RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install 

RUN chmod +x /src/manage.py