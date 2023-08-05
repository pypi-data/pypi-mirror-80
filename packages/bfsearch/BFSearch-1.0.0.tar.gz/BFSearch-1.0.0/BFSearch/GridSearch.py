# coding=utf-8
from itertools import product


class GridSearch(object):
    def __init__(self, obj_func, param_grid, verbose=True):
        self.obj_func = obj_func
        self.param_keys = param_grid.keys()
        self.param_values = [param_grid[k] for k in self.param_keys]
        self.best_param = {}
        self.best_score = -float('inf')
        self.verbose = verbose

    def run(self):
        for item in product(*self.param_values):
            param = dict(zip(self.param_keys, item))
            score = self.obj_func(**param)
            if self.verbose:
                print("param={0}\nscore={1}\n".format(param, score))
            if score > self.best_score:
                self.best_score = score
                self.best_param = param
        return self.best_param, self.best_score


if __name__ == '__main__':
    def score_func(a, b, **params):
        return a ** 2 + b ** 2 - 2 * a * b


    param_grid = {
        'a': range(10, 845),
        'b': range(4, 200)
    }

    g = GridSearch(score_func, param_grid)
    best_param, best_score = g.run()
    print(best_param, best_score)
