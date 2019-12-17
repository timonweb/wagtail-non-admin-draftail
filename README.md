# Public Draftail

Wagtail has an excellent WYSIWYG editor called Draftail. Unfortunately, the editor can be used only on admin pages. But what if you want non-admin users to be able to use it?

That is where Public Draftail comes to the rescue! This package provides a form widget that adds Draftail to a regular Django form that isn't a part of the admin interface. The only requirement is to have Wagtail installed.

# Installation

1. Install a package from PYPI: `pip install non_admin_draftail`
2. Add `non_admin_draftail` to `INSTALLED_APPS`:
    ```python
    INSTALLED_APPS = [
        ...
        'non_admin_draftail',
    ]
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
2. And a form that's used for editing that model by non-admin users:
   ```python
   from django.forms import ModelForm
   
   class JobPostForm(ModelForm):
     class Meta:
       model = JobPost
       fields = [
         "title",
         "body"
       ]       
   ```

You can now add `Draftail` editor to non-admin form via assigning a `NonAdminDraftailRichTextArea`
widget to `body` field:

```python
from django.forms import ModelForm
from non_admin_draftail.widgets import NonAdminDraftailRichTextArea

class JobPostForm(ModelForm):
 class Meta:
   model = JobPost
   fields = [
     "title",
     "body"
   ]
   widgets = {
     "body": NonAdminDraftailRichTextArea()
   }
```

Now, when you visit a page with a `JobPostForm` form, you should see
the body field with `Draftail` editor enabled.

# Contributors
[Tim Kamanin - A Full Stack Python / JavaScript Developer](https://timonweb.com)