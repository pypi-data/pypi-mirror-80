import json
import collections
import random
import os
from copy import deepcopy


def keypaths(nested):
    for key, value in nested.items():
        if isinstance(value, collections.Mapping):
            for subkey, subvalue in keypaths(value):
                yield [key] + subkey, subvalue
        else:
            yield [key], value


def create_test_data_sets(api, method):
    with open("tests/params_captured.json") as fobj:
        f = json.load(fobj)
    params_collection = []
    for _ in f.get(api, {}).get("200", {}).get(method, {}):
        params_info = {}
        for k, v in keypaths(_):
            if type(v) is list:
                for e in v:
                    if type(e) is dict:
                        for i, j in keypaths(e):
                            params_info[i[-1]] = j
                    else:
                        params_info[k[-1]] = v
            else:
                params_info[k[-1]] = v
        params_collection.append(params_info)

    input_params = {}
    processed_params = []
    selected_events_data = []
    for collection in params_collection:
        for k, v in collection.items():
            if k.startswith("$"):
                continue
            if k not in input_params:
                input_params[k] = {}
                continue
            if type(v) is list:
                if len(v) > len(input_params.get(k, {}).get(k, [])):
                    processed_params.append(k)
                    if input_params:
                        new_collection = deepcopy(collection)
                        new_collection["$comment"] = "Maximum length for List " + str(k) + " is " + str(
                            len(v)) + " with " \
                                      "values " + str(v)
                        input_params[k] = new_collection
            elif type(v) is bool:
                continue
            elif type(v) is int:
                if v > input_params.get(k, {}).get(k, 0):
                    processed_params.append(k)
                    if input_params:
                        new_collection = deepcopy(collection)
                        new_collection["$comment"] = "Maximum value for " + str(k) + " is " + str(v)
                        input_params[k] = new_collection
            elif len(str(v)) > len(str(input_params.get(k, {}).get(k, ""))):
                processed_params.append(k)
                if input_params:
                    new_collection = deepcopy(collection)
                    new_collection["$comment"] = "Maximum value for " + str(k) + " is " + str(
                        v) + " with length " + str(len(str(v)))
                    input_params[k] = new_collection
    selected_events_data += list(input_params.values())

    for collection in params_collection:
        for k, v in collection.items():
            if k.startswith("$"):
                continue
            if k not in input_params:
                input_params[k] = {}
                continue
            try:
                v = int(v)
            except ValueError:
                v = str(v)
            except TypeError:
                pass
            if type(v) is list:
                if len(v) < len(input_params.get(k, {}).get(k, [])):
                    processed_params.append(k)
                    if input_params:
                        new_collection = deepcopy(collection)
                        new_collection["$comment"] = "Minimum length for List " + str(k) + " is " + str(
                            len(v)) + " with " \
                                      "values " + str(v)
                        input_params[k] = new_collection
            elif type(v) is bool:
                continue
            elif type(v) is int:
                if v < int(input_params.get(k, {}).get(k, 0)):
                    processed_params.append(k)
                    if input_params:
                        new_collection = deepcopy(collection)
                        new_collection["$comment"] = "Minimum value for " + str(k) + " is " + str(v)
                        input_params[k] = new_collection
            elif len(str(v)) < len(str(input_params.get(k, {}).get(k, ""))):
                processed_params.append(k)
                if input_params:
                    new_collection = deepcopy(collection)
                    new_collection["$comment"] = "Minimum value for " + str(k) + " is " + str(
                        v) + " with length " + str(len(str(v)))
                    input_params[k] = new_collection
    selected_events_data += list(input_params.values())
    return selected_events_data


def generate_auto_input_params_file():
    with open("tests/data/params_info_from_spec.json") as fobj:
        f1 = json.load(fobj)
    input_params = {}
    for api, info in f1.items():
        if api not in input_params:
            input_params[api] = {"200": {}, "400": {}, "401": {}}
        for method, method_info in info.items():
            data_set = create_test_data_sets(api, method)
            if not data_set:
                continue
            random_data_set = random.choice(data_set)
            for k, v in random_data_set.items():
                if k.startswith("$"):
                    continue
                if k in method_info.get("required"):
                    error_data_block = deepcopy(random_data_set)
                    error_data_block[k] = "<delete>"
                    error_data_block["$comment"] = "This payload will miss the mandatory parameter " + str(k)
                    if method not in input_params[api]["400"]:
                        input_params[api]["400"][method] = [error_data_block]
                    else:
                        input_params[api]["400"][method].append(error_data_block)
                else:
                    success_data_block = deepcopy(random_data_set)
                    success_data_block[k] = "<delete>"
                    success_data_block["$comment"] = "This payload will miss the optional parameter " + str(k)
                    if method not in input_params[api]["200"]:
                        input_params[api]["200"][method] = [success_data_block]
                    else:
                        input_params[api]["200"][method].append(success_data_block)

            if method not in input_params[api]["200"]:
                input_params[api]["200"][method] = data_set
            else:
                input_params[api]["200"][method] += data_set

    if os.path.exists("tests"):
        with open("tests/input_params_auto-generated.json","w+") as fobj:
            fobj.write(json.dumps(input_params, indent=4))
    else:
        with open("input_params_auto-generated.json","w+") as fobj:
            fobj.write(json.dumps(input_params, indent=4))

# get_details("/v1/channels","post")

generate_auto_input_params_file()
