"""Console script for igel."""
import sys
import argparse
from igel import Igel, models_dict, metrics_dict
import inspect
import pdb


class CLI(object):
    """CLI describes a command line interface for interacting with igel, there
    are several different functions that can be performed.

    """

    available_args = {
        # fit, evaluate and predict args:
        "dp": "data_path",
        "yml": "yaml_path",
        "DP": "data_paths",

        # models arguments
        "name": "model_name",
        "type": "model_type"
    }

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Igel CLI Runner',
            usage='''
                     ___           _    ____ _     ___
                    |_ _|__ _  ___| |  / ___| |   |_ _|
                     | |/ _` |/ _ \ | | |   | |    | |
                     | | (_| |  __/ | | |___| |___ | |
                    |___\__, |\___|_|  \____|_____|___|
                        |___/


                    igel <command> [<args>]
                    - Available sub-commands at the moment are:
                       fit                 fits a model
                       evaluate            evaluate the performance of a pre-fitted model
                       predict             Predicts using a pre-fitted model
                       experiment          this command will run fit, evaluate and predict together
                       help                get help about how to use igel
                       models              get a list of supported machine learning algorithms/models
                       metrics             get a list of all supported metrics

                    - Available arguments:

                        # for usage with the fit, evaluate or predict command:
                        --data_path         Path to your dataset
                        --yaml_file         Path to your yaml file

                        # for usage with the experiment command
                        --data_paths        Paths to data you want to use for fitting, evaluating and predict respectively
                        --yaml_file         Path to the yaml file that will be used when fitting the model

                        # for getting help with the models command:
                        --model_type        type of the model you want to get help on -> whether regression or classification
                        --model_name        name of the model you want to get help on
                        ------------------------------------------

                        or for the short version
                        # for usage with the fit, evaluate or predict command:
                        -dp         Path to your dataset
                        -yml        Path to your yaml file

                      # for usage with the experiment command
                        -DP        Paths to data you want to use for fitting, evaluating and predict respectively
                        -yml       Path to the yaml file that will be used when fitting the model

                        # for getting help with the models command:
                        -type        type of the model you want to get help on -> whether regression or classification
                        -name        name of the model you want to get help on
                        ------------------------------------------

                    - Quick Start:

                    igel -h                                                             # print this help guide

                    igel models                                                         # type this to get a list of supported models

                    igel models -type regression -name random_forest                    # this will give you a help on how to use the
                                                                                        # RandomForestRegressor and will provide
                                                                                        # you a link to get more help in the sklearn website

                    igel metrics                                                        # get a list of all supported metrics

                    igel fit -dp "path_to_data" -yml "path_to_yaml_file"                # fit a model

                    igel evaluate -dp "path_to_data"                                    # evaluate the trained/pre-fitted model

                    igel predict -dp "path_to_data"                                     # make predictions using the trained/pre-fitted model

                    igel experiment -DP "path_to_train_data \                           # this will run fit using the trian data first,
                                        path_to_evaluation_data \                       # then will run evaluate using the evaluation data
                                        path_to_data_you_want_to_predict_on"            # and finally, will generate predictions on the last
                                    -yml "path_to_yaml_file"                            # data you passed to predict on.



''')

        self.parser.add_argument('command', help='Subcommand to run')
        self.cmd = self.parse_command()
        self.args = sys.argv[2:]
        self.dict_args = self.convert_args_to_dict()
        getattr(self, self.cmd.command)()

    def validate_args(self, dict_args: dict) -> dict:
        """
        validate arguments entered by the user and transform short args to the representation needed by igel
        @param dict_args: dict of arguments
        @return: new validated and transformed args

        """
        d_args = {}
        for k, v in dict_args.items():
            if k not in self.available_args.keys() and k not in self.available_args.values():
                print(f'Unrecognized argument -> {k}')
                self.parser.print_help()
                exit(1)

            elif k in self.available_args.values():
                d_args[k] = v

            else:
                d_args[self.available_args[k]] = v

        return d_args

    def convert_args_to_dict(self) -> dict:
        """
        convert args list to a dictionary
        @return: args as dictionary
        """

        dict_args = {self.args[i].replace('-', ''): self.args[i + 1] for i in range(0, len(self.args) - 1, 2)}
        dict_args = self.validate_args(dict_args)
        dict_args['cmd'] = self.cmd.command
        return dict_args

    def parse_command(self):
        """
        parse command, which represents the function that will be called by igel
        @return: command entered by the user
        """
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        cmd = self.parser.parse_args(sys.argv[1:2])
        if not hasattr(self, cmd.command):
            print('Unrecognized command')
            self.parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        return cmd

    def help(self, *args, **kwargs):
        self.parser.print_help()

    def fit(self, *args, **kwargs):
        print("""
         _____          _       _
        |_   _| __ __ _(_)_ __ (_)_ __   __ _
          | || '__/ _` | | '_ \| | '_ \ / _` |
          | || | | (_| | | | | | | | | | (_| |
          |_||_|  \__,_|_|_| |_|_|_| |_|\__, |
                                        |___/
        """)
        Igel(**self.dict_args)

    def predict(self, *args, **kwargs):
        print("""
         ____               _ _      _   _
        |  _ \ _ __ ___  __| (_) ___| |_(_) ___  _ __
        | |_) | '__/ _ \/ _` | |/ __| __| |/ _ \| '_ \
        |  __/| | |  __/ (_| | | (__| |_| | (_) | | | |
        |_|   |_|  \___|\__,_|_|\___|\__|_|\___/|_| |_|


        """)
        Igel(**self.dict_args)

    def evaluate(self, *args, **kwargs):
        print("""
         _____            _             _   _
        | ____|_   ____ _| |_   _  __ _| |_(_) ___  _ __
        |  _| \ \ / / _` | | | | |/ _` | __| |/ _ \| '_ \
        | |___ \ V / (_| | | |_| | (_| | |_| | (_) | | | |
        |_____| \_/ \__,_|_|\__,_|\__,_|\__|_|\___/|_| |_|

        """)
        Igel(**self.dict_args)

    def print_models_overview(self):
        print(f"\n"
              f"{'*' * 60}  Supported machine learning algorithms  {'*' * 60} \n\n"
              f"1 - Regression algorithms: \n"
              f"{'-' * 50} \n"
              f"{list(models_dict.get('regression').keys())} \n\n"
              f"{'=' * 120} \n"
              f"2 - Classification algorithms: \n"
              f"{'-' * 50} \n"
              f"{list(models_dict.get('classification').keys())} \n"
              f" \n")

    def models(self):
        """
        show an overview of all models supported by igel
        """
        if not self.dict_args:
            self.print_models_overview()
        else:
            model_name = self.dict_args.get('model_name', None)
            model_type = self.dict_args.get('model_type', None)

            if not model_name:
                print(f"Please enter a supported model")
                self.print_models_overview()
            else:
                if not model_type:
                    print(f"Please enter a type argument to get help on the chosen model\n"
                          f"type can be whether regression or classification \n")
                    self.print_models_overview()
                    return
                if model_type not in ('regression', 'classification'):
                    raise Exception(f"{model_type} is not supported! \n"
                                    f"model_type need to be regression or classification")

                models = models_dict.get(model_type)
                model_data = models.get(model_name.replace('_', ' '))
                model, link = model_data.values()
                print(f"model type: {model_type} \n"
                      f"model name: {model_name} \n"
                      f"sklearn model class: {model.__name__} \n"

                      f"{'-' * 60}\n"
                      f"You can click the link below to know more about the optional arguments "
                      f"that you can use with your chosen model ({model_name}).\n"
                      f"You can provide these optional arguments in the yaml file if you want to use them\n"
                      f"link: {link} \n")

    def metrics(self):
        """
        show an overview of all metrics supported by igel
        """
        print(f"\n\n"
              f"{'*' * 60}  Supported metrics  {'*' * 60} \n\n"
              f"1 - Regression metrics: \n"
              f"{'-' * 50} \n"
              f"{[func.__name__ for func in metrics_dict.get('regression')]} \n\n"
              f"{'=' * 120} \n"
              f"2 - Classification metrics: \n"
              f"{'-' * 50} \n"
              f"{[func.__name__ for func in metrics_dict.get('classification')]} \n"
              f" \n")

    def experiment(self):
        print("""
         _____                      _                      _
        | ____|_  ___ __   ___ _ __(_)_ __ ___   ___ _ __ | |_
        |  _| \ \/ / '_ \ / _ \ '__| | '_ ` _ \ / _ \ '_ \| __|
        | |___ >  <| |_) |  __/ |  | | | | | | |  __/ | | | |_
        |_____/_/\_\ .__/ \___|_|  |_|_| |_| |_|\___|_| |_|\__|
                   |_|

        """)
        data_paths = self.dict_args['data_paths']
        yaml_path = self.dict_args['yaml_path']
        train_data_path, eval_data_path, pred_data_path = data_paths.strip().split(' ')
        # print(f"{train_data_path} | {eval_data_path} | {test_data_path}")
        train_args = {"cmd": "fit",
                      "yaml_path": yaml_path,
                      "data_path": train_data_path}
        eval_args = {"cmd": "evaluate",
                     "data_path": eval_data_path}
        pred_args = {"cmd": "predict",
                     "data_path": pred_data_path}
        Igel(**train_args)
        Igel(**eval_args)
        Igel(**pred_args)


def main():
    CLI()


if __name__ == "__main__":
    main()
