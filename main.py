import argparse
import datetime
import json
import os
import random
import sys

import numpy as np

sys.path.append("..")
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from models import get_model
from tasks import eval_task


class Evaluator:
    def __init__(
        self,
        args,
        seed=1234,
    ):
        self.args = args

        model = args.model
        model_args = args.model_args
        self.set_seed(seed)

        if isinstance(model, str):
            if not model_args:
                exit("model args is required")

            model = get_model(model)(model_args)
        else:
            print("Incorrect model format")
            exit()

        self.model = model
        data_config = self.process_config(args.config_path)

        self.build_tasks(data_config)

    def process_config(self, config_path: str):
        if config_path.endswith("json"):
            data_config = json.load(open(config_path, "r"))
        else:
            exit("config file must be json format")
        return data_config

    def build_tasks(self, configs):
        dataset_map = {v["dataset_name"]: v for v in configs}

        selected_task_objects = []
        for name in dataset_map:
            dataset_cfg = dataset_map[name]

            if not os.path.exists(dataset_cfg["path"]):
                print(f'{dataset_cfg["path"]} not exist!')
                exit()

            if len(dataset_cfg["metrics"]) == 0:
                raise ValueError(
                    "No metric selected for dataset `{}`".format(
                        dataset_cfg["dataset_name"]
                    )
                )

            selected_task_objects.append(
                eval_task.EvalTask(
                    dataset_name=dataset_cfg["dataset_name"],
                    dataset_path=dataset_cfg["path"],
                    description=dataset_cfg.get("description", ""),
                    transform_script_path=dataset_cfg["transforms"],
                    num_few_shot=self.args.num_fewshot
                    if self.args.num_fewshot is not None
                    else dataset_cfg["fewshot"],
                    metrics_config=dataset_cfg["metrics"],
                    sample_config=dataset_cfg.get("generate"),
                    model_postprocess=self.args.postprocess,
                    task_postprocess=dataset_cfg["postprocess"],
                    log_dir=self.args.output_base_path,
                    params=self.args.params,
                    limit=self.args.limit,
                    batch_size=self.args.batch_size,
                )
            )

        self.tasks = selected_task_objects

    def set_seed(self, seed=1234):
        random.seed(seed)
        np.random.seed(seed)

    def run(
        self,
    ):
        for task in self.tasks:
            task.run(self.model)

    def write_out(self):
        def dump_task(task, base_path):
            for ins in task.dataset[: task.limit]:
                ins.dump(os.path.join(base_path, task.dataset_name))

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(dump_task, task, self.args.output_base_path)
                for task in self.tasks
            ]

            for future in futures:
                future.result()

    def make_table(
        self,
    ):
        from pytablewriter import LatexTableWriter, MarkdownTableWriter

        md_writer = MarkdownTableWriter()
        latex_writer = LatexTableWriter()
        md_writer.headers = ["Task", "Metric", "Value"]
        latex_writer.headers = ["Task", "Metric", "Value"]

        values = []
        dataset_result = {}
        for task in self.tasks:
            dataset_name = task.dataset_name.split("_")[0]
            if dataset_name not in dataset_result:
                dataset_result[dataset_name] = dict()
            dataset_result[dataset_name][task.dataset_name] = task.final_metrics

            for k, v in task.final_metrics.items():
                values.append([task.dataset_name, k, "%.4f" % v])

        md_writer.value_matrix = values
        latex_writer.value_matrix = values

        print(md_writer.dumps())

        for dataset, tasks in dataset_result.items():
            sums = defaultdict(float)
            counts = defaultdict(int)
            for key, value in tasks.items():
                for k, v in value.items():
                    sums[k] += v
                    counts[k] += 1
            dataset_result[dataset]["mean_result"] = {
                key: sums[key] / counts[key] for key in sums
            }

        with open(
            os.path.join(self.args.output_base_path, "_all_results.json"), "w"
        ) as f:
            json.dump(dataset_result, f, indent=4, ensure_ascii=False)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--model_args", required=True)
    parser.add_argument("--config_path", type=str, required=True)
    parser.add_argument("--output_base_path", type=str, default="logs")
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--num_fewshot", type=int)
    parser.add_argument("--postprocess", type=str, default="")
    parser.add_argument("--params", type=str, default="")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--write_out", action="store_true", default=False)

    return parser.parse_args()


def main():
    starting = time.time()
    args = parse_args()

    now = datetime.datetime.now()
    dir_name = now.strftime("%Y-%m-%d_%H-%M-%S")
    args.output_base_path = os.path.join(args.output_base_path, dir_name)

    evaluator = Evaluator(args)
    evaluator.run()
    evaluator.make_table()
    running = time.time()
    print(f"Running time: {running - starting} seconds")

    if args.write_out:
        evaluator.write_out()

    ending = time.time()
    print(
        f"Running time: {running - starting} seconds, the whole time: {ending - starting} seconds"
    )


if __name__ == "__main__":
    main()
