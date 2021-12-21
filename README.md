# Приложение сохранения кадров из стрима

При запуске приложения, каждые 5 секунд в течение суток (можно изменить в файле `.env`) из стрима берется кадр и
сохраняется в формате jpg в папку media. Для просмотра сохраненных фото есть веб-приложение. По умолчанию после запуска,
веб приложение доступно по адресу http://127.0.0.1:5000/web/

### Запуск:

- Для запуска нужен только _Docker_ (_docker-compose_)

- Запуск в консоле:``docker-compose up --build``
- Остановка в консоле``docker-compose down``

### Конфигурации

Конфигурации находятся в файле .env

Параметры:

- `VIDEO_URL` - ссылка для доступа к камере
- `VIDEO_FPS` - FPS с которого считывать данные с камеры
- `RECORDING_DELAY` - Сколько в секунах считывать данные из камеры
- `IMAGE_SAVE_DELAY` - Через какой промежуток в секундах сохранять кадр из видео

### Стуктура проекта

- В папке `backend` находиться бэкенд веб-приложения. Написан на `Flask`, содержит один метод api получение списка фото в
  папке `media`.
- В папке `media` сохраняются все фото из стрима. Отсюда же берутся фото для показа в веб-приложении.
- В папке `nginx` содержатся конфигурации сервера `nginx`.
- В папке `roading` находится программа чтение видео из стрима и сохранение кадров каждые t секунд.
- В папке `web` находится фронтенд веб-приложение. Собрано из кода написанного на `react`.