import face_recognition # зависим от dlib!!
import PIL
import vk_api

import requests
from io import BytesIO

import numpy as np


def recognize_profile(vk_login, vk_password, recognized_image: PIL.Image, 
                 potential_links, mode="RGB", n_photo_download=5):
    """Функция, чтобы не импортировать ручками 2 класса"""
    recognizer = AccountRecognizer()
    acc_finder = AccountFinder(recognizer, vk_login, vk_password, recognized_image, potential_links)
    
    recognized_id = acc_finder.get_recognized_profile()
    return recognized_id

class AccountFinder:
    def __init__(self, recognizer, vk_login, vk_password, recognized_image: PIL.Image, 
                 potential_links, mode="RGB", n_photo_download=5):
        
        self.recognizer = recognizer
        self.recognized_image = recognized_image.convert(mode)
        self.potential_links = potential_links
        
        self.vk_session = vk_api.VkApi(vk_login, vk_password)
        self.vk_session.auth()
        self.n_photo_download = n_photo_download
        
    def get_recognized_profile(self):
        self.ids = self._ids_from_links(self.potential_links)
        user_photos_dict = self._download_photos(self.ids)
        best_match_id = self.recognizer.match_id(self.recognized_image, user_photos_dict)
        return best_match_id
        
        
    def _ids_from_links(self, links):
        ids = []
        for link in links:
            id_of_link = self._get_id(link)
            ids.append(id_of_link)
        return ids
            
    def _get_id(self, link):
        if "id" in link:
            next2ids_idx = link.index("id") + 2
            string_id = link[next2ids_idx:]
            id_of_link = int(string_id)
        else:
            screen_name = link.split("/")[-1]
            id_of_link = self.vk_session.method("utils.resolveScreenName", values={"screen_name": screen_name})["object_id"]
        return id_of_link
    
    def _download_photos(self, ids):
        users_photos_dict = {}
        for user_id in ids:
            user_photos = self._user_images(user_id)
            users_photos_dict[user_id] = user_photos
        return users_photos_dict
            
    def _user_images(self, user_id):
        photos_response = self.vk_session.method("photos.get", values={"owner_id": user_id, "album_id": "profile"})
        urls = []
        for idx, photo_dict in enumerate(photos_response["items"]):
            if idx >= self.n_photo_download - 1:
                break
            largest_size_dict = photo_dict["sizes"][-1] # largest photo
            photo_url = largest_size_dict["url"]
            urls.append(photo_url)
            
        photos = self._download_images(urls)
        return photos
    
    def _download_images(self, urls):
        images = []
        for image_url in urls:
            response = requests.get(image_url)
            img = PIL.Image.open(BytesIO(response.content))
            images.append(img)
        return images
    
    
class AccountRecognizer:
    def match_id(self, unknown_img, user_image_dict):
        max_comp_value = 0
        best_user = None
        
        for user, images in user_image_dict.items():
            #print("user, images", user, images)
            face_encodings = self.encode_images(images)
            comp_value = self.mean_comparing_value(face_encodings, unknown_img)
            print("comp_value", comp_value)
            if comp_value > max_comp_value:
                max_comp_value = comp_value
                best_user = user
                
        return best_user
    
    def encode_images(self, images):
        face_encodings = []
        for img in images:
            img = np.array(img)
            img_encoding = face_recognition.face_encodings(img)
            if len(img_encoding):
                face_encodings.append(img_encoding[0])
            
        return face_encodings
    
    def mean_comparing_value(self, face_encodings, unknown_img):
        unknown_encoding = face_recognition.face_encodings(np.array(unknown_img))[0]
        compare_results = face_recognition.compare_faces(face_encodings, unknown_encoding)
        #print("compare_results", compare_results)
        if len(compare_results):    
            return sum(compare_results) / len(compare_results) # mean for bool
        else:
            return 0