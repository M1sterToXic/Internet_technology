# Architecture of invoices-s13

## Обзор системы
Проект **invoices-s13** представляет собой систему управления счетами (invoices). Она спроектирована по микросервисной архитектуре для обеспечения масштабируемости и независимого развертывания.

## Компоненты системы
1. **Invoices Service (invoices-svc-s13)**: Основной сервис для работы со счетами. Позволяет создавать, просматривать и отслеживать суммы (`amount`).
2. **Gateway**: Единая точка входа, обеспечивающая REST API и маршрутизацию запросов к внутреннему gRPC сервису.

## Схема взаимодействия
- **External Client** -> [HTTP/REST] -> **API Gateway** (/api/invoices) -> **Invoices Service**
- **Internal Communication** -> [gRPC] -> Используется для взаимодействия между Gateway и Invoices Service (InvoicesService).

## Технологический стек
- **Языки**: Python
- **Протоколы**: REST (FastAPI) для внешних вызовов, gRPC для межсервисного взаимодействия.
- **Инфраструктура**: Docker, Docker-Compose, Kubernetes (invoices-app).
