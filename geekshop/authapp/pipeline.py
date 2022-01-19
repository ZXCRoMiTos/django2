import requests
from geekshop.settings import BASE_DIR
import os


def save_user_profile(backend, user, response, *args, **kwargs):
    
    if backend.name == "google-oauth2":
        if 'email' in response.keys():
            user.email = response['email']

        if 'picture' in response.keys():
            avatar_name = f'{user.username}avatar.jpg'
            path_for_avatar = os.path.join(BASE_DIR, f'media/avatars/{avatar_name}')
            img_data = requests.get(response['picture']).content
            with open(path_for_avatar, 'wb+') as handler:
                handler.write(img_data)
            user.avatar = f'avatars/{avatar_name}'

        user.save()

