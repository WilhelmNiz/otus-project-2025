# Проект: Frontend-тестирование веб-приложения OpenCart и Backend-тестирование API Restful-Booker

Ответственный: Данил Нижеборцев (wilhelmkindly@gmail.com)

## Содержание
1. [Обзор проекта](#обзор-проекта)
2. [Предварительные требования](#предварительные-требования)
3. [Установка и настройка](#установка-и-настройка)
4. [Запуск инфраструктуры](#запуск-инфраструктуры)
5. [Запуск тестов](#запуск-тестов)
6. [Мониторинг и управление](#мониторинг-и-управление)
7. [Важные файлы проекта](#важные-файлы-проекта)

## Обзор проекта

Проект включает автоматизированное тестирование:
- **Frontend**: Веб-приложение OpenCart
- **Backend**: API Restful-Booker

Инфраструктура разворачивается в Docker и включает:
- **Selenoid** для запуска браузеров в контейнерах
- **Jenkins** для непрерывной интеграции
- **OpenCart** для тестирования фронтенда

## Предварительные требования

Перед началом убедитесь, что установлены:
- **Docker** (версия 20.10.0 или выше)
- **Docker Compose** (версия 2.0.0 или выше)
- **Git** (для клонирования репозитория)
- **Python 3.8+** (для запуска тестов)

Проверьте установку Docker:
```bash
    docker --version
    docker-compose --version
```
## Установка и настройка
### Клонируйте репозиторий:

```bash
    git clone https://github.com/WilhelmNiz/otus-project-2025.git
    cd otus-project-2025
    git checkout Otus_project_2025
```
### Установите зависимости Python:

```bash
    pip install -r requirements.txt
```
### Настройте окружение:

Убедитесь, что порты 4444, 8080, 8081 свободны.

Для Windows/Mac: убедитесь, что Docker Desktop запущен.

## Запуск инфраструктуры
💡 **Важно**: Запускайте сервисы в указанном порядке.

### 1. Запуск Selenoid
Selenoid обеспечивает запуск браузеров в Docker-контейнерах .

```bash
    cd infrastructure/testing-infra
    docker-compose up -d
```
Проверьте запуск:

```bash
  docker ps -a 
```
Откройте Selenoid UI: http://localhost/

## 2. Запуск Jenkins
Jenkins используется для CI/CD .

```bash
    cd infrastructure/ci-cd
    docker-compose up -d
```
Дождитесь инициализации (1-2 минуты). Получите пароль администратора:

```bash
    docker logs jenkins 2>&1 | grep -A 2 -B 2 "password"
```

Откройте Jenkins: http://localhost:8081

## 3. Запуск OpenCart


``` bash
    cd infrastructure/opencart
    docker-compose up -d
```
Дождитесь инициализации (1-2 минуты). Проверьте логи:


``` bash
    docker-compose logs opencart
```
Откройте:

OpenCart: http://localhost:8081

Админ-панель: http://localhost:8081/administration

## Запуск тестов
Тесты расположены:

**Frontend:** frontend/tests/test_opencart.py

**Backend:** backend/tests/test_auth.py, backend/tests/test_booking.py

Запуск фронтенд-тестов
Для тестов OpenCart используйте Selenoid :

```bash
  python -m pytest --browser chrome frontend/tests/test_opencart.py
```
Запуск бэкенд-тестов

Для тестов Restful-Booker :


```bash
    python -m pytest --browser chrome backend/tests/test_auth.py
    python -m pytest --browser chrome backend/tests/test_booking.py
```
Запуск всех тестов
```bash
  python -m pytest --browser chrome frontend/tests/ backend/tests/
```
## Мониторинг и управление
### Selenoid UI
URL: http://localhost

Назначение: мониторинг запущенных браузеров, просмотр сессий и логинов .

### Jenkins
URL: http://localhost:8080

Назначение: настройка пайплайнов, отслеживание сборок и результатов тестов .

### OpenCart
URL: http://localhost:8081

Админ-панель: http://localhost:8081/administration

Учетные данные: заданы в infrastructure/opencart/docker-compose.yml .

## Важные файлы проекта
**infrastructure/testing-infra/docker-compose.yml** - конфигурация Selenoid

**infrastructure/ci-cd/docker-compose.yml** - конфигурация Jenkins

**infrastructure/opencart/docker-compose.yml** - конфигурация OpenCart

**frontend/tests/test_opencart.py** - тесты OpenCart

**backend/tests/test_auth.py** - тесты аутентификации Restful-Booker

**backend/tests/test_booking.py** - тесты бронирования Restful-Booker

