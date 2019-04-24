import os
import cv2

import create_users
import comparing
import time
# os.chdir("C:/Institut/programs/")
os.chdir("/home/nikolay/learning/")


def main():
    print("run comparing 40-55...")
    list_probe = create_users.make("fingers/probe/crossMatchDB_55")
    print("created list of probe...")
    list_standard = create_users.make("fingers/standard/crossMatchDB")
    print("created list of standard...")

    # start_time = time.time()
    list_results = list(map(lambda probe: comparing.compare_one_with_n(probe, list_standard), list_probe))
    print(comparing.fold_results(list_results).to_string())
    # users = create_users.make("fingers/probe/crossMatchDB_mini")
    # probe = cv2.imread("database/101_2.tif", cv2.IMREAD_GRAYSCALE)
    # standard = cv2.imread("database/101_3.tif", cv2.IMREAD_GRAYSCALE)
    # comparing.compare(users[0], users[1], 40)
    # print(" {} всего сек".format((time.time() - start_time)))


if __name__ == "__main__":
    try:
        main()
    except:
        raise
