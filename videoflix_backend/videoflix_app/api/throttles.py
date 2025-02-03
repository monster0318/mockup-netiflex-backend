from rest_framework.throttling import UserRateThrottle


class EightyCallsPerSecond(UserRateThrottle):

    scope = 'eighty'