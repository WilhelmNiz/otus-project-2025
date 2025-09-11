#!/bin/bash

# Параметры Xvfb для максимальной совместимости
Xvfb :99 -screen 0 $XVFB_WHD -ac +extension RANDR +extension GLX +render -noreset >/dev/null 2>&1 &

# Ожидание инициализации дисплея с таймаутом
for i in {1..10}; do
  if xdpyinfo -display :99 >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
done

# Настройки для Chrome
export CHROME_HEADLESS=1
export CHROME_HEADLESS_WIDTH=1920
export CHROME_HEADLESS_HEIGHT=1080
export QT_X11_NO_MITSHM=1
export _X11_NO_MITSHM=1
export _MITSHM=0

# Настройки для Firefox
export MOZ_HEADLESS=1
export MOZ_HEADLESS_WIDTH=1920
export MOZ_HEADLESS_HEIGHT=1080


# Запуск тестов с дополнительными флагами для стабильности
exec "$@"