import os
import cv2

import create_users
import comparing
import time
import multiprocessing

# os.chdir("C:/Institut/programs/")
os.chdir("/home/nikolay/learning/")


if __name__ == "__main__":
    start_time = time.time()
    print("run comparing...")
    list_probe = create_users.make("fingers/probe/crossMatchDB_mini")
    print("created list of probe...")
    list_standard = create_users.make("fingers/standard/crossMatchDB_mini")
    print("created list of standard...")

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(processes=pool_size)
    list_results = pool.map(lambda probe: comparing.compare_one_with_n(probe, list_standard), list_probe)
    # print("list", list(map(lambda res: res.to_string(), list_results)))
    pool.close()
    pool.join()
    print(comparing.fold_results(list_results).to_string())
    print("%s sec" % (time.time() - start_time))
