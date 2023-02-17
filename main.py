import requests
import re
from multiprocessing import Pool
import pdb

def send_req(item):
    check = item[4].post('https://hh.ru/applicant/vacancy_response/popup', data={"incomplete": False, "vacancy_id":int(item[0]), "resume_hash": f"{item[1]}","ignore_postponed": True, "_xsrf":f"{item[2]}", "letter": f"{item[3]}", "lux": True, "withoutTest": "no", "hhtmFromLabel": "undefined", "hhtmSourceLabel": "undefined"})

    print(check.status_code, item[0])
    if check.status_code != 200:
        if check.json()['error' ] == 'negotiations-limit-exceeded':
            return False


if __name__ == "__main__":
    n = 0
    req = requests.Session()

    """
    Привет! Чтобы скрипт заработал надо заполнить несколько полей, иначе HH не пустит запросы

    Введи сюда сво куки. Важно быть залогиненым на HH. Проще всего это сделав скопировав все как HAR . Дальше нас инетерсует все что после 'Cookie:' до следующего поля с ':' (это может быть 'X-hhtmFrom:') или что-то другое. Главное забрать все после кук
    """
    cookies = "Вставь сюда свои куки"

    if cookies != "Вставь сюда свои куки":
        raise Exception("Ты забыл вставить сюда свои куки")

    req.headers = {"Host": "hh.ru", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15", "Cookie": f"""{cookies}"""}

    """Здесь нам нужно вставить хеш резюме. Оно находиться в разделе https://hh.ru/applicant/resumes . Дальше ты должен перейти в одно из своих резюме и скопировать хеш после ссылки . Как пример https://hh.ru/resume/71010d6fff099f0ef20039ed1f497978653133 . Тут нам нужно забрать 71010d6fff099f0ef20039ed1f497978653133 и вставить в поле ниже"""

    resume_hash = "71010d6fff099f0ef20039ed1f497978653133"

    if resume_hash != "71010d6fff099f0ef20039ed1f497978653133":
        raise Exception("Ты забыл вставить сюда своё резюме")

    xsrf_token = re.search("_xsrf=(.*?);", cookies).group(1)

    """Ниже вставляем свое письмо. Советую сделать его максимально обобщенным. Больше об этом в мое треде https://twitter.com/ns0000000001/status/1612456900993650688?s=52&t=X3kUKCZQjFDJbTbg9aQWbw """

    letter = "Вставь сюда свое письмо"

    if letter != "Вставь сюда свое письмо":
        raise Exception("Ты забыл вставить сюда своё письмо")

    """Дальще переходи на страницу HH и в поиске вбиваем то, что вам интересно. После нажимает Enter и копируем ссыку на которую вас перебросило. Пример который получается при вводе 'автоматизация python': https://hh.ru/search/vacancy?text=автоматизация+python&salary=&schedule=remote&ored_clusters=true&enable_snippets=true"""

    search_link = "Вставь сюда свой поисковый запрос"

    if search_link != "Вставь сюда свой поисковый запрос":
        raise Exception("Ты забыл вставить сюда свой запрос")

    pool = Pool(processes=70)

    """Важно, что HH позволяет в день откликаться только на 200 вакансий. Поэтому, как только скрипт получит ошибку о привышения лимита, он автоматически отключиться. Если ты все сделал правильно, то ты будешь видеть в консоли такие записи

    400 76870753
    200 76613497

    400 и 200 статусы это ок. Если ты видишь только 403 или 404 проверь, правильно ли ты вставил куки
    """

    while True:
        data = req.get(f"{search_link}&page={n}").text
        links = re.findall('https://hh.ru/vacancy/(\d*)?', data, re.DOTALL)
        send_dict = []
        for link in links:
            send_dict.append((link, resume_hash, xsrf_token, letter, req))
        if links == []:
            break
        check = pool.map(send_req, send_dict)
        if False in check:
            break
        n += 1
    pool.close()
    pool.join()