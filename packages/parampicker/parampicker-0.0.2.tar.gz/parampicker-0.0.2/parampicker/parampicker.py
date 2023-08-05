import argparse
import datetime
import json
import logging
import os
import numpy as np
from logging import handlers
import configargparse
import sys
#
# class Parser(configargparse.ArgParser):
#     def __init__(self):
#         super().__init__()
#
#         self.add('--epoch', type=int, help='epoch number', default=3000000)
#         self.add('--tasks', type=int, help='meta batch size, namely task num', default=10)
#         self.add('--capacity', type=int, help='meta batch size, namely task num', default=50)
#         self.add('--meta-lr', type=float, nargs='+', help='meta-level outer learning rate', default=[1e-5, 1e-4, 1e-3])
#         self.add('--l1', type=float, nargs='+', help='meta-level outer learning rate', default=[1e-2, 1e-1, 1e-3])
#         self.add('--b1', type=float, nargs='+', help='meta-level outer learning rate', default=[0.9])
#         self.add('--b2', type=float, nargs='+', help='meta-level outer learning rate', default=[0.999])
#         self.add('--gpus', type=int, help='meta-level outer learning rate', default=1)
#         self.add('--name', help='Name of experiment', default="oml_regression")
#         self.add('--model', help='Name of model', default="representation")
#         self.add('--model-path', help='Path to model', default=None)
#         self.add("--no-save", action="store_true")
#         self.add('--seed', nargs='+', help='Seed', default=[90], type=int)
#         self.add('--rank', type=int, help='meta batch size, namely task num', default=0)
#         self.add("--width", type=int, default=400)
#         self.add('--update-step', type=int, help='task-level inner update steps', default=5)
#         self.add('--update-lr', nargs='+', type=float, help='task-level inner update learning rate',
#                  default=[0.003])

logger = logging.getLogger('global')


# How to use this class (See the main function at the end of this file for an actual example)

## 1. Create an parampicker object in the main file (the one used to run the parampicker)
## 2. Pass a name and args_parse objecte. Output_dir corresponds to directly where all the results will be stored
## 3. Use parampicker.path to get path to the output_dir to store any other results (such as saving the model)
## 4. You can also store results in parampicker.result dictionary (Only add objects which are json serializable)
## 5. Call parampicker.store_json() to store/update the json file (I just call it periodically in the training loop)

class ParamPicker(configargparse.ArgParser):
    '''
    Class to create directory and other meta information to store parampicker results.
    A directory is created in output_dir/DDMMYYYY/name_0
    In-case there already exists a folder called name, name_1 would be created.

    Race condition:
    '''

    def __init__(self):
        super().__init__()
        self.add('--name', help='Name of the experiment', default="untitiled")
        self.add('--seeds', nargs='+', help='List of seeds', default=[90], type=int)
        self.add('--output_dir', help='Output directory for storing results', default="../")
        self.logger = logging.getLogger('global')
        self.state = {}
    def get_logger(self):
        return self.logger

    def parse_params(self, rank=0):
        self.all_args = vars(self.parse_known_args()[0])
        self.state['All arguments'] = self.all_args
        self.rank = rank
        self.state["rank"] = rank
        self.args = self.get_run(self.all_args, self.rank)
        self.state["Selected arguments"] = self.args

        total_seeds = len(self.all_args["seeds"])
        args = self.args
        if "output_dir" in args:
            output_dir = args['output_dir']
        else:
            assert(False)
            output_dir = "../../"

        rank = int(rank/total_seeds)

        self.command_args = "python " + " ".join(sys.argv)
        name = self.args["name"]
        if not args is None:
            if rank is not None:
                self.name = name+ "/" + str(rank) + "/" + "run"
            else:
                self.name = name
            self.params = args
            print(self.params)
            # self.state = {}
            self.dir = output_dir

            root_folder = datetime.datetime.now().strftime("%d%B%Y")

            if not os.path.exists(output_dir + root_folder):
                try:
                    os.makedirs(output_dir + root_folder)
                except:
                    assert (os.path.exists(output_dir + root_folder))

            self.root_folder = output_dir + root_folder
            full_path = self.root_folder + "/" + self.name

            ver = 0

            while True:
                ver += 1
                if not os.path.exists(full_path + "_" + str(ver)):
                    try:
                        os.makedirs(full_path + "_" + str(ver))
                        break
                    except:
                        pass
            self.path = full_path + "_" + str(ver) + "/"

            fh = logging.FileHandler(self.path + "log.txt")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(
                logging.Formatter('rank:' + str(args['rank']) + ' ' + name + ' %(levelname)-8s %(message)s'))
            logger.addHandler(fh)

            ch = logging.handlers.logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(
                logging.Formatter('rank:' + str(args['rank']) + ' ' + name + ' %(levelname)-8s %(message)s'))
            logger.addHandler(ch)
            logger.setLevel(logging.DEBUG)
            logger.propagate = False

            self.store_json()

    def is_jsonable(self, x):
        try:
            json.dumps(x)
            return True
        except:
            return False

    def add_result(self, key, value):
        assert (self.is_jsonable(key))
        assert (self.is_jsonable(value))
        self.state[key] = value

    def store_json(self):
        with open(self.path + "metadata.json", 'w') as outfile:
            json.dump(self.state, outfile, indent=4, separators=(',', ': '), sort_keys=True)
            outfile.write("")

    def get_json(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True)

    def get_run(self, arg_dict, rank):
        # print(arg_dict)
        combinations = []

        if isinstance(arg_dict["seeds"], list):
            combinations.append(len(arg_dict["seeds"]))

        for key in arg_dict.keys():
            if isinstance(arg_dict[key], list) and not key == "seeds":
                combinations.append(len(arg_dict[key]))

        total_combinations = np.prod(combinations)
        selected_combinations = []
        for base in combinations:
            selected_combinations.append(rank % base)
            rank = int(rank / base)

        counter = 0
        result_dict = {}

        result_dict["seeds"] = arg_dict["seeds"]
        if isinstance(arg_dict["seeds"], list):
            result_dict["seeds"] = arg_dict["seeds"][selected_combinations[0]]
            counter += 1

        for key in arg_dict.keys():
            if key != "seeds":
                result_dict[key] = arg_dict[key]
                if isinstance(arg_dict[key], list):
                    result_dict[key] = arg_dict[key][selected_combinations[counter]]
                    counter += 1

        logger.info("Parameters %s", str(result_dict))

        return result_dict



if __name__ == "__main__":
    parser = ParamPicker()
    parser.add_argument('--batch-size', type=int, default=50, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--epochs', type=int, default=200, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--epochs2', type=int, default=10, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--lrs', type=float, nargs='+', default=[0.00001],
                        help='learning rate (default: 2.0)')
    parser.add_argument('--decays', type=float, nargs='+', default=[0.99, 0.97, 0.95],
                        help='learning rate (default: 2.0)')
    parser.add_argument('--rank', type=int, default=6,
                        help='learning rate (default: 2.0)')

    parser.parse_params(0)
    # quit()
    args = parser.args
    # print(args)
    # print(parser.all_args)
    # quit()
    # e = ParamPicker("TestExperiment3", args, args['rank'])
    parser.add_result("Test Key", "Test Result")
    parser.store_json()

