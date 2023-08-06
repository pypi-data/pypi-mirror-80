#!/usr/bin/env python3

__all__ = ['migrate']
from pgmigrator.migration import Migration


def migrate(conn, **kwargs):
    migration = Migration(conn, kwargs)
    migration.migrate()
