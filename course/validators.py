from rest_framework import serializers


def validator_scam_url(url):
    if not url.startswith('https://www.youtube.com/'):
        raise serializers.ValidationError('Нельзя использовать другой ресурс')
