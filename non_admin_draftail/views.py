import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from wagtail.embeds import embeds
from wagtail.embeds.exceptions import EmbedNotFoundException, EmbedUnsupportedProviderException
from wagtail.embeds.finders.embedly import AccessDeniedEmbedlyException, EmbedlyException

validate_url = URLValidator(message="Please enter a valid URL")


@login_required
@require_http_methods(["POST"])
def embed_upload_view(request):
    response = None
    error = None

    data = json.loads(request.body)
    url = data["url"]

    try:
        validate_url(url)
        embed_obj = embeds.get_embed(url)
        response = {
            'embedType': embed_obj.type,
            'url': embed_obj.url,
            'providerName': embed_obj.provider_name,
            'authorName': embed_obj.author_name,
            'thumbnail': embed_obj.thumbnail_url,
            'title': embed_obj.title,
        }
    except ValidationError as e:
        error = e.message
    except AccessDeniedEmbedlyException:
        error = "There seems to be a problem with your embedly API key. Please check your settings."
    except (EmbedNotFoundException, EmbedUnsupportedProviderException):
        error = "Cannot find an embed for this URL."
    except EmbedlyException:
        error = (
            "There seems to be an error with Embedly while trying to embed this URL."
            " Please try again later."
        )
    except Exception:
        error = "Something went wrong, please try again"

    if error:
        return HttpResponse(error, status=400)

    return JsonResponse(response)
