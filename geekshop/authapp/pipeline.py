from datetime import datetime

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile

from geekshop.authapp.models import ShopUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend != 'vk-oauth2':
        return

    api_url = f"https://api.vk.com/method/users.get?fields=bday,sex,about&access_token={response['access_token']}"

    vk_response = requests.get(api_url)

    if vk_response.status_code != 200:
        return

    vk_data = vk_response.json()['response'][0]

    if vk_data['sex']:
        if vk_data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        elif vk_data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE

    if vk_data['about']:
        user.shopuserprofile.about_me = vk_data['about']

    if vk_data['bdate']:
        b_date = datetime.strptime(vk_data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - b_date.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age


    #
    # if vk_data['photo_50']:
    #     user.shopuserprofile.photo_50 = vk_data['photo_50']

    user.save()


#
# def get_avatar(backend, response, user=None, *args, **kwargs):
#     url = None
#     if backend.name == 'vk-oauth2':
#         url = response.get('photo_50', '')
#
#     if url:
#         user.avatar = url
#         user.save()
#         print(user.avatar)
