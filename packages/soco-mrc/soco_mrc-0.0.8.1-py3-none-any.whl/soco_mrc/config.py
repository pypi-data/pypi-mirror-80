import os
import json


class EnvVars(object):
    # system configuration
    region = os.environ.get("REGION", 'us')
    use_gpu = os.environ.get('USE_GPU', 'off') == 'on'
    api_key = os.environ.get('API_KEY', 'convmind')
    max_ans_len= os.environ.get('MAX_ANS_LEN', 64)

