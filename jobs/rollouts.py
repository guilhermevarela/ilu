from pathlib import Path
from datetime import datetime
import sys
import os
import json
import tempfile
import argparse
import multiprocessing as mp
import time
from collections import defaultdict

import configparser

from models.rollouts1 import roll

ILURL_HOME = os.environ['ILURL_HOME']

CONFIG_PATH = Path(f'{ILURL_HOME}/config/')

# LOCK = mp.Lock()

# def delay_run(*args):
#     LOCK.acquire()
#     try:
#         time.sleep(1)
#     finally:
#         LOCK.release()
#     return main(*args)

def get_arguments():
    parser = argparse.ArgumentParser(
        description="""
            This scripts runs recursevely every experiment on path. It must receve a batch path.
        """
    )
    parser.add_argument('batch_dir', type=str, nargs='?',
                        help='''A directory which it\'s subdirectories are experiments''')

    return parser.parse_args()

def concat(evaluations):
    """Receives an experiments' json and merges it's contents

    Params:
    -------
        * evaluations: list
        list of rollout evaluations

    Returns:
    --------
        * result: dict
        where `id` key certifies that experiments are the same
              `list` params are united
              `numeric` params are appended

    """
    result = defaultdict(list)
    for qtb in evaluations:
        exid = qtb.pop('id')
        qid = qtb.pop('rollout')
        # can either be a rollout from the prev
        # exid or a new experiment
        if exid not in result['id']:
            result['id'].append(exid)

        ex_idx = result['id'].index(exid)
        for k, v in qtb.items():
            append = isinstance(v, list) or isinstance(v, dict)
            # check if integer fields match
            # such as cycle, save_step, etc
            if not append:
                if k in result:
                    if result[k] != v:
                        raise ValueError(
                            f'key:\t{k}\t{result[k]} and {v} should match'
                        )
                else:
                    result[k] = v
            else:
                if ex_idx == len(result[k]):
                    result[k].append(defaultdict(list))
                result[k][ex_idx][qid].append(v)
    return result
class PipeGuard(object):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, *args, **kwargs):
        sys.stdout.close()
        sys.stdout = self._stdout

if __name__ == '__main__':
    # with PipeGuard():
    # Read script arguments from run.config file.
    args = get_arguments()
    # clear command line arguments after parsing
    batch_path = Path(args.batch_dir)
    # get all tables
    pattern = '**/*Q*.pickle'
#     rollout_paths = [rp for rp in batch_path.glob(pattern)]
# 
#     run_config = configparser.ConfigParser()
#     run_config.read(str(CONFIG_PATH / 'run.config'))
# 
#     num_processors = int(run_config.get('run_args', 'num_processors'))
#     num_runs = int(run_config.get('run_args', 'num_runs'))
#     train_seeds = json.loads(run_config.get("run_args", "train_seeds"))
# 
#     if len(train_seeds) != num_runs:
#         raise configparser.Error('Number of seeds in run.config `train_seeds`'
#                         'must match the number of runs (`num_runs`) argument.')
# 
#     # Assess total number of processors.
#     processors_total = mp.cpu_count()
#     print(f'Total number of processors available: {processors_total}\n')
# 
#     # Adjust number of processors.
#     if num_processors > processors_total:
#         num_processors = processors_total
#         print(f'Number of processors downgraded to {num_processors}\n')
# 
#     # Read train.py arguments from train.config file.
#     rollouts_config = configparser.ConfigParser()
#     rollouts_config.read(str(CONFIG_PATH / 'rollouts.config'))
#     num_rollouts = int(rollouts_config.get('rollouts_args', 'num-rollouts'))
# 
# 
#     # number of processes vs layouts
#     # seeds must be different from training
#     custom_configs = []
#     for rn, rp in enumerate(rollout_paths):
#         base_seed = max(train_seeds) + num_rollouts * rn
#         for rr in range(num_rollouts):
#             seed = base_seed + rr + 1
#             custom_configs.append((str(rp), seed))
# 
#     print(f'''
#     \tArguments (jobs.rollouts.py):
#     \t---------------------------
#     \tNumber of runs: {num_runs}
#     \tNumber of processors: {num_processors}
#     \tTrain seeds: {train_seeds}
#     \tNum. rollout files: {len(rollout_paths)}
#     \tNum. rollout repetions: {num_rollouts}
#     \tNum. rollout total: {len(rollout_paths) * num_rollouts}''')
# 
#     with tempfile.TemporaryDirectory() as f:
# 
#         tmp_path = Path(f)
#         # Create a config file for each train.py
#         # with the respective seed. These config
#         # files are stored in a temporary directory.
#         rollouts_cfg_paths = []
#         cfg_key = "rollouts_args"
#         for cfg in custom_configs:
#             rollout_path, seed = cfg
# 
#             # Setup custom rollout settings
#             rollouts_config.set(cfg_key, "rollout-path", str(rollout_path))
#             rollouts_config.set(cfg_key, "rollout-seed", str(seed))
#             
#             # Write temporary train config file.
#             cfg_path = tmp_path / f'rollouts-{seed}.config'
#             rollouts_cfg_paths.append(str(cfg_path))
#             print(str(cfg_path))
#             with cfg_path.open('w') as fw:
#                 rollouts_config.write(fw)
#             # tmp_cfg_file = open(cfg_path, "w")
# 
#             # rollout_config.write(tmp_cfg_file)
#             # tmp_cfg_file.close()
# 
#             
#         # pool = mp.Pool(num_processors)
#         # rvs = pool.map(roll, [[cfg] for cfg in rollout_configs])
#         # pool.close()
#         # Run.
#         # TODO: option without pooling not working. why?
#         # rvs: directories' names holding experiment data
#         # if num_processors > 1:
#         #     pool = mp.Pool(num_processors)
#         #     rvs = pool.map(delay_run, [[cfg] for cfg in train_configs])
#         #     pool.close()
#         # else:
#         rvs = []
#         for cfg in rollouts_cfg_paths[:2]:
#             rvs.append(roll([cfg]))

        # cfg = rollouts_cfg_paths[0]
        # t = Thread(target=roll(cfg))
        # t.start()
#         import json
#         for i, data in enumerate(rvs):
#             json_path = batch_path / f'{i}.json'
#             with json_path.open('w') as fj:
#                 json.dump(data, fj)
# 
# 
#         pdb.set_trace()
    import pdb
    rvs = []
    for i in range(2):
        json_path = batch_path / f'{i}.json'

        with json_path.open('r') as fj:
            data = json.load(fj)
        rvs.append(data)

    pdb.set_trace()
    # this should be json files in need of concatenation

    # Create a directory and move newly created files
    paths = [Path(f) for f in rvs]
    commons = [p.parent for p in paths]
    if len(set(commons)) > 1:
        raise ValueError(f'Directories {set(commons)} must have the same root')
    dirpath = commons[0]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S.%f')
    batchpath = dirpath / timestamp
    if not batchpath.exists():
        batchpath.mkdir()

    # Move files
    for src in paths:
        dst = batchpath / src.parts[-1]
        src.replace(dst)
    # sys.stdout.write(str(batchpath))
