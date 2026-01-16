# VK_project
1. Склонируйте репозиторий.
2. Установите зависимости Python:
   `pip install -r requirements.txt`
3. Убедитесь, что у вас установлен и запущен локальный MySQL-сервер.
4. Создайте пустую базу данных с именем, указанным в файле `config.json` (имя: vk_project_so).
5. Примените миграции Django для создания таблиц:
   `python manage.py migrate`
6. (Опционально) Создайте суперпользователя:
   `python manage.py createsuperuser`
7. Запустите проект:
   `python manage.py runserver`
