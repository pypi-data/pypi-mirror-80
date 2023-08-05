# GridSearch
A Brute-Force based GridSearch Tool

Installation：
    pip install BFSearch

Usage:

```
from BFSearch import GridSearch

def score(a, b, **params):
    return a ** 2 + b ** 2 - 2 * a * b


if __name__ == '__main__':
    param_grid = {
        'a': np.arange(10, 845, 5),
        'b': range(4, 200)
    }
    g = GridSearch(score, param_grid, verbose=False)
    best_param, best_score = g.run()
    print(best_param, best_score)
```