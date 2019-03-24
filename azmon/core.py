from datetime import datetime, timedelta
from .tools import datatools


class Metrics(object):
    """
    See: https://docs.microsoft.com/en-us/azure/azure-monitor/platform/metrics-supported
    """
    def __init__(self, client, resource_id):
        self._client = client
        self._resource_id = resource_id

    @classmethod
    def create_interface(cls, client, resource_id, interface):
        metrics = cls(client, resource_id)
        return interface(metrics)

    def list_definitions(self):
        for item in self._client.metric_definitions.list(self._resource_id):
            print(item.name)

    def list_metrics(self, metric_names, aggregation):
        """
        valid aggregations: Average, Total, Maximum, Minimum, Count
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)

        data = self._client.metrics.list(
            resource_uri=self._resource_id,
            timespan=f'{start_time}/{end_time}',
            #interval='PT1H',
            #interval='PT1M',
            interval='PT5M',
            metricnames=metric_names,
            aggregation=aggregation,
        )

        result = [
            datatools.dict_clean({
                'name': item.name.localized_value,
                'unit': item.unit.name,
                'timestamp': ts_data_item.time_stamp,
                'total': ts_data_item.total,
                'average': ts_data_item.average,
                'count': ts_data_item.count,
                'maximum': ts_data_item.maximum,
                'minimum': ts_data_item.minimum,
            })
            for item in data.value
            for ts_item in item.timeseries
            for ts_data_item in ts_item.data
        ]

        return result


class CosmosMetrics(object):
    def __init__(self, metrics):
        self._metrics = metrics

    def total_request_units(self):
        """
        From: https://docs.microsoft.com/en-us/azure/azure-monitor/platform/metrics-supported
        Used to monitor Total RU usage at a minute granularity. To get average RU consumed per second, use Total aggregation at minute and divide by 60.
        """
        return self._metrics.list_metrics('TotalRequestUnits', 'Total')

    def ru_per_s(self):
        """
        Custom metric derived from total_request_units
        """
        data = self.total_request_units()
        return [ { **item, 'RUs': item['total'] / 60 } for item in data ]

    def data_usage(self):
        """
        From: https://docs.microsoft.com/en-us/azure/azure-monitor/platform/metrics-supported
        Used to monitor total data usage at collection and region, minimum granularity should be 5 minutes.

        """
        return self._metrics.list_metrics('DataUsage', 'Total')
