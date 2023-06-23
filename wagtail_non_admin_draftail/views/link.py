from django.contrib.auth.decorators import login_required
from wagtail.admin.forms.choosers import (
    AnchorLinkChooserForm,
    EmailLinkChooserForm,
    ExternalLinkChooserForm,
    PhoneLinkChooserForm,
)
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.admin.views.chooser import shared_context


@login_required
def external_link(request):
    initial_data = {
        "url": request.GET.get("link_url", ""),
        "link_text": request.GET.get("link_text", ""),
    }

    if request.method == "POST":
        form = ExternalLinkChooserForm(
            request.POST, initial=initial_data, prefix="external-link-chooser"
        )

        if form.is_valid():
            result = {
                "url": form.cleaned_data["url"],
                "title": form.cleaned_data["link_text"].strip()
                or form.cleaned_data["url"],
                # If the user has explicitly entered / edited something in the link_text field,
                # always use that text. If not, we should favour keeping the existing link/selection
                # text, where applicable.
                # (Normally this will match the link_text passed in the URL here anyhow,
                # but that won't account for non-text content such as images.)
                "prefer_this_title_as_link_text": ("link_text" in form.changed_data),
            }

            return render_modal_workflow(
                request,
                None,
                None,
                None,
                json_data={"step": "external_link_chosen", "result": result},
            )
    else:
        form = ExternalLinkChooserForm(
            initial=initial_data, prefix="external-link-chooser"
        )

    return render_modal_workflow(
        request,
        "wagtail_non_admin_draftail/link/external_link.html",
        None,
        shared_context(
            request,
            {
                "form": form,
            },
        ),
        json_data={"step": "external_link"},
    )


@login_required
def email_link(request):
    initial_data = {
        "link_text": request.GET.get("link_text", ""),
        "email_address": request.GET.get("link_url", ""),
    }

    if request.method == "POST":
        form = EmailLinkChooserForm(
            request.POST, initial=initial_data, prefix="email-link-chooser"
        )

        if form.is_valid():
            result = {
                "url": "mailto:" + form.cleaned_data["email_address"],
                "title": form.cleaned_data["link_text"].strip()
                or form.cleaned_data["email_address"],
                # If the user has explicitly entered / edited something in the link_text field,
                # always use that text. If not, we should favour keeping the existing link/selection
                # text, where applicable.
                "prefer_this_title_as_link_text": ("link_text" in form.changed_data),
            }
            return render_modal_workflow(
                request,
                None,
                None,
                None,
                json_data={"step": "external_link_chosen", "result": result},
            )
    else:
        form = EmailLinkChooserForm(initial=initial_data, prefix="email-link-chooser")

    return render_modal_workflow(
        request,
        "wagtail_non_admin_draftail/link/email_link.html",
        None,
        shared_context(
            request,
            {
                "form": form,
            },
        ),
        json_data={"step": "email_link"},
    )


@login_required
def phone_link(request):
    initial_data = {
        "link_text": request.GET.get("link_text", ""),
        "phone_number": request.GET.get("link_url", ""),
    }

    if request.method == "POST":
        form = PhoneLinkChooserForm(
            request.POST, initial=initial_data, prefix="phone-link-chooser"
        )

        if form.is_valid():
            result = {
                "url": "tel:" + form.cleaned_data["phone_number"],
                "title": form.cleaned_data["link_text"].strip()
                or form.cleaned_data["phone_number"],
                # If the user has explicitly entered / edited something in the link_text field,
                # always use that text. If not, we should favour keeping the existing link/selection
                # text, where applicable.
                "prefer_this_title_as_link_text": ("link_text" in form.changed_data),
            }
            return render_modal_workflow(
                request,
                None,
                None,
                None,
                json_data={"step": "external_link_chosen", "result": result},
            )
    else:
        form = PhoneLinkChooserForm(initial=initial_data, prefix="phone-link-chooser")

    return render_modal_workflow(
        request,
        "wagtail_non_admin_draftail/link/phone_link.html",
        None,
        shared_context(
            request,
            {
                "form": form,
            },
        ),
        json_data={"step": "phone_link"},
    )


@login_required
def anchor_link(request):
    initial_data = {
        "link_text": request.GET.get("link_text", ""),
        "url": request.GET.get("link_url", ""),
    }

    if request.method == "POST":
        form = AnchorLinkChooserForm(
            request.POST, initial=initial_data, prefix="anchor-link-chooser"
        )

        if form.is_valid():
            result = {
                "url": "#" + form.cleaned_data["url"],
                "title": form.cleaned_data["link_text"].strip()
                or form.cleaned_data["url"],
                "prefer_this_title_as_link_text": ("link_text" in form.changed_data),
            }
            return render_modal_workflow(
                request,
                None,
                None,
                None,
                json_data={"step": "external_link_chosen", "result": result},
            )
    else:
        form = AnchorLinkChooserForm(initial=initial_data, prefix="anchor-link-chooser")

    return render_modal_workflow(
        request,
        "wagtail_non_admin_draftail/link/anchor_link.html",
        None,
        shared_context(
            request,
            {
                "form": form,
            },
        ),
        json_data={"step": "anchor_link"},
    )
