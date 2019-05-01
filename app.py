import os
import cv2

import create_users
import comparing
import time
os.chdir("C:/Institut/programs/")
# os.chdir("/home/nikolay/learning/")


def calc_f_metric(cr):
    if cr.true_positive == 0:
        precision = 0
        recall = 0
        f_metric = 0
    else:
        precision = cr.true_positive / (cr.true_positive + cr.false_positive)
        recall = cr.true_positive / (cr.true_positive + cr.false_negative)
        b = 1
        f_metric = (1 + b ** b) * ((precision * recall) / (b ** b * precision + recall))
    return [precision, recall, f_metric]


def calc_far_frr(cr):
    far = cr.false_positive / (cr.false_positive + cr.true_negative)
    frr = cr.false_negative / (cr.true_positive + cr.false_negative)
    return [far, frr]


def calc_tpr_fpr(cr):
    tpr = cr.true_positive / (cr.true_positive + cr.false_negative)
    fpr = cr.false_positive / (cr.true_negative + cr.false_positive)
    return [tpr, fpr]


def main():
    print("run comparing...")
    start_time = time.time()
    list_probe = create_users.make("fingers/probe/crossMatchDB")
    print("created list of probe on {} sec...".format(time.time() - start_time))
    start_time = time.time()
    list_standard = create_users.make("fingers/standard/crossMatchDB")
    print("created list of standard on {} sec...".format(time.time() - start_time))

    def calc_result(threshold):
        print("расчёт на уровне {}".format(threshold))
        list_results =\
            list(map(lambda probe: comparing.compare_one_with_n(probe, list_standard, threshold), list_probe))
        result = comparing.fold_results(list_results)
        print(result.to_string())
        print("precision, recall, f-metric {}".format(calc_f_metric(result)))
        print("FAR, FRR {}".format(calc_far_frr(result)))
        print("TPR, FPR {}".format(calc_tpr_fpr(result)))
        print("----------------------------------------------------------")
        return result

    thresholds = list(range(200, 1, -4))
    results = list(map(calc_result, thresholds))
    print("All precision, recall, f-metric {}".format(list(map(calc_f_metric, results))))
    print("All FAR, FRR {}".format(list(map(calc_far_frr, results))))
    print("All TPR, FPR {}".format(list(map(calc_tpr_fpr, results))))
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
