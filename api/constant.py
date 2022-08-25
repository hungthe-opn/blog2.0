from datetime import timedelta

#  EMPLOYEE EVENT TIME SCHEDULE OPTION
USER_RANK_Lv1 = 'Thành viên mới'
USER_RANK_Lv2 = 'Người dùng'
USER_RANK_Lv3 = 'Tác giả'
USER_RANK_Lv4 = 'Fan cứng'
USER_RANK_Lv5 = 'Người có tầm ảnh hưởng'
USER_RANK_Lv6 = 'Chuyên gia bình luận'
USER_RANK_Lv7 = 'Quản trị viên'
USER_RANK_OPTION = (
    (USER_RANK_Lv1, USER_RANK_Lv1),
    (USER_RANK_Lv2, USER_RANK_Lv2),
    (USER_RANK_Lv3, USER_RANK_Lv3),
    (USER_RANK_Lv4, USER_RANK_Lv4),
    (USER_RANK_Lv5, USER_RANK_Lv5),
    (USER_RANK_Lv6, USER_RANK_Lv6),
    (USER_RANK_Lv7, USER_RANK_Lv7),
)
# USER_RANK_OPTION = {
#     USER_RANK_Lv1: USER_RANK_Lv1,
#     USER_RANK_Lv2: USER_RANK_Lv2,
#     USER_RANK_Lv3: USER_RANK_Lv3,
#     USER_RANK_Lv4: USER_RANK_Lv4,
#     USER_RANK_Lv5: USER_RANK_Lv5,
#     USER_RANK_Lv6: USER_RANK_Lv6,
#     USER_RANK_Lv7: USER_RANK_Lv7,
# }
# SEX USER
USER_SEX_NEW = ''
USER_SEX_MALE = 'Nam'
USER_SEX_FEMALE = 'Nữ'
USER_SEX_ORTHER = 'Khác'
USER_SEX_SECRET = 'Bí mật'
USER_SEX_OPTION = (
    (USER_SEX_MALE, USER_SEX_MALE),
    (USER_SEX_FEMALE, USER_SEX_FEMALE),
    (USER_SEX_ORTHER, USER_SEX_ORTHER),
    (USER_SEX_SECRET, USER_SEX_SECRET),
    (USER_SEX_NEW, USER_SEX_NEW),
)
DEFAULT_USER_DATA = [
    'id',
    'email',
    'image',
    'first_name',
    'about',
    'user_name',
    'password'
]

