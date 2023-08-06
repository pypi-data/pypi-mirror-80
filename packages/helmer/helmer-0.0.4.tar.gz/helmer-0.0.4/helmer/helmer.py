import os
import sys

import yaml
import string
import json

# from ruamel.yaml import YAML


def make_values(values):
    flat_values = []
    flat_values_str = []

    def walk(item, path=""):
        if hasattr(item, "items"):
            for k, v in item.items():
                walk(v, f"{path + (path and '.')}{k}")
        else:
            print(item)
            # value = str(item).replace("True", "true").replace("False", "false")
            if isinstance(item, str):
                value = json.dumps(item)  # .replace('"', "")
                flat_values_str.append(f"{path}={value}")
            else:
                value = json.dumps(item)  # .replace('"', "")
                flat_values.append(f"{path}={value}")

    for value in values:
        walk(value)
    return flat_values, flat_values_str


def main():
    path = "helmer.yaml"
    if len(sys.argv) > 1:
        path = os.path.join(sys.argv[1], "helmer.yaml")
    with open(path) as f:
        # yaml = YAML(typ="safe")
        # y = yaml.load(f)
        y = yaml.load(f, Loader=yaml.FullLoader)
    for r in y["releases"]:
        repo_name = r["chart"].split("/")[0]
        os.system(f'helm repo add {repo_name} {r["repository"]}')
        os.system("helm repo update")
        flat_values, flat_values_str = make_values(r["values"])
        r["flat_values"] = "--set " + ",".join(flat_values)
        r["flat_values_str"] = "--set-string " + ",".join(flat_values_str)
        r["ver"] = f" --version {r['version']}" if r.get("version") else ""
        os.system(f"kubectl create ns {r['namespace']} &> /dev/null")
        cmd = string.Template(
            "helm upgrade -i $name $chart --namespace $namespace$ver $flat_values $flat_values_str"
        ).substitute(r)
        # print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    # sys.argv.append("charts.yaml")
    main()
