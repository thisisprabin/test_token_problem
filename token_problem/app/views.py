import jwt
import time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app.serializers import TokenSerializer
from utils.utility import (
    get_expire_token_time,
    get_timezone,
    validate_uuid4,
)
from utils.constants import (
    TOKEN_COUNT,
    TOKEN_GENERATE_SUCCESS_MSG,
    RESPONSE_DATA_LIST,
    RESPONSE_DATA_OBJ,
    TOKEN_ASS_SUCCESS,
    NO_TOKEN_ASS_ERR,
    TOKEN_LAST_USED,
    INVALID_TOKEN_MSG,
    INVALID_TOKEN_CODE,
    KEEP_ALIVE_SUCCESS,
    NO_DATA_FOUND,
    COMMON_SERVER_ERROR,
    TOKEN_DEALLOCATE_MSG,
    TOKEN_DEALLOCATE_NOT_FOUND,
    TOKEN_NOT_FOUND,
    TOKEN_DEL_SUCCESS_MSG,
)
from app.models import Token
from utils.authenticator import CheckToken


# Create your views here.


class GenerateToken(APIView):
    def get(self, request):

        response_data = RESPONSE_DATA_OBJ.copy()
        try:

            _obj_list = []
            for i in range(TOKEN_COUNT):
                _obj_list.append(
                    Token(
                        **{
                            "token": (
                                jwt.encode(
                                    {"some": str(time.time())},
                                    "secret",
                                    algorithm="HS256",
                                )
                            ).decode("utf-8"),
                        }
                    )
                )

            Token.objects.bulk_create(_obj_list)

            response_data.update(
                {"code": status.HTTP_200_OK, "message": TOKEN_GENERATE_SUCCESS_MSG}
            )
            response = Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            response_data.update(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": COMMON_SERVER_ERROR,
                }
            )
            response = Response(
                response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class TokenList(APIView):
    def get(self, request):

        response_data = RESPONSE_DATA_LIST.copy()
        try:

            _info = []
            se_data = TokenSerializer(Token.objects.filter(deleted=False), many=True)
            _info = se_data.data

            if len(_info):
                response_data.update(
                    {
                        "code": status.HTTP_200_OK,
                        "message": TOKEN_GENERATE_SUCCESS_MSG,
                        "data": _info,
                        "total": len(_info),
                    }
                )
                response = Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data.update(
                    {
                        "code": status.HTTP_404_NOT_FOUND,
                        "message": NO_DATA_FOUND,
                        "data": _info,
                        "total": len(_info),
                    }
                )
                response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response_data.update(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": COMMON_SERVER_ERROR,
                }
            )
            response = Response(
                response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class AssignToken(APIView):
    def get(self, request):

        response_data = RESPONSE_DATA_OBJ.copy()

        try:
            token = Token.objects.filter(is_assigned=False, deleted=False)
            if token.exists():
                token = token[0]
                token.expire_time = get_expire_token_time(created_time=get_timezone())
                token.is_assigned = True
                token.save()

                _info = {"id": token.id, "token": token.token}

                response_data.update(
                    {
                        "code": status.HTTP_200_OK,
                        "message": TOKEN_ASS_SUCCESS,
                        "data": _info,
                    }
                )
                response = Response(response_data, status=status.HTTP_200_OK)

            else:
                response_data.update(
                    {"code": status.HTTP_404_NOT_FOUND, "message": NO_TOKEN_ASS_ERR}
                )
                response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response_data.update(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": COMMON_SERVER_ERROR,
                }
            )
            response = Response(
                response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class KeepAlive(APIView):

    authentication_classes = [CheckToken]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        response_data = RESPONSE_DATA_OBJ.copy()

        try:

            token = request.user
            if token.last_used:

                current_time = get_timezone()
                time_diff = current_time - token.last_used

                if time_diff.seconds < TOKEN_LAST_USED:
                    token.last_used = get_timezone()
                    token.save()
                    response_data.update(
                        {"code": status.HTTP_200_OK, "message": KEEP_ALIVE_SUCCESS}
                    )
                    response = Response(response_data, status=status.HTTP_200_OK)
                else:
                    token.is_assigned = False
                    token.expire_time = None
                    token.last_used = None
                    token.save()

                    response_data.update(
                        {
                            "code": status.HTTP_401_UNAUTHORIZED,
                            "message": INVALID_TOKEN_MSG,
                            "error_type": INVALID_TOKEN_CODE,
                        }
                    )
                    response = Response(
                        response_data, status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                token.last_used = get_timezone()
                token.save()
                response_data.update(
                    {"code": status.HTTP_200_OK, "message": TOKEN_ASS_SUCCESS}
                )
                response = Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            response_data.update(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": COMMON_SERVER_ERROR,
                }
            )
            response = Response(
                response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class DeallocateToken(APIView):
    def get(self, request, pk):
        response_data = RESPONSE_DATA_OBJ.copy()

        try:

            if validate_uuid4(uuid_string=pk):

                token_data = Token.objects.filter(pk=pk, deleted=False)
                if token_data.exists():
                    token_data = token_data[0]
                    if token_data.is_assigned:
                        token_data.is_assigned = False
                        token_data.expire_time = None
                        token_data.last_used = None
                        token_data.save()

                        response_data.update(
                            {
                                "code": status.HTTP_200_OK,
                                "message": TOKEN_DEALLOCATE_MSG,
                            }
                        )
                        response = Response(response_data, status=status.HTTP_200_OK)

                    else:
                        response_data.update(
                            {
                                "code": status.HTTP_200_OK,
                                "message": TOKEN_DEALLOCATE_NOT_FOUND,
                            }
                        )
                        response = Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data.update(
                        {"code": status.HTTP_404_NOT_FOUND, "message": TOKEN_NOT_FOUND}
                    )
                    response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
            else:
                response_data.update(
                    {"code": status.HTTP_404_NOT_FOUND, "message": TOKEN_NOT_FOUND}
                )
                response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response_data.update(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": COMMON_SERVER_ERROR,
                }
            )
            response = Response(
                response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class DeleteToken(APIView):
    def delete(self, request, pk):

        response_data = RESPONSE_DATA_OBJ.copy()
        try:
            if validate_uuid4(uuid_string=pk):
                token_data = Token.objects.filter(pk=pk, deleted=False)
                if token_data.exists():
                    token_data = token_data[0]
                    token_data.is_assigned = False
                    token_data.expire_time = None
                    token_data.last_used = None
                    token_data.deleted = True
                    token_data.save()

                    response_data.update(
                        {"code": status.HTTP_200_OK, "message": TOKEN_DEL_SUCCESS_MSG}
                    )
                    response = Response(response_data, status=status.HTTP_200_OK)

                else:
                    response_data.update(
                        {"code": status.HTTP_404_NOT_FOUND, "message": TOKEN_NOT_FOUND}
                    )
                    response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
            else:
                response_data.update(
                    {"code": status.HTTP_404_NOT_FOUND, "message": TOKEN_NOT_FOUND}
                )
                response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response_data.update(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": COMMON_SERVER_ERROR,
                }
            )
            response = Response(
                response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response
