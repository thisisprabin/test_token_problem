RESPONSE_DATA_LIST = {
    "code": None,
    "message": None,
    "data": None,
    "total": 0,
    "error_type": None,
}
RESPONSE_DATA_OBJ = {"code": None, "message": None, "data": None, "error_type": None}

INVALID_TOKEN_MSG = "Invalid token"
INVALID_TOKEN_CODE = "invalid_token"

COMMON_SUCCESS_MSG = "Success."
DATA_FETCHED_SUCCESS_MSG = "Data fetched successfully."
NO_DATA_FOUND = "No data found."

COMMON_SERVER_ERROR = "Something went wrong. Please try again later."

TOKEN_COUNT = 10
TOKEN_EXPIRE_LIMIT = 300  # In seconds
TOKEN_LAST_USED = 60  # In seconds

TOKEN_GENERATE_SUCCESS_MSG = "Token generated successfully."
TOKEN_EXP_ERR_CODE = "token_expired"
TOKEN_EXPIRED_MSG = "Token expired."
TOKEN_DEALLOCATE_CODE = "token_deallocated"

TOKEN_DEALLOCATE_MSG = "This token is deallocated successfully."
TOKEN_DEALLOCATE_NOT_FOUND = "Requested token is already deallocated."
TOKEN_NOT_FOUND = "Token not found."
TOKEN_DEL_SUCCESS_MSG = "Token deleted successfully."

NO_TOKEN_ASS_ERR = "No token found for assignment."
TOKEN_ASS_SUCCESS = "Token assigned successfully."

KEEP_ALIVE_SUCCESS = "This token will alive for next {} seconds.".format(TOKEN_LAST_USED)
