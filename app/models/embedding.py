import vk_api
import re
from . import rus_preprocessing_udpipe
from importlib import reload
import pandas as pd
import numpy as np

from stop_words import get_stop_words

from simple_elmo import ElmoModel

def get_user_embedding_and_popular_words(model, user_id, vk_login, vk_password):
    USED_POSTS_NUM = 1
    used_groups_limit = 10
    
    user_embed, popular_groups_words = build_embeddings(user_id, vk_login, vk_password, model, used_groups_limit, used_posts_num=USED_POSTS_NUM)
    return user_embed, popular_groups_words


def get_groups_text(user_id, used_groups_limit, used_posts_num, vk_session):
    groups = get_user_groups(user_id, vk_session)
    groups_text, popular_words = get_groups_posts_text(groups, used_groups_limit, used_posts_num, vk_session)
    return groups_text, popular_words


def get_user_groups(user_id, vk_session):
    return vk_session.method("groups.get", values={"user_id": user_id})["items"]


def get_groups_posts_text(groups, used_groups_limit, used_posts_num, vk_session):
    #     global groups_texts
    groups_texts = _raw_groups_texts(groups, used_groups_limit, used_posts_num, vk_session)
    russian_texts, popular_words = extract_russian_words(groups_texts)

    return russian_texts, popular_words


def _raw_groups_texts(groups, used_groups_limit, used_posts_num, vk_session):
    groups_texts = []

    for idx, group in enumerate(groups[:used_groups_limit]):
        try:
            group_wall = vk_session.method("wall.get", values={"owner_id": -group})
            posts_texts = get_wall_texts(group_wall, used_posts_num)
            posts_texts = " ".join(posts_texts)
            groups_texts.append(posts_texts)

        except vk_api.ApiError:
            print("Приватный паблик")

    return groups_texts


def extract_russian_words(groups_texts):
    stop_words = get_stop_words("ru")

    #     concatenated_texts = " ".join(groups_texts)
    russian_texts = keep_russian_letters(groups_texts)

    for idx, text in enumerate(russian_texts):
        filtered_words = [word for word in text.split() if word not in stop_words]
        filtered_russian_text = " ".join(filtered_words)
        russian_texts[idx] = filtered_russian_text

    popular_words = get_popular_words(russian_texts)

    russian_texts = rus_preprocessing_udpipe.run(russian_texts)
    return russian_texts, popular_words


def get_wall_texts(wall, limit):
    posts = wall["items"]
    posts_texts = []
    for post in posts[:limit]:
        posts_texts.append(post["text"])

    return posts_texts


def keep_russian_letters(texts):
    russian_letters = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    for idx, text in enumerate(texts):
        russian_text = "".join(re.findall(f"[{russian_letters}\s]", text))
        russian_text = re.sub("\s", " ", russian_text)
        texts[idx] = russian_text

    return texts


def get_popular_words(texts):
    concatenated_texts = " ".join(texts)
    groups_words = pd.Series(concatenated_texts.split())
    counts = groups_words.value_counts().head(50)
    return counts[counts.index.str.len() > 3]


def build_embeddings(user_id, vk_login, vk_password, elmo_model, used_groups_limit, used_posts_num, words_num_thr=100):
    vk_session = vk_api.VkApi(vk_login, vk_password)
    vk_session.auth()
    try:
        groups_texts, popular_groups_words = get_groups_text(user_id, used_groups_limit, used_posts_num, vk_session)
        
        for idx, text in enumerate(groups_texts):
            text = " ".join(text.split()[:words_num_thr])
            groups_texts[idx] = text
            
        print("text", groups_texts[0])

        groups_embedding = np.zeros(1024)
        step = 10

        for text_start_idx in range(0, len(groups_texts), step):
            text_end_idx = text_start_idx + step
            embeddings = elmo_model.get_elmo_vector_average(groups_texts[text_start_idx: text_end_idx])
            mean_embedding = embeddings.mean(axis=0)
            groups_embedding += mean_embedding
            del embeddings, mean_embedding

        groups_embedding /= ((len(groups_texts) + step - 1) // step)

        return groups_embedding, popular_groups_words
    
    except Exception as e:
        print(e)
        return None, None


def create_elmo(zipfile_path, batch=5):
    model = ElmoModel()
    model.load(zipfile_path, max_batch_size=batch)
    return model