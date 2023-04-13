# Установка через Докер


Относительно свежая версия Ирины доступна в виде Docker-образа (для linux/amd64) и может быть запущена
следующей командой (linux/arm64 пока не поддерживается, т.к. не умею делать target на мультиплатформу):

```shell
docker run -it --publish 5003:5003 \
  janvarev/ireneva:latest
```

Далее можно открыть [https://localhost:5003/webapi_client/](https://localhost:5003/webapi_client/) (или аналогичный адрес на том хосте, где был
запущен контейнер) и, разрешив использование самоподписанного сертификата, использовать Ирину через веб-интерфейс.

(Если что, автор не специалист в Докер, поэтому могут быть глюки при работе.)

В Докер-образе в качестве TTS работает silero_v3.

Кроме того:
- по адресу [https://localhost:5003/webapi_client/](https://localhost:5003/webapi_client/) располагается клиент, который производит распознавание STT в браузере (браузерная версия VOSK, тяжелая)
- по адресу [https://localhost:5003/mic_client/](https://localhost:5003/mic_client/) располагается клиент, который посылает информацию с микрофона на сервер, для серверного распознавания речи в потоковом режиме. Он более легкий для браузера, но в нем чуть меньше настроек, и плохо отрабатывает дисконнект.

#### Доступ к опциям в Докере

Чтобы получить доступ к опциям, подмонтируйте папку options (при первом запуске будут созданы все файлы options, которые можно будет редактировать)
```shell
 docker run -it --publish 5003:5003 \
 -v "C:/temp/temp_irene_docker/options:/home/python/irene/options" \
 janvarev/ireneva:latest
```
или для Linux
```shell
 docker run -it --publish 5003:5003 \
 -v "$HOME/irene_options:/home/python/irene/options" \
 janvarev/ireneva:latest
```

Чтобы получить доступ к плагинам, подмонтируйте также папку plugins
```shell
 docker run -it --publish 5003:5003 \
 -v "$HOME/irene_options:/home/python/irene/options" \
 -v "$HOME/irene_plugins:/home/python/irene/plugins" \
 janvarev/ireneva:latest
```
НО! 
1. Положите в эту папку все дефолтовые плагины из plugins Git Ирины. Иначе не запустится - просто плагинов не будет. 
2. Положите туда же плагин silero_v3 из plugins_inactive.
3. Рекомендуется туда же положить core.py из docker_plugins для корректного подключения дефолтовых настроек.
