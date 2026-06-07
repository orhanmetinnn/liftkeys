# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**LiftKeys** is a Django 5.2 + Wagtail 7.1 B2B e-commerce and CRM platform for elevator/lift components, supporting 6 languages (Turkish, English, Arabic, Russian, French, German). The default language is Turkish.

## Commands

```bash
# Development server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Translation workflow
python manage.py makemessages -l tr   # extract strings for a locale
python manage.py compilemessages       # compile .po → .mo

# Automated translation (via AWS Translate)
python manage.py wagtail_translate    # Wagtail CMS pages
python manage.py category_translate   # product categories
python manage.py product_translate    # product records

# Tests
python manage.py test crm

# Static files (production)
python manage.py collectstatic
```

## Architecture

### App Structure

The entire business logic lives in a single Django app: **`crm/`**. There is no secondary app — Wagtail's pages and Django's custom models all coexist in `crm/`.

| File | Purpose |
|---|---|
| `crm/models.py` | All data models (~1000 lines, 20+ models) |
| `crm/views.py` | All views (~75k lines) |
| `crm/forms.py` | All forms (~41k lines, 20+ form classes) |
| `crm/urls.py` | 89 URL patterns |
| `crm/translation.py` | modeltranslation field declarations |
| `crm/wagtail_pages.py` | Wagtail page model definitions |
| `crm/context_processors.py` | Global template context (cart count, language flags, etc.) |

Settings live at `liftkeys/settings.py` (not the app-level default location). The `manage.py` in the repo root points there.

### Authentication & Roles

- Custom user model (`crm.CustomUser`) uses **email** as the login identifier, not username.
- Two roles: `employee` and `customer`. Employee-only views are protected with a custom `@employee_required` decorator defined in `crm/views.py`.
- Sessions last 30 days and renew on each request.

### URL Design

All URLs are i18n-prefixed (e.g., `/tr/`, `/en/`, `/ar/`). Root `/` detects browser language and redirects. Key namespaces:

- `/admin/` → Django admin  
- `/cms/` → Wagtail admin  
- `/rosetta/` → .po file editor (in-browser translation)  
- `/api/` → Simple DRF endpoints (companies, products, employees, gallery)  
- `/offers/`, `/cart/`, `/orders/` → E-commerce flow  
- `/companies/manage/`, `/directorycompany/` → CRM/company management

### Multi-Language Strategy

Three translation layers work together:

1. **Django i18n** (`locale/` .po files): UI strings — run `makemessages` / `compilemessages`.
2. **modeltranslation** (`crm/translation.py`): Adds per-language DB columns to models (e.g., `name_tr`, `name_en`). After adding a new `TranslationOptions` class, run `makemigrations`.
3. **Wagtail Localize** (`wagtail-localize`): CMS page translations synced through the Wagtail admin.

AWS Translate is used for batch automated translation via the management commands and the standalone scripts `dilceviri.py` (for .po files) and `translate_blogs.py`.

### Key Domain Models

```
CustomUser ──── Employee (HR profile, image cropping)
                JobInfo / Department / WorkLocation / TitlePersonel

Company ──────── Opportunity ──── Offer ──── OfferProduct (line items)
                DirectoryCompany (leads/contacts)

Category (hierarchical, parent/child)
  └── Product ── ProductMarketImage (multiple images)
               ── ProductQuestion / ProductQuestionOption / ProductAnswer
               ── Option (specs/variants)

Order ──── OrderItem (stores question answers as JSON)
CartItem (session-based, anonymous or authenticated)

Wagtail pages: SiteRoot → HomePage / ProductPage / BlogIndexPage / BlogPage / GalleryItem
```

Products support multi-currency pricing: TRY, USD, EUR, GBP, SAR, AED, EGP, QAR, KWD.

### Database

MySQL 8.0, `utf8mb4` charset, strict mode. Development also includes a `db.sqlite3` fallback, but MySQL is the target.

### Static & Media

- `static/` + `crm/static/` → source assets (CSS, JS, images, fonts)  
- `staticfiles/` → `collectstatic` output (production)  
- `media/` → user uploads (product images, employee photos, category images)

### Logging

All logs go to `logs/django.log` (WARNING level minimum) and console. The log file is git-ignored except for tracking changes (it appears in git status as modified).

## Important Notes

- The `settings.py` contains a hardcoded `SECRET_KEY` and MySQL credentials. Do not commit changes that expose these.
- AWS credentials are referenced in `dilceviri.py` and `translate_blogs.py` — these scripts are not imported by the app; they are standalone batch tools.
- There is no CI/CD pipeline. Deployment is manual to an AWS EC2 instance (`3.75.82.93`).
- `ALLOWED_HOSTS` in settings includes `liftkeys.com`, `www.liftkeys.com`, `3.75.82.93`, and `localhost`.
