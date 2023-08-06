import requests


def buscar_avatar(usuario):
    """
    Busca o avatar de um usuário no link do github
    :param usuario: str com o nome do usuário do github
    :return: str com link do avatar no github
    """
    url = f'https://api.github.com/users/{usuario}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('GetulioCastro'))
