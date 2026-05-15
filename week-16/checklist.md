# Security Checklist for sessions-s13

- [x] **A01:2021-Broken Access Control**: Проверка прав доступа пользователя к сессиям других пользователей.
- [x] **A02:2021-Cryptographic Failures**: Использование HTTPS и хэширование чувствительных данных.
- [x] **A03:2021-Injection**: Использование параметризованных запросов (ORM) для предотвращения SQLi.
- [x] **A04:2021-Insecure Design**: Наличие механизмов ограничения попыток входа (Rate Limiting).
- [x] **A05:2021-Security Misconfiguration**: Отключение отладочных режимов в продакшене.
- [x] **A06:2021-Vulnerable and Outdated Components**: Регулярное обновление зависимостей (pip list --outdated).
- [x] **A07:2021-Identification and Authentication Failures**: Политика сложности паролей и сессионных токенов.
- [x] **A08:2021-Software and Data Integrity Failures**: Проверка целостности передаваемых данных.
- [x] **A09:2021-Security Logging and Monitoring Failures**: Логирование событий безопасности (логин, смена пароля).
- [x] **A10:2021-Server-Side Request Forgery (SSRF)**: Валидация URL-адресов, запрашиваемых сервером.
