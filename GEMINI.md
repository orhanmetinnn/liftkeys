# LiftKeys Project

## Project Overview
LiftKeys is a B2B e-commerce and CRM platform for elevator/lift components built with Django 5.2 and Wagtail 7.1. It supports 7 languages (Turkish, English, Arabic, Russian, French, German, Spanish), with Turkish as the default.

The entire business logic, Wagtail pages, and custom models reside in a single Django app named `crm/`.

### Key Technologies
- **Backend**: Django 5.2
- **CMS**: Wagtail 7.1
- **Database**: MySQL 8.0 (development fallback to SQLite)
- **Frontend**: Bootstrap 5, crispy-forms
- **Translations**: Django i18n, django-modeltranslation, wagtail-localize

## Building and Running

### Development Server
```bash
python manage.py runserver
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Translations Workflow
```bash
# Extract strings for a locale (e.g., Turkish)
python manage.py makemessages -l tr

# Compile .po files to .mo
python manage.py compilemessages
```

### Tests
```bash
python manage.py test crm
```

## Development Conventions

- **App Structure:** All models, views, forms, and Wagtail pages are located in the `crm/` directory. Continue using `crm/` for business logic rather than creating secondary apps.
- **Authentication:** The custom user model (`crm.CustomUser`) uses **email** as the login identifier, not username. Employee-only views are protected with the `@employee_required` decorator.
- **Translations:** Three translation layers work together:
  1. Django i18n for UI strings.
  2. `django-modeltranslation` for per-language DB columns (`crm/translation.py`).
  3. `wagtail-localize` for Wagtail CMS page content.
- **Routing:** All URLs are i18n-prefixed (e.g., `/tr/`, `/en/`). The root path detects the browser language and redirects appropriately.
- **Security Warning:** The repository contains hardcoded secrets like `SECRET_KEY` and MySQL credentials in `settings.py`, and AWS credentials in standalone scripts. **Do not log, print, or commit these credentials.**
