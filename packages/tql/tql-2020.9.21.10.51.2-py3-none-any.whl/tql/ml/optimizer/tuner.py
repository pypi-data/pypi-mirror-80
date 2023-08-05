#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : LGBMClassifierTuner
# @Time         : 2020/9/21 10:19 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import optuna
import numpy as np
import pandas as pd

from sklearn.metrics import roc_auc_score
import catboost

import lightgbm as lgb
from lightgbm import LGBMClassifier

from tql.ml.oof import LGBMClassifierOOF
from tql.ml.optimizer.BaseOptimizer import BaseOptimizer


class LGBMClassifierTuner(BaseOptimizer):

    def __init__(self, X, y, params=None, feval=roc_auc_score):
        self.X = X
        self.y = y
        self.params = params
        self.feval = feval

    def _objective(self, trial: optuna.trial.Trial):
        opt_params = dict(
            num_leaves=trial.suggest_int("num_leaves", 2, 2 ** 8),
            learning_rate=trial.suggest_discrete_uniform('learning_rate', 0.001, 1, 0.001),
            n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),

            min_child_samples=trial.suggest_int('min_child_samples', 2, 2 ** 8),
            min_child_weight=trial.suggest_loguniform('min_child_weight', 1e-8, 1),
            min_split_gain=trial.suggest_loguniform('min_split_gain', 1e-8, 1),

            subsample=trial.suggest_uniform('subsample', 0.4, 1),
            subsample_freq=trial.suggest_int("subsample_freq", 0, 2 ** 4),
            colsample_bytree=trial.suggest_uniform('colsample_bytree', 0.4, 1),
            reg_alpha=trial.suggest_loguniform('reg_alpha', 1e-8, 10),
            reg_lambda=trial.suggest_loguniform('reg_lambda', 1e-8, 10),
        )
        cv = trial.suggest_int('cv', 2, 2 ** 4)

        if self.params is not None:
            opt_params.update(self.params)

        clf_oof = LGBMClassifierOOF(self.X, self.y, params=opt_params, cv=cv, feval=self.feval)
        clf_oof.run()

        return clf_oof.oof_score
