from rest_framework.throttling import UserRateThrottle


class BurstLimit(UserRateThrottle):

    scope = 'user_burst'

class SustainedLimit(UserRateThrottle):

    scope = 'user_sustained'