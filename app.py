import os
import cv2

import create_users
import comparing

# os.chdir("C:/Institut/programs/fingerprint-Kjanko")
os.chdir("/home/nikolay/learning/fingerprint-Kjanko")


def main():
    print("run comparing...")
    list_probe = create_users.make("../fingers/probe/crossMatchDB")
    print("created list of probe...")
    list_standard = create_users.make("../fingers/standard/crossMatchDB")
    print("created list of standard...")

    print(list(map(lambda probe: comparing.compare_one_with_n(probe, list_standard), list_probe)))
    # probe = cv2.imread("database/101_2.tif", cv2.IMREAD_GRAYSCALE)
    # standard = cv2.imread("database/101_3.tif", cv2.IMREAD_GRAYSCALE)
    # comparing.compare(probe, standard)


if __name__ == "__main__":
    try:
        main()
    except:
        raise
