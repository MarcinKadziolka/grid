# Script allowing for hyperparameter search using ![Optuna](https://optuna.org/)

## Installation

### Clone and enter the repository

```
git clone git@github.com:MarcinKadziolka/grid.git
cd grid
```

### Create virtual environment and activate it

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install required packages

```
pip install -r requirements.txt
```

### Move the script

Script must be placed into main project directory:
```
C:\Users\<username>\source\repos\WindowsApp\WindowsApp
```
```
├── WindowsApp
│   ├── WindowsApp
│   │   ├── **grid.py**
│   │   ├── dump
│   │   │   ├── save
│   │   ├── models
│   │   │   ├── <dataset_1>
│   │   │   ├── <dataset_2>
│   │   │   ├── <dataset_n>
│   │   ├── x64\
       .
       .
       .
│   │   ├── config.txt    
│   │   ├── WindowsApp.cpp
│   ├── x64
│   │   ├── Release
│   │   │   ├── WindowsApp.exe
```

### Set hyperparameters
Use the dictionary to add hyperparameters that will be subjected for search:
```
optuna_values = {
        "lr_gauss_rgb_components": trial.suggest_float('lr_gauss_rgb_components', 1e-5, 1e-2),
        "lr_gauss_alpha_component": trial.suggest_float('lr_gauss_alpha_component', 1e-5, 1e-2),
        "lr_gauss_means": trial.suggest_float('lr_gauss_means', 1e-5, 1e-2),
    }
```
For more information about setting the trial suggestion refer to the ![Optuna docs.](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)


Refer to the config parameters list to set specific parameter value:
```
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
```
### Set the number of runs
Adjust the `n_trials` argument.
```
study.optimize(objective, n_trials=3)
```
### Run the program

```
python3 grid.py
```

### Results
Results are stored in the `<Blender data directory path (1)>` provided in the `config.txt`.

Outputs will appear in the folder named `optuna`. Every run is saved under unique name. After the run the best psnr is checked.
Then the following files are **moved** to the output folder:
* `PSNR_Test.txt`
* `PSNR_Train.txt`
* `MSE_Test.txt`
* `MSE_Train.txt` 

The `config.txt` is **copied** to the output folder.
 
Apart from that, the checkpoints stored in the `.\dump\save` that **correspond** to the best psnr will also be saved, so:
* `<best_psnr_iter>.GC(1-4)`
* `<best_psnr_iter>.m(1-4)`
* `<best_psnr_iter>.v(1-4)`

Warning! Then the folder  `.\dump\save` is **cleared** preparing for the next run.

`optuna.log` will keep mapping of unique folder name to the psnr achieved by the run.

The final folder structure will look like this:
```
├── WindowsApp
│   ├── WindowsApp
│   │   ├── models
│   │   │   ├── <dataset>
│   │   │   │   ├── optuna
│   │   │   │   │   ├── optuna.log
│   │   │   │   │   ├── <unique_name_1>
│   │   │   │   │   │   ├── <best_psnr_iter>.GC(1-4)
│   │   │   │   │   │   ├── <best_psnr_iter>.m(1-4)
│   │   │   │   │   │   ├── <best_psnr_iter>.v(1-4)
│   │   │   │   │   │   ├── config.txt
│   │   │   │   │   │   ├── MSE_test.txt
│   │   │   │   │   │   ├── MSE_train.txt
│   │   │   │   │   │   ├── PSNR_test.txt
│   │   │   │   │   │   ├── PSNR_train.txt
│   │   │   │   │   ├── <unique_name_2>
         .
         .
         .
│   │   │   │   │   ├── <unique_name_n>
```
