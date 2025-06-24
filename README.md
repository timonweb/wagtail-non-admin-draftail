# Non-admin Draftail

Wagtail has an excellent WYSIWYG editor called Draftail. Unfortunately, the editor can only be used on admin pages. But what if you want to use it on non-admin pages, such as Django form view pages?

This is where Non-admin Draftail comes to the rescue! The package provides all the necessary magic to set Draftail free from Wagtail admin and make it usable with a regular Django form that doesn't belong to the CMS admin interface. The only requirement is, of course, to have Wagtail installed.

# Compatibility
The current version of the package is compatible with Wagtail v7+.

# Installation
1. Install the package from PyPI: `pip install wagtail_non_admin_draftail`
2. Add `wagtail_non_admin_draftail` to `INSTALLED_APPS`:
    ```python
    INSTALLED_APPS = [
        ...
        'wagtail_non_admin_draftail',
    ]
    ```
3. Add the following line to the main `urls.py` of the project:
    ```python
    path("non-admin-draftail/", include("wagtail_non_admin_draftail.urls", namespace="wagtail_non_admin_draftail")),
    ```
4. Include `"wagtail_non_admin_draftail/draftail_media.html"` in the `<head>` of every page that will have the editor.
   There are many ways to do this. Here is one way to accomplish it:

    a. Add the `{% block wagtail_non_admin_draftail_head %}` block to the `<head>` of your `base.html` file:

    ```html
    {% load wagtail_non_admin_draftail_tags %}
    <!DOCTYPE html>
    <html>
    <head>
     ...
     {% block wagtail_non_admin_draftail_head %}{% endblock wagtail_non_admin_draftail_head %}
    </head>
    <body>
    </body>
    </html>
    ```

    b. Then add `wagtail_non_admin_draftail/draftail_media.html` to the `wagtail_non_admin_draftail_head` block on every page that uses the editor.

    For example, if you have a page template called `post_edit.html` that renders a form with the editor, add the following block to that template:
    ```django
    {% block wagtail_non_admin_draftail_head %}
      {% include "wagtail_non_admin_draftail/draftail_media.html" %}
      {{ form.media }}  {# Add this line if your template doesn't use "{{ form }}" but renders fields individually #}
    {% endblock wagtail_non_admin_draftail_head %}
    ```
    That's it! The Draftail editor should now have all the JS/CSS required to boot up on the page.

5. Use `NonAdminDraftailRichTextArea` as the widget for your form field to enable Draftail on non-admin pages:
    ```python
    from wagtail_non_admin_draftail.widgets import NonAdminDraftailRichTextArea

    class NoteForm(forms.ModelForm):
        class Meta:
            model = Note
            fields = ["text"]
            widgets = {"text": NonAdminDraftailRichTextArea}
    ```

# Configuration

By default, all images and documents uploaded via Non-admin Draftail are saved in Wagtail's Images/Documents library, in the "Public uploads" collection. You can customize the name of the collection by defining the `WAGTAIL_NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME` variable in your main Django `settings.py` file:

```
WAGTAIL_NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME = "Visitor uploads"
```

# Usage
Assuming the following steps:

1. You have a model that has a Wagtail `RichTextField`:
    ```python
    from django.db import models
    from wagtail.fields import RichTextField

    class JobPost(models.Model):
      title = models.CharField(max_length=255)
      body = RichTextField()
    ```

2. Ensure that `job_post_form.html` (or whatever template is responsible for rendering the Job post edit form) includes `draftail_media.html` in the `<head>` of the page (see step 4 of the Installation instructions above).

3. Now, when you visit a page with a `JobPostForm` form, you should see the body field with the Draftail editor enabled.

# Contributing

## How to run the example project locally
To contribute, you may want to run the local project. Here is how to do it:

1. This project uses [Poetry](https://python-poetry.org/) for packaging and dependency management (if you have Poetry installed, skip this step):
    ```
    pip install poetry
    ```

2. Clone the repo:
    ```
    git clone https://github.com/timonweb/wagtail-non-admin-draftail.git
    ```

3. Change into the cloned directory:
    ```
    cd wagtail-non-admin-draftail
    ```

4. Install dependencies with Poetry:
    ```
    poetry install
    ```

5. Run the project with Poetry:
    ```
    poetry run python manage.py runserver
    ```

6. Open your browser and go to the test form page: [http://127.0.0.1:8000/example/form/](http://127.0.0.1:8000/example/form/)

## How to run the test suite
Assuming you have completed steps 1–4 above, you can run the `pytest` test suite with the following command:
```
poetry run pytest
```

If tests fail and the installation is fresh, make sure that Playwright (the end-to-end test library used) is installed. Run the following command to install it:

```
poetry run python -m playwright install chromium
```

# Created by
[Tim Kamanin - A Full Stack Python / JavaScript Developer](https://timonweb.com)
