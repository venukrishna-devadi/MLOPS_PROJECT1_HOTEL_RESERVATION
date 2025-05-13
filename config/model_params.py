from scipy.stats import randint, uniform

RANDOM_SEARCH_PARAMS = {
    "n_iter":5,
    "cv":3,
    "n_jobs":1,
    "verbose":2,
    "random_state":99,
    "scoring":"accuracy"
}

HISTGB_PARAMS = {
    "learning_rate": uniform(0.01, 0.3),
    "max_iter": randint(100, 500),
    "max_depth": randint(3, 20),
    "min_samples_leaf": randint(20, 100),
    "l2_regularization": uniform(0.0, 1.0)
}