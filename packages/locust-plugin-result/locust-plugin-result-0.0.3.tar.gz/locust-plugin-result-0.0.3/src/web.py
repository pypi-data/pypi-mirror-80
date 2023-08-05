# -*- coding: utf-8 -*-

import locust
from flask import jsonify


def add_listener():
    @locust.events.init.add_listener
    def on_locust_init(environment, **kw):
        if environment.web_ui is None:
            # Don't add route on worker nodes, they do not have a web ui
            return

        @environment.web_ui.app.route("/status")
        @environment.web_ui.auth_required_if_enabled
        def status():
            runner = environment.runner
            return jsonify({
                "state": runner.state,
                "result": getattr(runner, 'result', None),
                "worker_count": getattr(runner, 'worker_count', None),  # 'worker_count' does not exist for LocalRunner
                "user_count": runner.user_count,
            })
