"""Subcommand for running machine translation on a pod."""

import os
import click
from grow.commands import shared
from grow.pods import pods
from grow.pods import storage
from xtermcolor import colorize


@click.command()
@shared.pod_path_argument
@click.option('--locale', type=str, multiple=True)
def machine_translate(pod_path, locale):
    """Translates the pod message catalog using machine translation."""
    root = os.path.abspath(os.path.join(os.getcwd(), pod_path))
    pod = pods.Pod(root, storage=storage.FileStorage)
    with pod.profile.timer('grow_machine_translate'):
        pod.catalogs.extract()
        for identifier in locale:
            catalog = pod.catalogs.get(identifier)
            catalog.update()
            catalog.machine_translate()
        pod.logger.info(colorize(
            'WARNING! Use machine translations with caution.', ansi=197))
        pod.logger.info(colorize(
            'Machine translations are not intended for use in production.', ansi=197))
    return pod
