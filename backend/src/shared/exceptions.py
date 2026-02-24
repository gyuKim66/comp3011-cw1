"""
Author: Dongwook Kim
Created: 2026-02-24

Shared exception types.
"""


class DomainError(Exception):
    pass


class NotFoundError(DomainError):
    pass


class ValidationError(DomainError):
    pass
