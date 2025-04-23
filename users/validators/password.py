import re

from rest_framework import serializers


def validate_password_policy(password):
    # 길이 검사
    if len(password) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")

    # 조합 조건 검사
    count = 0
    if re.search(r"[a-z]", password):
        count += 1
    if re.search(r"[A-Z]", password):
        count += 1
    if re.search(r"[0-9]", password):
        count += 1
    if count < 2:
        raise serializers.ValidationError("Password must include at least 2 types: uppercase, lowercase, numbers.")

    # 동일 문자 3회 이상 반복 금지 조건 검사
    if re.search(r"(.)\1\1", password):
        raise serializers.ValidationError("Password cannot contain the same character 3 times in a row.")

    # 연 문자 3개 이상 반복 금지 조건 검사
    sequences= [password[i:i + 3] for i in range(len(password) - 2)]
    for seq in sequences:
        if seq.isalpha() or seq.isdigit():
            if ord(seq[0]) + 1 == ord(seq[1]) and ord(seq[1]) + 1 == ord(seq[2]):
                raise serializers.ValidationError("Password cannot contain 3 or more consecutive characters.")

    return password
