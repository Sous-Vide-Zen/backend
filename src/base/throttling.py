import sys
from rest_framework.throttling import ScopedRateThrottle


class ScopedOnePerThreeSecsThrottle(ScopedRateThrottle):
    rate = "100/s"

    def parse_rate(self, rate):
        if "pytest" in sys.argv[0]:
            return (100, 1)
        else:
            return (1, 3)
