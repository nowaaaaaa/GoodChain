import re

def validate_username(username):
    if len(username) < 4:
        return False
    elif len(username) > 12:
        return False
    elif not re.fullmatch(r"[a-zA-Z_]", username[0]):
        return False
    elif len(re.findall(r"[a-zA-Z0-9_'\.]", username)) != len(username):
        return False
    return True

def validate_password(password):
    if len(password) < 6:
        return False
    elif len(password) > 30:
        return False
    elif len(re.findall(r"[(a-z)+(A-Z)+(0-9)+(~!@#`\$%&_\-\+=`\|\\\(\)\{\}\[\]:;'<>,\.\?/)+]", password)) != len(password) :
        return False
    elif re.search(r"[a-z]", password) is None:
        return False
    elif re.search(r"[0-9]", password) is None:
        return False
    return True