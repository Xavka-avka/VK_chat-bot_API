import vk_api
import requests
import adds
import utils
from io import BytesIO
from PIL import Image
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint
from vk_api.upload import VkUpload


def main():
    vk_session = vk_api.VkApi(token=adds.token_vk_bot)
    session_api = vk_session.get_api()
    upload_session = VkUpload(session_api)
    longpoll = VkBotLongPoll(vk_session, adds.group_id)
    print('='*30)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            ct = event.message.text.lower()
            content = str(ct).split(" ")
            user_id = event.message.from_id
            peer_id = event.message.peer_id
            if content[0][0] == '/':
                user_profile = session_api.users.get(user_ids=user_id)[0]
                user_first_name, user_last_name = user_profile['first_name'], user_profile['last_name']
                print(f'{user_first_name} {user_last_name} написал(а): {ct}\n' + '=' * 30)
                if content[0][1:] == 'help':
                    session_api.messages.send(peer_id=peer_id, message=adds.f_help, random_id=0)
                elif content[0][1:] == 'привет':
                    session_api.messages.send(peer_id=peer_id, message='Привет!', random_id=0)
                elif content[0][1:] == 'пока':
                    session_api.messages.send(peer_id=peer_id, message='Пока!', random_id=0)
                elif content[0][1:] == 'кубик':
                    number = randint(1, 6)
                    upload_result = upload_session.photo_messages(photos=f'dices/{number}.png')
                    picture = f"photo{upload_result[0]['owner_id']}_{upload_result[0]['id']}"
                    session_api.messages.send(peer_id=peer_id, message=f'Вам выпало {number}!',
                                              attachment=picture, random_id=0)
                elif content[0][1:] == 'погода':
                    geolocation = requests.get(
                        'https://api.ipgeolocation.io/ipgeo',
                        params=adds.g_api_params
                    ).json()
                    print(geolocation['latitude'], geolocation['longitude'])
                    weather = requests.get(
                        'https://api.weather.yandex.ru/v2/informers?',
                        headers=adds.y_api_headers,
                        params={'lat': 53.19171, 'lon': 50.19091, 'lang': 'ru_RU'}
                    ).json()
                    answer = f'Погода для Russia, Samara' \
                             f'\nТемпература: {weather["fact"]["temp"]}°C' \
                             f'\nОщущается как: {weather["fact"]["feels_like"]}°C' \
                             f'\nСкорость ветра: {weather["fact"]["wind_speed"]} м/с'
                    session_api.messages.send(peer_id=peer_id, message=answer, random_id=0)
                elif content[0][1:] == 'сундуки':
                    profile = requests.get(f'{adds.cr_link}/players/%23{content[1].upper()}',
                                           headers=adds.cr_header).json()
                    if len(profile["name"]) > 9:
                        session_api.messages.send(peer_id=peer_id, message='Ты слабый', random_id=0)
                        continue
                    upcoming_chests = requests.get(f'{adds.cr_link}/players/%23{content[1].upper()}/upcomingchests',
                                                   headers=adds.cr_header).json()
                    result = Image.open('cr/back1.jpg', 'r')
                    result.thumbnail((500, 500))
                    index = 0
                    for i in (10, 130, 260, 390):
                        utils.add_chest(
                            utils.get_chests()[upcoming_chests['items'][index]['name']],
                            i, 150, result, index+1)
                        index += 1
                    for i in (10, 130, 260, 390):
                        utils.add_chest(
                            utils.get_chests()[upcoming_chests['items'][index]['name']],
                            i, 300, result, index+1)
                        index += 1
                    utils.add_text(f'Следующие сундуки\n\nдля игрока',
                                   result, (60, 30), (255, 255, 255))
                    size_w, size_h = utils.add_text(profile['name'],
                                                    result, (280, 84), (246, 100, 175))
                    utils.add_text(':',
                                   result, (280 + size_w, 81), (255, 255, 255))
                    fp = BytesIO()
                    result.save(fp, format='PNG')
                    fp.seek(0)
                    upload_result = upload_session.photo_messages(photos=fp)  # type: ignore
                    picture = f"photo{upload_result[0]['owner_id']}_{upload_result[0]['id']}"
                    session_api.messages.send(peer_id=peer_id, attachment=picture, random_id=0)
            else:
                print(f'{user_id} написал(а): {ct}\n' + '=' * 30)
                session_api.messages.send(peer_id=peer_id, message="Список всех команд: /help", random_id=0)


if __name__ == '__main__':
    main()
