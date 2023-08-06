def __init__(hub):
    hub.pop.config.load(["pop_create"], cli="pop_create")


def cli(hub):
    print("pop-create works!")
