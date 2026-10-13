from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.documents import get_document_model
from wagtail.search import index as search_index

from wagtail_non_admin_draftail.forms import get_document_form


def get_chooser_context():
    """construct context variables needed by the chooser JS"""
    return {
        "step": "choose",
        "error_label": _("Server Error"),
        "error_message": _(
            "Report this error to your webmaster with the following information:"
        ),
    }


def get_document_result_data(document):
    """
    helper function: given a document, return the json data to pass back to the
    chooser panel
    """

    return {
        "id": document.id,
        "title": document.title,
        "url": document.url,
        "filename": document.filename,
        "edit_link": reverse("wagtaildocs:edit", args=(document.id,)),
    }


@login_required
def document_chooser(request):
    Document = get_document_model()
    DocumentForm = get_document_form(Document)
    uploadform = DocumentForm(user=request.user, prefix="document-chooser-upload")

    return render_modal_workflow(
        request,
        "wagtail_non_admin_draftail/document/upload.html",
        None,
        {
            "uploadform": uploadform,
            "is_searching": False,
        },
        json_data=get_chooser_context(),
    )


def document_chosen(request, document_id):
    document = get_object_or_404(get_document_model(), id=document_id)

    return render_modal_workflow(
        request,
        None,
        None,
        None,
        json_data={
            "step": "chosen",
            "result": get_document_result_data(document),
        },
    )


@login_required
def document_chooser_upload(request):
    Document = get_document_model()
    DocumentForm = get_document_form(Document)

    if request.method == "POST":
        document = Document(uploaded_by_user=request.user)
        form = DocumentForm(
            request.POST,
            request.FILES,
            instance=document,
            user=request.user,
            prefix="document-chooser-upload",
        )

        if form.is_valid():
            document.file_size = document.file.size

            # Set new document file hash
            document.file.seek(0)
            document._set_file_hash()
            document.file.seek(0)

            form.save()

            # Reindex the document to make sure all tags are indexed
            search_index.insert_or_update_object(document)

            return render_modal_workflow(
                request,
                None,
                None,
                None,
                json_data={
                    "step": "chosen",
                    "result": get_document_result_data(document),
                },
            )
    else:
        form = DocumentForm(user=request.user, prefix="document-chooser-upload")

    documents = Document.objects.order_by("title")

    return render_modal_workflow(
        request,
        "wagtail_non_admin_draftail/document/upload.html",
        None,
        {"documents": documents, "uploadform": form},
        json_data=get_chooser_context(),
    )
