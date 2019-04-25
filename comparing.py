import cv2
import numpy
import matplotlib.pyplot as plt
from enhance import image_enhance
# from skimage.morphology import skeletonize
import functools
from compare_result import Compare_result
import time


def removedot(invertThin):
    temp0 = numpy.array(invertThin[:])
    temp0 = numpy.array(temp0)
    temp1 = temp0/255
    temp2 = numpy.array(temp1)
    temp3 = numpy.array(temp2)

    enhanced_img = numpy.array(temp0)
    filter0 = numpy.zeros((10,10))
    W,H = temp0.shape[:2]
    filtersize = 6

    for i in range(W - filtersize):
        for j in range(H - filtersize):
            filter0 = temp1[i:i + filtersize,j:j + filtersize]

            flag = 0
            if sum(filter0[:, 0]) == 0:
                flag += 1
            if sum(filter0[:, filtersize - 1]) == 0:
                flag += 1
            if sum(filter0[0, :]) == 0:
                flag += 1
            if sum(filter0[filtersize - 1,:]) == 0:
                flag += 1
            if flag > 3:
                temp2[i:i + filtersize, j:j + filtersize] = numpy.zeros((filtersize, filtersize))

    return temp2


def get_descriptors(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)
    # start_time = time.time()
    img = image_enhance.crop_image(img, 350)
    img = numpy.array(img, dtype=numpy.uint8)
    # print("{} time apply enchance".format(time.time() - start_time))
    # Threshold
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU);
    # Normalize to 0 and 1 range
    img[img == 255] = 1

    #Thinning
    # skeleton = skeletonize(img)
    # skeleton = numpy.array(skeleton, dtype=numpy.uint8)
    # skeleton = removedot(skeleton)
    # Harris corners
    harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)
    harris_normalized = cv2.normalize(harris_corners, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
    threshold_harris = 125
    # Extract keypoints
    keypoints = []
    for x in range(0, harris_normalized.shape[0]):
        for y in range(0, harris_normalized.shape[1]):
            if harris_normalized[x][y] > threshold_harris:
                keypoints.append(cv2.KeyPoint(y, x, 1))
    # Define descriptor
    orb = cv2.ORB_create()
    # Compute descriptors
    _, des = orb.compute(img, keypoints)
    return (keypoints, des);


def compare(probe, standard, threshold, need_plot=False):
    # image_name = sys.argv[1]
    kp1, des1 = probe.image  # get_descriptors(probe_image)
    # image_name = sys.argv[2]
    kp2, des2 = standard.image  # get_descriptors(standard_image)

    # Matching between descriptors
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = sorted(bf.match(des1, des2), key=lambda match: match.distance)

    if need_plot:
        # Plot keypoints
        img4 = cv2.drawKeypoints(probe.image, kp1, outImage=None)
        img5 = cv2.drawKeypoints(standard.image, kp2, outImage=None)
        f, axarr = plt.subplots(1, 2)
        axarr[0].imshow(img4)
        axarr[1].imshow(img5)
        plt.show()
        # Plot matches
        img3 = cv2.drawMatches(probe.image, kp1, standard.image, kp2, matches, flags=2, outImg=None)
        plt.imshow(img3)
        plt.show()

    # Calculate score
    score = 0
    for match in matches:
        score += match.distance
    result = score/len(matches) < threshold
    user_match = probe.user_id == standard.user_id and probe.finger_id == standard.finger_id

    print("user_ids", probe.user_id, standard.user_id, "finger_ids", probe.finger_id, standard.finger_id)
    if result:
        if user_match:
            return lambda cr: Compare_result(
                true_positive=cr.true_positive + 1,
                false_positive=cr.false_positive,
                true_negative=cr.true_negative,
                false_negative=cr.false_negative)
        else:
            return lambda cr: Compare_result(
                true_positive=cr.true_positive,
                false_positive=cr.false_positive + 1,
                true_negative=cr.true_negative,
                false_negative=cr.false_negative)
    else:
        if user_match:
            return lambda cr: Compare_result(
                true_positive=cr.true_positive,
                false_positive=cr.false_positive,
                true_negative=cr.true_negative,
                false_negative=cr.false_negative + 1)
        else:
            return lambda cr: Compare_result(
                true_positive=cr.true_positive,
                false_positive=cr.false_positive,
                true_negative=cr.true_negative + 1,
                false_negative=cr.false_negative)


def fold_funcs(list_func):
    return functools.reduce(lambda acc, f: f(acc), list_func, Compare_result(0, 0, 0, 0))


def func_fold(acc, res):
    return Compare_result(
        true_positive=acc.true_positive + res.true_positive,
        false_positive=acc.false_positive + res.false_positive,
        true_negative=acc.true_negative + res.true_negative,
        false_negative=acc.false_negative + res.false_negative)


def fold_results(list_cr):
    return functools.reduce(func_fold, list_cr, Compare_result(0, 0, 0, 0))


def compare_one_with_n(probe, list_standard, threshold=40):
    return fold_funcs(list(map(lambda standard: compare(probe, standard, threshold), list_standard)))
