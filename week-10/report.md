# Отчет по Docker

## Размер образа
- Исходный образ (python:3.11): ~1.2 ГБ
- Оптимизированный образ (python:3.11-slim): ~150 МБ

## Количество слоёв
Каждый слой в Dockerfile создаёт новый слой образа:
1. Базовый образ builder (python:3.11)
2. WORKDIR /app
3. COPY requirements.txt
4. RUN pip install (установка зависимостей)
5. Базовый образ runtime (python:3.11-slim)
6. WORKDIR /app
7. COPY --from=builder (копирование установленных пакетов)
8. COPY . . (копирование приложения)
9. EXPOSE 8266
10. CMD (команда запуска)

Итого: 10 слоёв в финальном образе.

## Команды сборки и запуска
```bash
docker build -t week10-app .
docker run -p 8266:8266 week10-app
```
