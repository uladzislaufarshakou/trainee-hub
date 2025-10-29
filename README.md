# Trainee Hub

> **Статус: 🚧 В разработке (Status: in progress) 🚧**

Проект "Система Менторства", построенный в соответствии с принципами **Чистой/Луковой Архитектуры** (Clean/Onion Architecture) для обеспечения максимальной тестируемости, гибкости и изоляции бизнес-логики от инфраструктурных "деталей".

---

## 🧅 Архитектура

Проект строго следует **Правилу Зависимостей (Dependency Rule)**: зависимости направлены _только внутрь_.

1.  **Core** (Ядро): Бизнес-сущности и правила. Ни от чего не зависит.
2.  **Application** (Логика): Сценарии использования (Use Cases) и абстракции (Порты). Зависит только от `Core`.
3.  **Infrastructure** (Инструменты): Базы данных, API-клиенты (Адаптеры). Зависит от `Application` и `Core`.
4.  **Presentation** (Вход): API (FastAPI), CLI. Зависит от `Application` и `Core`.

---

## ✅ Что Готово (Completed)

На данный момент "внутренние" слои (Ядро и Логика) определены и синхронизированы.

### 1. 🧅 Ядро (Core Layer)

Этот слой полностью определен и стабилизирован.

- `[x]` **`core.domain`**:
  - Определены все Бизнес-Сущности (Pydantic-модели, `frozen=True`).
  - Включает: `User`, `TraineeTechnologyState`, `LearningSessionLog` и др.
  - Определены все Бизнес-Правила (Enums).
  - Включает: `Role`, `LearningState`, `ReviewState` и др.
- `[x]` **`core.exceptions`**:
  - Определена полная иерархия доменных исключений.
  - Включает: `DomainError`, `NotFoundError`, `BusinessRuleError`, `LearningSessionAlreadyInProgressError` и др.
  - Настроены `__init__.py` для чистого импорта (`from src.core.exceptions import ...`).

### 2. 🧠 Слой Приложения (Application Layer)

Этот слой определяет всю бизнес-логику и контракты.

- `[x]` **`application.repositories` (Порты)**:
  - Определены все _интерфейсы_ (абстрактные классы) для репозиториев.
  - Включает: `ITraineeTechnologyStateRepository`, `ILearningSessionLogRepository`, `IUserRepository` и др.
  - Интерфейсы прошли аудит и синхронизированы с бизнес-логикой.
  - Настроены `__init__.py` для чистого импорта (`from src.application.repositories import ...`).
- `[x]` **`application.services` (Сценарии Использования)**:
  - Реализован первый "вертикальный срез" логики: **`TraineeService`**.
  - `TraineeService` управляет логикой стажера (старт/стоп сессии), зависит _только_ от абстракций (`I...Repository`) и `core`.
- `[x]` **`application.dto` (Контракты Данных)**:
  - Определены базовые DTO для передачи данных между `presentation` и `application` слоями.

---

## 🗺️ Дорожная Карта (To-Do Roadmap)

Следующие шаги включают реализацию "внешних" слоев (Инфраструктура и Представление) и расширение логики.

### 3. 💾 Слой Инфраструктуры (Infrastructure Layer)

- `[ ]` **3.1. Реализация Репозиториев (Адаптеры)**:
  - Создать `src/infrastructure/persistence/sqlalchemy/repositories/`
  - `[ ]` `SQLAlchemyTraineeTechnologyStateRepository(ITraineeTechnologyStateRepository)`
  - `[ ]` `SQLAlchemyLearningSessionLogRepository(ILearningSessionLogRepository)`
  - `[ ]` (и т.д. для всех остальных интерфейсов)
- `[ ]` **3.2. Модели БД (SQLAlchemy)**:
  - Создать `src/infrastructure/persistence/sqlalchemy/models/`
  - `[ ]` Определить все таблицы SQLAlchemy (`DeclarativeBase`), которые маппятся на доменные модели `core.domain`.
  - `[ ]` Настроить `Alembic` для миграций.
- `[ ]` **3.3. Unit of Work (UoW)**:
  - `[ ]` Реализовать паттерн Unit of Work (`src/infrastructure/persistence/sqlalchemy/uow.py`) для управления сессиями и обеспечения атомарности транзакций (например, в `TraineeService`, где нужно обновить `State` _и_ создать `Log`).

### 4. 🌐 Слой Представления (Presentation Layer)

- `[ ]` **4.1. Эндпоинты API (FastAPI)**:
  - Создать `src/presentation/api/v1/endpoints/`
  - `[ ]` `trainee.py`: Реализовать роутеры (`@router.post(...)`) для `TraineeService` (например, `POST /technologies/{id}/start`).
  - `[ ]` `mentor.py`: Реализовать роутеры для `MentorService`.
- `[ ]` **4.2. Обработка Исключений (Exception Handlers)**:
  - `[ ]` Настроить в `FastAPI` обработчики, которые будут ловить доменные исключения (`core.exceptions`) и преобразовывать их в корректные HTTP-ответы (404, 409, 400).

### 5. 🧩 Сборка (Composition Root)

- `[ ]` **5.1. Dependency Injection (DI)**:
  - Создать `src/presentation/api/dependencies.py` (или использовать встроенный `FastAPI.Depends`).
  - `[ ]` "Склеить" приложение: научить DI-контейнер "понимать", что когда сервис просит `ITraineeTechnologyStateRepository`, ему нужно предоставить `SQLAlchemyTraineeTechnologyStateRepository`.
- `[ ]` **5.2. `main.py`**:
  - `[ ]` Создать точку входа для запуска `uvicorn`.

### 6. 📈 Расширение (Application Layer Expansion)

- `[ ]` **6.1. `MentorService`**:
  - `[ ]` Написать `MentorService` для логики ревью (approve/reject).
- `[ ]` **6.2. `UserService` / `AuthService`**:
  - `[ ]` Написать сервисы для управления пользователями и аутентификацией.

---

## 🚀 Установка и Запуск (Setup and Run)

```shell
# 1. Clone repository
git clone https://github.com/uladzislaufarshakou/trainee-hub.git

# 2. Create venv
uv venv .venv

# 3. Install dependencies
uv sync
```

Run isn't ready yet.
