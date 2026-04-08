import hashlib
import json


def get_transformation_cache_key(image_id, data):
    param_str = json.dumps(data, sort_keys=True)
    param_hash = hashlib.md5(param_str.encode()).hexdigest()
    return f"img_transform_{image_id}_{param_hash}"
