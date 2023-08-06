import logging
import django
from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger("cas")


def oauthLogoutUrl(request):
    """
    Generates Oauth logout URL
    :param: request RequestObj
    """
    hapHost = request.domain.auth.url
    logoutUrl = f"{hapHost}/logout"
    return logoutUrl


def get_user_group_model():
    """
        Return the UserGroup model that is active in this project.
    """
    try:
        return django_apps.get_model(
            settings.USER_GROUP_MODEL, require_ready=False
        )
    except ValueError:
        raise ImproperlyConfigured(
            "USER_GROUP_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "USER_GROUP_MODEL refers to model '%s' that has not been installed"
            % settings.USER_GROUP_MODEL
        )


if django.VERSION < (1, 11):
    def is_authenticated(user):
        return user.is_authenticated()
else:
    def is_authenticated(user):
        return user.is_authenticated
