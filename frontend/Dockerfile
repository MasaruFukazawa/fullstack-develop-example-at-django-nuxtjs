FROM node:21

WORKDIR /src

# プロジェクトのファイルをコピー
COPY ./frontend /src

RUN cd fullstack-develop-example-at-django-nuxtjs && \
npm install -g npm@latest && \
npm install