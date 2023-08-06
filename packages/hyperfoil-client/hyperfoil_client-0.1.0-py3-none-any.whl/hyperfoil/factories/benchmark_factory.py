import io
from typing import Union

import yaml


class BenchmarkFactory:
    def __init__(self):
        self._benchmark = {'http': []}

    def create(self):
        return self._benchmark

    def load_benchmark(self, stream: Union[io.StringIO, io.FileIO]) -> 'BenchmarkFactory':
        benchmark = yaml.load(stream, Loader=yaml.Loader)
        self._benchmark.update(benchmark)
        return self

    def add_host(self, host: str, shared_connections: int, **kwargs) -> 'BenchmarkFactory':
        self._benchmark['http'].append({
            host: host,
            shared_connections: shared_connections,
            **kwargs
        })
        return self
