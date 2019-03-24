import click
from ..tools import clicktools


def commands(cosmos):
    @cosmos.command()
    @click.pass_obj
    @clicktools.handle_result
    def rups(metrics_client):
        """Cosmos DB Request Units per Second"""
        return metrics_client.ru_per_s()

    @cosmos.command()
    @click.pass_obj
    @clicktools.handle_result
    def ru(metrics_client):
        """Cosmos DB Request Units per Minute"""
        return metrics_client.total_request_units()

    @cosmos.command()
    @click.pass_obj
    @clicktools.handle_result
    def data(metrics_client):
        """Cosmos DB total data usage"""
        return metrics_client.data_usage()

    @cosmos.command()
    @click.pass_obj
    @clicktools.handle_result
    def documents(metrics_client):
        """Cosmos DB document count"""
        return metrics_client.document_count()
