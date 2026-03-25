import asyncio
import websockets
import json
from datetime import datetime

"""
Signaling Server для WebRTC P2P соединений

Этот сервер пересылает SDP offers/answers и ICE candidates между клиентами.
После установления P2P соединения трафик идёт напрямую между браузерами.

Запуск: python weeks/week-09/starter/signaling.py
"""

# Хранилище подключений
CONNECTIONS = set()

# Счётчик подключений для логирования
connection_count = 0


async def handler(websocket):
    global connection_count
    
    connection_count += 1
    client_id = f"client-{connection_count}"
    CONNECTIONS.add(websocket)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {client_id} подключился. Всего клиентов: {len(CONNECTIONS)}")
    
    try:
        async for message in websocket:
            try:
                # Парсим JSON сообщение
                data = json.loads(message)
                msg_type = data.get('type', 'unknown')
                
                # Логируем тип сообщения
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {client_id} отправил {msg_type}")
                
                # Рассылаем сообщение всем остальным подключенным клиентам
                # В production здесь была бы логика комнат/пар
                broadcast_tasks = []
                for conn in CONNECTIONS:
                    if conn != websocket:
                        broadcast_tasks.append(conn.send(message))
                
                if broadcast_tasks:
                    await asyncio.gather(*broadcast_tasks, return_exceptions=True)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Сообщение разослано {len(broadcast_tasks)} клиентам")
                    
            except json.JSONDecodeError:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Получено не JSON сообщение: {message[:100]}")
                # Пересылаем как есть (для отладки)
                for conn in CONNECTIONS:
                    if conn != websocket:
                        await conn.send(message)
                        
    except websockets.exceptions.ConnectionClosed:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {client_id} отключился (закрыто)")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Ошибка {client_id}: {e}")
    finally:
        CONNECTIONS.remove(websocket)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {client_id} удалён из CONNECTIONS. Осталось: {len(CONNECTIONS)}")


async def main():
    host = "localhost"
    port = 8765
    
    print("=" * 50)
    print("WebRTC Signaling Server")
    print("=" * 50)
    print(f"Слушаю на: ws://{host}:{port}")
    print("")
    print("Инструкция:")
    print("1. Откройте client/index.html в двух вкладках браузера")
    print("2. В первой вкладке нажмите 'Создать предложение (Offer)'")
    print("3. Во второй вкладке нажмите 'Создать ответ (Answer)'")
    print("4. После установления соединения отправляйте сообщения")
    print("")
    print("Нажмите Ctrl+C для остановки сервера")
    print("=" * 50)
    
    async with websockets.serve(handler, host, port):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nSignaling server остановлен пользователем")
