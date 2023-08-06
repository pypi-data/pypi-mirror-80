#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pop.hub


def pop_create():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="pop_create")
    hub.opts = hub.OPT["pop_create"]
    hub.pop_create.seed.new()
