from os import listdir
import cv2
from user import User
from comparing import get_descriptors


def create_user(file_name, image):
    name_without_type = file_name.split(".")[0]
    arr_name = list(map(int, name_without_type.split("_")))
    if len(arr_name) == 3:
        user = User(arr_name[0], arr_name[1], arr_name[2], get_descriptors(image))
        print("user {} created". format(user.user_id))
        return user
    else:
        return User(arr_name[0], 0, arr_name[1], get_descriptors(image))


def make(path):
    file_names = listdir(path)
    return list(map(lambda f: create_user(f, cv2.imread(path + "/" + f, cv2.IMREAD_GRAYSCALE)), file_names))
