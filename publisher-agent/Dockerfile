FROM node:15-alpine
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN npm install
CMD node src/DataReceiver.js