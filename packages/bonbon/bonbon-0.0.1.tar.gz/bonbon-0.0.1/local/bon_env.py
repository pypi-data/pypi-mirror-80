import os


def plant_env(kv_dict):
    for k, v in kv_dict.items():
        k = f'BON_{k}' if not str(k).startswith('BON') else k
        os.environ[k] = v


def check_env():
    res = {}
    for k, v in os.environ.items():
        if str(k).startswith('BON'):
            res[k] = v
    return res


def clean_up_env():
    for k, v in os.environ.items():
        if str(k).startswith('BON'):
            del os.environ[k]


if __name__ == "__main__":
    print('### ghost ###')
