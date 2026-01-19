# build env
FROM node:21.7.1-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
# Сохраняем собранные файлы в /app/build для последующего использования
# и копируем в result_build для совместимости
RUN cp -r build result_build || true
CMD ["sh", "-c", "cp -r /app/build/* /app/staticfiles/ 2>/dev/null || cp -r /app/result_build/* /app/staticfiles/ 2>/dev/null || tail -f /dev/null"]
