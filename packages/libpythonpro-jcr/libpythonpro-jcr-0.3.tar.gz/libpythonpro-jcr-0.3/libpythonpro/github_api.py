import requests


def buscar_avatar(usuario):
    '''
    Busca o avatar de um usuário no Github
    :param usuario: str busca o nome de um usuário no Github
    :return:str com o link do avatar
    '''
    url = 'https://api.github.com/users/{}'.format(usuario)
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('julianocramos'))
