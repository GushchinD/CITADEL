# TODO below is for mock only

from random import choice
from .account_recognition import recognize_profile, AccountFinder, AccountRecognizer
from .embedding import get_user_embedding_and_popular_words, create_elmo
from .lgb_predict import predict_nlp


#def get_matched_image(target, images):
#    return choice(images)
