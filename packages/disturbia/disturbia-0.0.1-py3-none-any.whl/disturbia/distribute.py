import random
from datetime import datetime


def distribute(distributions):

    random.seed(datetime.now())

    usages = {obj: count for (obj, count) in distributions}

    while {obj: count for obj, count in usages.items() if count > 0}:
        choices = {obj: count for obj, count in usages.items() if count > 0}.keys()
        choice = random.choice(list(choices))
        yield choice
        usages[choice] -= 1
