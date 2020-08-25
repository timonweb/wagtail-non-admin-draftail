from django.urls import path

from .views.image import (
    image_select_format,
    image_upload,
)

from .views.embed import (
    embed_chooser,
    embed_chooser_upload,
)

from .views.link import (
    external_link, email_link, phone_link, anchor_link
)

app_name = "non_admin_draftail"

urlpatterns = [
    path('embed-chooser/', embed_chooser, name='embed-chooser'),
    path('embed-chooser-upload/', embed_chooser_upload, name='embed-chooser-upload'),
    path("image-upload/", image_upload, name="image-upload"),
    path("image-select-format/<int:image_id>/", image_select_format, name="image-select-format",),
    path('external-link/', external_link, name='external-link'),
    path('email-link/', email_link, name='email-link'),
    path('phone-link/', phone_link, name='phone-link'),
    path('anchor-link/', anchor_link, name='anchor-link'),

    #path('choose-page/', chooser.browse, name='wagtailadmin_choose_page'),
    #path('choose-page/<int:parent_page_id>/', chooser.browse, name='wagtailadmin_choose_page_child'),
    #path('choose-page/search/', chooser.search, name='wagtailadmin_choose_page_search'),
    #path('choose-external-link/', chooser.external_link, name='wagtailadmin_choose_page_external_link'),
    #path('choose-email-link/', chooser.email_link, name='wagtailadmin_choose_page_email_link'),
    #path('choose-phone-link/', chooser.phone_link, name='wagtailadmin_choose_page_phone_link'),
    #path('choose-anchor-link/', chooser.anchor_link, name='wagtailadmin_choose_page_anchor_link'),

]
