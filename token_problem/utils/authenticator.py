from django.core.exceptions import ObjectDoesNotExist

from rest_framework import exceptions, status
from rest_framework.authentication import TokenAuthentication
from django.utils.translation import gettext_lazy as _
from utils.constants import INVALID_TOKEN_MSG, INVALID_TOKEN_CODE
from app.models import Token
from utils.utility import get_timezone
from utils.constants import (
    TOKEN_EXPIRE_LIMIT,
    TOKEN_EXP_ERR_CODE,
    TOKEN_EXPIRED_MSG,
    TOKEN_DEALLOCATE_MSG,
    TOKEN_DEALLOCATE_CODE,
    TOKEN_LAST_USED,
)


class TokenNotActiveException(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _(INVALID_TOKEN_MSG)
    default_code = INVALID_TOKEN_CODE


class CustomTokenExpireException(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _(TOKEN_EXPIRED_MSG)
    default_code = TOKEN_EXP_ERR_CODE


class CustomTokenDeallocateException(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _(TOKEN_DEALLOCATE_CODE)
    default_code = TOKEN_DEALLOCATE_MSG


class CheckToken(TokenAuthentication):
    def authenticate_credentials(self, token):
        try:

            token_details = Token.objects.get(
                token=token, deleted=False, is_assigned=True
            )
            current_time = get_timezone()

            total_sec_diff_ep = token_details.expire_time - current_time
            if total_sec_diff_ep.seconds < TOKEN_EXPIRE_LIMIT:
                if token_details.last_used:
                    total_sec_diff = current_time - token_details.last_used
                    if total_sec_diff.seconds < TOKEN_EXPIRE_LIMIT:
                        setattr(token_details, "is_authenticated", True)
                        return token_details, token
                    else:

                        token_details.is_assigned = False
                        token_details.expire_time = None
                        token_details.last_used = None
                        token_details.deleted = True
                        token_details.save()

                        raise CustomTokenExpireException(TOKEN_EXPIRED_MSG)
                else:
                    setattr(token_details, "is_authenticated", True)
                    return token_details, token
            else:

                token_details.is_assigned = False
                token_details.expire_time = None
                token_details.last_used = None
                token_details.deleted = True
                token_details.save()

                raise exceptions.AuthenticationFailed(INVALID_TOKEN_MSG)

        except CustomTokenDeallocateException:
            raise CustomTokenDeallocateException(TOKEN_DEALLOCATE_MSG)

        except CustomTokenExpireException:
            raise CustomTokenExpireException(TOKEN_EXPIRED_MSG)

        except ObjectDoesNotExist as e:
            print(e)
            raise TokenNotActiveException(INVALID_TOKEN_MSG)

        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed(INVALID_TOKEN_MSG)
