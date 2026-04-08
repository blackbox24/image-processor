from rest_framework.throttling import UserRateThrottle


class ImageTransFormationLimiter(UserRateThrottle):
    rate = "5/minute"
