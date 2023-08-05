#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : SimpleOptimizer
# @Time         : 2020/9/8 8:14 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import json
import optuna
import numpy as np

from optuna.samplers import TPESampler
from sklearn.metrics import f1_score

optuna.logging.set_verbosity(optuna.logging.ERROR)


class SimpleOptimizer(object):

    def __init__(self, y_true, y_pred, **kwargs):
        self.y_true = y_true
        self.y_pred = y_pred

    # 定义其他变量
    def get_vars(self):
        pass

    # 重写该方法即可
    def __objective(self, trial: optuna.trial.Trial):
        # threshold = trial.suggest_uniform('threshold', 0, 1)

        threshold = trial.suggest_discrete_uniform('threshold', 0.001, 1, 0.001)
        y_pred_ = np.where(self.y_pred > threshold, 1, 0)
        score = f1_score(self.y_true, y_pred_)
        return score

    def run(self, trials=1, n_jobs=1, plot=True, gc_after_trial=False, seed=777):
        show_progress_bar = False if n_jobs > 1 else True

        self.study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=seed))
        self.study.optimize(
            self.__objective,
            n_trials=trials,
            gc_after_trial=gc_after_trial,
            show_progress_bar=show_progress_bar,
            n_jobs=n_jobs
        )

        if plot:
            print(f"best_params:\n{json.dumps(self.study.best_params, indent=4)}")
            return self._plot()

    def _plot(self):
        # optuna.visualization.plot_slice(self.study)
        _ = optuna.visualization.plot_optimization_history(self.study)

        # optuna.visualization.plot_param_importances(self.study)
        # optuna.visualization.plot_edf(self.study)
        # optuna.visualization.plot_parallel_coordinate(self.study)
        return _
