#!/usr/bin/env python
import yaml
import math
import typing
import random
import argparse


def parse_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        return config


def get_command(config: typing.Dict,
                method: str = "grid",
                number: int = -1,
                hyphens: bool = True) -> typing.List[str]:
    params = config["parameters"]
    nums = []
    for key in params:
        if "value" in params[key]:
            params[key]["values"] = [params[key]["value"]]
        elif "min" in params[key] and "max" in params[key]:
            params[key]["values"] = list(range(params[key]["min"], params[key]["max"] + 1))
        nums.append(len(params[key]["values"]))
    total_num = math.prod(nums)
    cmds = [["python", config["program"]] for _ in range(total_num)]
    for key in params:
        num = len(params[key]["values"])
        for i in range(total_num):
            if hyphens:
                cmds[i].append("--" + key)
            else:
                cmds[i].append(key)
            cmds[i].append(str(params[key]["values"][i % num]))
    if method == "grid":
        return cmds
    elif method == "random":
        random.shuffle(cmds)
        return cmds[:number]
    else:
        raise NotImplementedError(
            "Doese not support {} method".format(method)
        )


def save_cmds(cmds, out_path):
    with open(out_path, "w") as f:
        for cmd in cmds:
            f.write(" ".join(cmd) + "\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str,
                        help="config path")
    parser.add_argument("--method", type=str, default="grid",
                        choices=["grid", "random"],
                        help="method (default: %(default)s)")
    parser.add_argument("--number", type=int, default=-1,
                        help="Availible in random mode (default: %(default)s)")
    parser.add_argument("--out-path", type=str, default="commands",
                        help="Out file path (default: %(default)s)")
    parser.add_argument("--max-cmds", type=int, default=-1,
                        help="max commands per outfile (default: %(default)s)")
    parser.add_argument("--no-hypens", action="store_true",
                        help="no hypens (default: %(default)s)")

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    print("Sweep commands :")
    print(args)

    config = parse_config(args.config)

    cmds = get_command(
        config,
        method=args.method,
        number=args.number,
        hyphens=not args.no_hypens
    )
    import ipdb; ipdb.set_trace()

    if args.max_cmds <= 0:
        save_cmds(cmds, args.out_path)
    else:
        num_split = math.ceil(len(cmds) / args.max_cmds)
        for i in range(num_split):
            min_ind = i * args.max_cmds
            max_ind = min((i + 1) * args.max_cmds, len(cmds))
            save_cmds(cmds[min_ind:max_ind],
                      "{}-{}".format(args.out_path, i))

    print("Complete!")


if __name__ == "__main__":
    main()
