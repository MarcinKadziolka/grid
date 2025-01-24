# -*- coding: utf-8 -*-
import subprocess
from itertools import zip_longest
import os
from turtledemo.penrose import start

import optuna
import uuid
import shutil
from collections import namedtuple
PSNR = namedtuple('PSNR', 'iter value')

config_parameters = ["model_learning_phase",
                     "data_directory_path",
                     "pretrained_gs_model_path",
                     "data_format",
                     "start_epoch",
                     "end_epoch",
                     "lr_gauss_rgb_components",
                     "exp_decay_coeff_lr_gauss_rgb_component",
                     "final_value_lr_gauss_rgb_component",
                     "lr_gauss_alpha_component",
                     "exp_decay_coeff_lr_gauss_alpha_component",
                     "final_value_lr_gauss_alpha_component",
                     "lr_gauss_means",
                     "exp_decay_coeff_lr_gauss_means",
                     "final_value_lr_gauss_means",
                     "lr_gauss_scales",
                     "exp_decay_coeff_lr_gauss_scales",
                     "final_value_lr_gauss_scales",
                     "lr_gauss_quaternions",
                     "exp_decay_coeff_lr_gauss_quaternions",
                     "final_value_lr_gauss_quaternions",
                     "densification_frequency",
                     "densification_start_epoch",
                     "densification_end_epoch",
                     "alpha_threshold_for_gauss_removal",
                     "min_s_coeff_clip_threshold",
                     "max_s_coeff_clip_threshold",
                     "min_s_norm_threshold_gauss_removal",
                     "max_s_norm_threshold_gauss_removal",
                     "mu_gradient_norm_threshold_densification",
                     "s_norm_threshold_gauss_split_strategy",
                     "split_ratio_for_gauss_split_strategy",
                     "lambda_parameter_for_the_cost_function",
                     "ray_termination_t_threshold",
                     "last_significant_gauss_alpha_gradient_precision",
                     "chi_square_squared_radius_gauss_ellipsoid_of_confidence",
                     "max_num_gauss_per_ray",
                     "model_parameter_save_freq",
                     "model_evaluation_freq",
                     "model_evaluation_epoch",
                     "maximum_number_of_gauss_per_model_threshold"]

def extract_from_config(config, config_parameters, to_extract):
    extracted = {}
    for i, param in enumerate(config_parameters):
        if param in to_extract:
            extracted[param] = config[i]
    return extracted



def read_config(config_name):
    with open(config_name, encoding="utf-8") as file:
        all_lines = file.read().splitlines()

    return all_lines

def create_new_config(config_parameters, optuna_values, current_config):
    new_config = []

    for i, config_line in enumerate(current_config):
        try:
            value, desc = config_line.split("<")
            if config_parameters[i] in optuna_values.keys():
                new_config.append("".join(
                    [str(optuna_values[config_parameters[i]]), "\t\t", "<" + desc]))
            else:
                new_config.append(config_line)
        except:
            new_config.append(config_line)

    return new_config


def insert_optuna_values(config_parameters, config_name, optuna_values):
    with open(config_name, encoding="utf-8") as file:
        all_lines = file.read().splitlines()

        new_config = []

        for i, config_line in enumerate(all_lines):
            try:
                value, desc = config_line.split("<")
                if config_parameters[i] in optuna_values.keys():
                    new_config.append("".join(
                        [str(optuna_values[config_parameters[i]]), "\t\t", "<" + desc]))
                else:
                    new_config.append(config_line)
            except:
                new_config.append(config_line)
    return new_config



def write_config(config, name="config.txt"):
    with open(name, "w", encoding="utf-8") as file:
        for line in config:
            file.write(f"{line}\n")


def get_pid(name):
    return subprocess.check_output(["pidof",name])

def run_ray_splatting():
    windows_app_path = r"..\x64\Release\WindowsApp.exe"
    subprocess.run([windows_app_path])

def read_psnr_txt(filename):
    iter_psnr = []
    with open(filename, encoding="utf-8") as file:
        all_lines = file.read().splitlines()
        for line in all_lines:
            iteration, psnr = line[:-1].split(": ")
            iter_psnr.append(PSNR(int(iteration), float(psnr)))
    return iter_psnr


def sort_by_item(iterable, index):
    return sorted(
        iterable,
        key=lambda x: x[index],
        reverse=True
    )

def get_best_psnr(filename):
    psnr_test = read_psnr_txt(filename)
    psnr_test_sorted = sort_by_item(iterable=psnr_test, index=1)
    return psnr_test_sorted[0]


def log_files(target_base_dir, best_psnr, best_psnr_iter):


    unique_name = create_unique_output_name()
    optuna_dir = os.path.join("./", target_base_dir, "optuna")
    os.makedirs(optuna_dir, exist_ok=True)
    with open(os.path.join(optuna_dir, "optuna_log.txt"), "a") as file:
        file.write(f"{unique_name}: {best_psnr}\n")
    target_dir = os.path.join(optuna_dir, unique_name)
    # prepare structure
    os.makedirs(target_dir, exist_ok=True)



    to_log = ["PSNR_test.txt", "PSNR_train.txt", "MSE_test.txt", "MSE_train.txt"]
    for file in to_log:
        shutil.move(file, target_dir)

    shutil.copy("config.txt", os.path.join(target_dir, "config.txt"))

    saves_dir = r".\dump\save"
    for file_type in ["GC", "m", "v"]:
        for i in range(1, 5):
            filename = f"{best_psnr_iter}.{file_type}{i}"
            save_file_path = os.path.join(saves_dir, filename)
            shutil.move(save_file_path, target_dir)

    shutil.rmtree(saves_dir)
    os.makedirs(saves_dir)

def create_unique_output_name():
    if os.getenv('OAR_JOB_ID'):
        unique_str = os.getenv('OAR_JOB_ID')
    else:
        unique_str = str(uuid.uuid4())
    return unique_str

def parse_value(config_line):
    return config_line.split("<")[0].replace(" ", "")

def objective(trial):
    optuna_values = {
        "lr_gauss_rgb_components": trial.suggest_float('lr_gauss_rgb_components', 1e-5, 1e-2)
    }
    current_config = read_config(config_name="config.txt")

    extracted = extract_from_config(config_parameters=config_parameters, config=current_config,
                                    to_extract=["data_directory_path", "model_parameter_save_freq", "model_evaluation_freq"])
    data_directory_path = parse_value(extracted["data_directory_path"])

    model_parameter_save_freq = int(parse_value(extracted["model_parameter_save_freq"]))
    model_evaluation_freq = int(parse_value(extracted["model_evaluation_freq"]))

    assert model_evaluation_freq == model_parameter_save_freq, "model_parameter_save_freq must be the same as model model_evaluation_freq"


    extracted = extract_from_config(config_parameters=config_parameters, config=current_config, to_extract=["data_directory_path"])
    data_directory_path = extracted["data_directory_path"].split("<")[0].replace(" ", "")

    new_config = create_new_config(config_parameters=config_parameters, optuna_values=optuna_values, current_config=current_config)
    write_config(config=new_config, name="config.txt")

    run_ray_splatting()
    psnr = get_best_psnr("PSNR_Test.txt")

    log_files(data_directory_path, psnr.value, psnr.iter)

    return psnr.value


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=3)