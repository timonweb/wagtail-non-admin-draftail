from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.models import popular_tags_for_model
from wagtail.images import get_image_model
from wagtail.images.formats import get_image_format
from wagtail.images.forms import ImageInsertionForm
from wagtail.images.permissions import permission_policy

from wagtail_non_admin_draftail.forms import get_image_form


def get_chooser_js_data():
    """construct context variables needed by the chooser JS"""
    return {
        "step": "choose",
        "error_label": _("Server Error"),
        "error_message": _(
            "Report this error to your webmaster with the following information:"
        ),
        "tag_autocomplete_url": reverse("wagtailadmin_tag_autocomplete"),
    }


def get_chooser_context(request):
    """Helper function to return common template context variables for the main chooser view"""

    collections = permission_policy.collections_user_has_permission_for(
        request.user, "choose"
    )
    if len(collections) < 2:
        collections = None

    return {
        "searchform": SearchForm(),
        "is_searching": False,
        "query_string": None,
        "will_select_format": request.GET.get("select_format"),
        "popular_tags": popular_tags_for_model(get_image_model()),
        "collections": collections,
    }


@login_required
def image_chooser_and_upload(request):
    from wagtail.search import index as search_index

    Image = get_image_model()
    ImageForm = get_image_form(Image)

    if request.method == "POST":
        image = Image(uploaded_by_user=request.user)
        form = ImageForm(
            request.POST,
            request.FILES,
            instance=image,
            user=request.user,
            prefix="image-chooser-upload",
        )

        if form.is_valid():
            # Set image file size
            image.file_size = image.file.size

            # Set image file hash
            image.file.seek(0)
            image._set_file_hash()
            image.file.seek(0)

            form.save()

            # Reindex the image to make sure all tags are indexed
            search_index.insert_or_update_object(image)

            if request.GET.get("select_format"):
                form = ImageInsertionForm(
                    initial={"alt_text": image.default_alt_text},
                    prefix="image-chooser-insertion",
                )
                return render_modal_workflow(
                    request,
                    "wagtail_non_admin_draftail/image/select_format.html",
                    None,
                    {"image": image, "form": form},
                    json_data={"step": "select_format"},
                )
            else:
                # not specifying a format; return the image details now
                return render_modal_workflow(
                    request,
                    None,
                    None,
                    None,
                    json_data={
                        "step": "chosen",
                        # "result": get_image_result_data(image),
                    },
                )
    else:
        form = ImageForm(user=request.user, prefix="image-chooser-upload")

    context = get_chooser_context(request)
    context.update({"uploadform": form})
    return render_modal_workflow(
        request,
        "wagtail_non_admin_draftail/image/upload.html",
        None,
        context,
        json_data=get_chooser_js_data(),
    )


@login_required
def image_select_format(request, image_id):
    image = get_object_or_404(get_image_model(), id=image_id)

    if request.method == "POST":
        form = ImageInsertionForm(
            request.POST,
            initial={"alt_text": image.default_alt_text},
            prefix="image-chooser-insertion",
        )
        if form.is_valid():
            format = get_image_format(form.cleaned_data["format"])
            preview_image = image.get_rendition(format.filter_spec)

            image_data = {
                "id": image.id,
                "title": image.title,
                "format": format.name,
                "alt": form.cleaned_data["alt_text"],
                "class": format.classnames,
                "edit_link": reverse("wagtailimages:edit", args=(image.id,)),
                "preview": {
                    "url": preview_image.url,
                    "width": preview_image.width,
                    "height": preview_image.height,
                },
                "html": format.image_to_editor_html(
                    image, form.cleaned_data["alt_text"]
                ),
            }

            return render_modal_workflow(
                request,
                None,
                None,
                None,
                json_data={"step": "chosen", "result": image_data},
            )
    else:
        initial = {"alt_text": image.default_alt_text}
        initial.update(request.GET.dict())
        form = ImageInsertionForm(initial=initial, prefix="image-chooser-insertion")

    return render_modal_workflow(
        request,
        "wagtail_non_admin_draftail/image/select_format.html",
        None,
        {"image": image, "form": form},
        json_data={"step": "select_format"},
    )
