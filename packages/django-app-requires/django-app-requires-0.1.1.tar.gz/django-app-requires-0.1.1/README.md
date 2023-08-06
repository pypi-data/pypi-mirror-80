# django-app-requires

A simple tools auto add app extra requires.

## Install

```
pip install django-app-requires
```

## Usage

1. If your django application requires extra application, then add `app_requires = ["your", "required", "apps"]` in the `app/__init__.py` file.
2. In project using your application, add belowe code to the `pro/settings.py` after `INSTALLED_APPS`.
    ```
    from django_app_requires import add_requires
    INSTALLED_APPS = add_requires(INSTALLED_APPS)
    ```


## Releases

### v0.1.1 2020/09/25

- Add fastutils & magic-import in requirements.txt.
- Fix problem of recursive required.

### v0.1.0 2020/09/23

- First release.