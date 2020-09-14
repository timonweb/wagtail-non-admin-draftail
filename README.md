# Non-admin Draftail

Wagtail has an excellent WYSIWYG editor called Draftail. Unfortunately, the editor can be used only on admin pages. But what if you want to use it on non-admin pages, like Django form view pages?

This is where Non-admin Draftail comes to the rescue! The package provides all the necessary magic to free Draftail from Wagtail admin and make it usable with a regular Django form that doesn't belong to the CMS admin interface. The only requirement is, of course, to have Wagtail installed.

# Installation

1. Install a package from PYPI: `pip install non_admin_draftail`
2. Add `non_admin_draftail` to `INSTALLED_APPS`:
    ```python
    INSTALLED_APPS = [
        ...
        'non_admin_draftail',
    ]
    ```
3. Add
    ```python
    path("non-admin-draftail/", include("non_admin_draftail.urls", namespace="non_admin_draftail")),
    ```
    to the main `urls.py` of the project
4. Include `"non_admin_draftail/draftail_media.html"` in the `<head>` of every page that will have the editor.
There are many ways to do this. I like doing this the following way:

    a. Add `{% block non_admin_draftail_head %}` block to the `<head>` of your `base.html` file:

    ```html
    {% load non_admin_draftail_tags %}
    <!DOCTYPE html>
    <html>
    <head>
     ...
     {% block non_admin_draftail_head %}{% endblock non_admin_draftail_head %}
    </head>
    <body></body>
    </html>
    ```

    b. Then add `non_admin_draftail/draftail_media.html` to `non_admin_draftail_head` block on
    every page that uses the editor.

    For example, we have a page template `post_edit.html` that renders a form
    with the editor, so we need to add the following block to that template:
    ```
    {% block non_admin_draftail_head %}
      {% include "non_admin_draftail/draftail_media.html" %}
      {{ form.media }} # add this line if your template doesn't use "{{ form }}" but fields by themselves
    {% endblock non_admin_draftail_head %}
    ```
    And that's it, Draftail editor should now have all JS/CSS to boot up on the page.

# Configuration

By default, all images and documents uploaded via non-admin draftail are saved in Wagtail's Images/Documents library in the "Public uploads" collection. You can customize the name of the collection by defining a `NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME` variable in your main Django `settings.py` file:

```
NON_ADMIN_DRAFTAIL_PUBLIC_COLLECTION_NAME = "Visitor uploads"
```

# Usage
Given:

1. You have a model that has a Wagtail `RichTextField`:
    ```python
    from django.db import models
    from wagtail.core.fields import RichTextField

    class JobPost(models.Model):
      title = models.CharField(max_length=255)
      body = RichTextField()
    ```

2. Ensure that `job_post_form.html` (or whatever template is responsible for rendering Job post edit form) includes `draftail_media.html` in the `<head>` of the page (See step 4 of the Installation instructions above).

3. Now, when you visit a page with a `JobPostForm` form, you should see
the body field with `Draftail` editor enabled.

# Contributors
[Tim Kamanin - A Full Stack Python / JavaScript Developer](https://timonweb.com)
