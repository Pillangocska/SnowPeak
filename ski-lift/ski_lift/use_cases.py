"""Ski lift use cases."""

import os

from typing import List
from ski_lift.core.auth import BaseAuthenticator, InMemoryAuthenticator
from ski_lift.app.entity import SkiLiftController, SkiLiftAuthorizer
from ski_lift.core.controller import Controller
from ski_lift.core.engine import Engine


def create_controller() -> Controller:
    """Create a controller with an authorizer."""
    return SkiLiftController(
        engine=Engine(),
        authorizer=SkiLiftAuthorizer(authenticator=create_authenticate_from_env()),
    )


def create_authenticate_from_env() -> BaseAuthenticator:
    """Create authenticator from users defined in env variables."""
    workers_str: str = os.getenv('WORKER_OPERATORS', 'secret')
    workers: List[str] = workers_str.split(',')
    
    authenticator: BaseAuthenticator = InMemoryAuthenticator()
    for worker in workers:
        authenticator.add(worker)
    return authenticator