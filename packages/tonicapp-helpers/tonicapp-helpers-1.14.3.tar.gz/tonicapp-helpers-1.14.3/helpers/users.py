import hashlib

def get_user_id_with_uid(user_hash, salt="3CD13NwnvxQmwc3WLaeE"):
    """
      params: user_hash and salt
      return: user_id
    """
    user_list = {}

    while len(user_hash) < 32:
        user_hash = f'0{user_hash}'

    for i in range(100000):
        text = str(i) + salt
        hash_object = hashlib.md5(text.encode('utf-8'))
        user_list[hash_object.hexdigest()] = str(i)

    return user_list[user_hash]
