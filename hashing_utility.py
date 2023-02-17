import bcrypt

def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)

"""
if __name__ == '__main__':
    # Test the above functions manually
    original_password = 'my_very_secureP4ssword!'  # From registration form
    print('original_password: ' + original_password)

    hashed_password = hash_password(original_password)  # This shall be saved in the DB
    print('hashed_password: ' + hashed_password)

    user_input_password = 'Hey Siri, what is my password?'  # From a login form, a mistyped input
    is_matching = verify_password(user_input_password, hashed_password)
    print('is_matching: ' + str(is_matching))

    user_input_password = 'my_very_secureP4ssword!'  # From a login form, the correct input
    is_matching = verify_password(user_input_password, hashed_password)
    print('is_matching: ' + str(is_matching))
"""