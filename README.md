# AutoPremium — интернет-магазин автомобилей (Django)

Практическая работа по МДК 03.02 «Разработка кода информационных ресурсов».

## Структура

- `rootshop/` — Django-проект
- `shop/` — приложение
  - `templates/base.html` — базовый шаблон
  - `templates/includes/header.html` — шапка сайта
  - `templates/includes/footer.html` — подвал сайта
  - `templates/main.html`, `catalog.html`, `about.html` — страницы (наследуют base.html)
  - `static/shop/css/styles.css` — единый файл стилей
  - `static/shop/js/script.js` — JavaScript

## Запуск

```bash
cd rootshop
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install django
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

## Что сделано в рефакторинге

1. Весь CSS вынесен в `static/shop/css/styles.css`
2. JS вынесен в `static/shop/js/script.js`
3. Создан базовый шаблон `base.html`
4. Header и footer вынесены в includes и подключены в base.html
5. Страницы наследуют base.html через `{% extends %}` — структура не дублируется
6. Ссылки используют `{% url %}`
