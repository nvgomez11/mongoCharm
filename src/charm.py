#!/usr/bin/env python3
# Copyright 2020 Ubuntu
# See LICENSE file for licensing details.

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.charm import CharmBase
from ops.model import ActiveStatus

from charms.reactive import when, when_not, set_flag
from charmhelpers.core.hookenv import status_set
import charms.apt


logger = logging.getLogger(__name__)


class WordpressCharm(CharmBase):
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_config_changed)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.fortune_action, self._on_fortune_action)
        self.framework.observe(self.on.mssql_ready, self)
        self._stored.set_default(things=[])

    def _on_config_changed(self, _):
        current = self.config["thing"]
        if current not in self._stored.things:
            logger.debug("found a new thing: %r", current)
            self._stored.things.append(current)

    def _on_fortune_action(self, event):
        fail = event.params["fail"]
        if fail:
            event.fail(fail)
        else:
            event.set_results({"fortune": "A bug in the code is worth two in the documentation."})

    def _on_msql_ready(self, event):
        pass

@when_not('apt.installed.wordpress')
def install_wordpress_apt():
    charms.apt.queue_install(['wordpress'])
    #sets the 'apt.installed.wordpress' flag when done

@when('apt.installed.wordpress')


@when_not('wordpress.ready')
def install_wordpress():
    status_set('blocked', "wordpress installed, waiting for database")
    set_flag('wordpress.ready')

@when_not('wordpress.ready')
@when_not('apt.installed.wordpress')
def waiting_for_wordpress():
    status_set('maintenance', "waiting for apt wordpress installation")

if __name__ == "__main__":
    main(WordpressCharm)