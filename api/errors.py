from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.exceptions import APIException, ErrorDetail

ERROR_GROUP_DOES_NOT_EXIST = (
    "ERROR_GROUP_DOES_NOT_EXIST",
    HTTP_404_NOT_FOUND,
    "The requested group does not exist.",
)
ERROR_USER_INVALID_GROUP_PERMISSIONS = (
    "ERROR_USER_INVALID_GROUP_PERMISSIONS",
    HTTP_400_BAD_REQUEST,
    "You need {e.permissions} permissions.",
)
ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"
BAD_TOKEN_SIGNATURE = "BAD_TOKEN_SIGNATURE"
EXPIRED_TOKEN_SIGNATURE = "EXPIRED_TOKEN_SIGNATURE"
ERROR_HOSTNAME_IS_NOT_ALLOWED = (
    "ERROR_HOSTNAME_IS_NOT_ALLOWED",
    HTTP_400_BAD_REQUEST,
    "Only the hostname of the web frontend is allowed.",
)


class RequireValue(APIException):
    status_code = 400
    default_detail = '必要な値'
    default_code = 'required_value'


class ExistedValue(APIException):
    status_code = 400
    default_detail = '既存の値'
    default_code = 'existed_value'


class FormatErrorValue(APIException):
    status_code = 400
    default_detail = 'フォーマットエラー値'
    default_code = 'format_error_value'


class UserTypeError(APIException):
    status_code = 400
    default_detail = 'ユーザータイプエラー'
    default_code = 'user_type'


class DoesNotExist(APIException):
    status_code = 400
    default_detail = 'は存在しません'
    default_code = 'does_not_exist'


class MaxNumberOfItem(APIException):
    status_code = 400
    default_detail = 'アイテムの最大数'
    default_code = 'max_number_of_item'


class ParticipantUserError(APIException):
    status_code = 400
    default_detail = '参加者のユーザーエラー'
    default_code = 'participant_user_error'


class PasswordIncorrect(APIException):
    status_code = 400
    default_detail = 'パスワードが正しくありません'
    default_code = 'password_incorrect'


class UseNotActive(APIException):
    status_code = 400
    default_detail = 'ユーザーがアクティブではありません'
    default_code = 'user_not_active'


class EventTimeSelected(APIException):
    status_code = 400
    default_detail = 'イベント時間はすでに選択されています'
    default_code = 'event_time_selected'


class PermissionDenied(APIException):
    status_code = 403
    default_detail = '操作する権限がありません。'
    default_code = 'permission_denied'


class SourceSESEmailNotVerified(APIException):
    status_code = 400
    default_detail = 'Source SES Email Not Verified'
    default_code = 'source_ses_email_not_verified'


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Bad Request'
    default_code = 'bad_request'
