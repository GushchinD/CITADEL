from PIL import Image
from io import BytesIO
from shutil import copyfileobj

from app.models import recognize_profile
from app.models.lgb_predict import predict_nlp
from app.models.embedding import create_elmo, get_user_embedding_and_popular_words

from app.data.financial import FNSClient, ArbitClient, TerroristSearchClient
import vk_api

# elmo = create_elmo("196.zip")
fns_client = FNSClient()
arbit_client = ArbitClient()
terrorist_client = TerroristSearchClient()


def collect_data(image_bytes, links):
    image = Image.open(BytesIO(image_bytes))
    recognized_id = recognize_profile("+79041741968", "ezz2JA5b", image, links)

    # ПОФИГ НА КРЕДЫ
    # embedding, popular_words = get_user_embedding_and_popular_words(elmo, recognized_id, "+79041741968", "ezz2JA5b")
    # prediction = predict_nlp(embedding, "nlp_scoring.txt")
    # ПОФИГ НА КРЕДЫ 2 ДЕДЛАЙН ЧЕРЕЗ ЧАС
    vk_session = vk_api.VkApi("+79041741968", "ezz2JA5b")
    vk_session.auth()
    fio = vk_session.method('users.get', values={"user_ids": recognized_id})[0]
    first, last = fio['first_name'], fio['last_name']
    # return popular_words, prediction
    itns = fns_client.search(f'{first} {last}')
    arbits = arbit_client.search(f'{first} {last}')
    return None, None, first, last, itns, arbits
