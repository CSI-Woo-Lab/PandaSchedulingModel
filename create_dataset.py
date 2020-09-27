import os
from collections import namedtuple as tup
import argparse


import numpy as np
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from sched import SchedT1Dataset
from sched_solver import Solver
from sched_heuristic import liu_test
import sched_heuristic as heu
import pickle

Args = tup("Argument", "seq_len num_procs num_sample period_range util")
NUM_SAMPLES = 20000

## data/#procs_#tasks
import sched
import importlib
importlib.reload(sched)
def gen_taskset(num_procs, seq_len, ddir="data"):
    try:
        os.mkdir(ddir)
    except FileExistsError:
        pass
    base = "%s/%d-%d" % (ddir, num_procs, seq_len)
    try:
        os.mkdir(base)
    except FileExistsError:
        pass


    step = 0.1

    for util in np.arange(step, num_procs, step):
        args = Args(seq_len=seq_len,
            num_procs=num_procs,
            num_sample=NUM_SAMPLES,
            period_range=(10, 1000),
            util=util)
        dataset = sched.SchedT1Dataset(args.num_procs, args.seq_len, args.num_sample, args.period_range, args.util, gg=True)
        with open(os.path.join(base, "%0.2f" % util), 'wb') as f:
            pickle.dump(dataset, f)

#num_proc_list = [4, 8, 12, 16]
#num_tasks_list = [8, 16, 24, 32, 48, 64, 80]
num_proc_list = [4, 6, 8]
num_tasks_list = [24]
samples = []
for num_proc in num_proc_list:
    for num_tasks in num_tasks_list:
        if num_proc >= num_tasks:
            continue
        samples.append((num_proc, num_tasks))


from concurrent.futures import ProcessPoolExecutor
E = ProcessPoolExecutor(32)

def wrap(x):
    print("!")
    num_proc, num_task = x
    print(num_proc, num_task)
    #gen_taskset(num_proc, num_task,"tr")
    #gen_taskset(num_proc, num_task,"te")
    #gen_taskset(num_proc, num_task,"eval")
    gen_taskset(num_proc, num_task,"np_tr")
    gen_taskset(num_proc, num_task,"np_te")
    gen_taskset(num_proc, num_task,"np_eval")
    return "!"

for ret in E.map(wrap, samples):
    print(ret)
