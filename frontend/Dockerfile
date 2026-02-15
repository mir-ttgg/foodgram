FROM node:21.7.1-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build

FROM node:21.7.1-alpine
WORKDIR /app

COPY --from=builder /app/build ./build

RUN mkdir -p /app/staticfiles

CMD ["sh", "-c", "cp -r /app/build/* /app/staticfiles/ && echo 'Frontend files copied successfully' && tail -f /dev/null"]