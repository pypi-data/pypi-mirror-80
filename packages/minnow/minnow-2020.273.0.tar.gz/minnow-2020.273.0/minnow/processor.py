# vim: expandtab tabstop=4 shiftwidth=4

import logging

from pathlib import Path

from .utils import list_pairs_at_path

class Processor:
    def __init__(self, input_path: Path, output_path: Path) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.DEBUG)

    def process(self, metadata_path: Path, data_path: Path, output_path: Path) -> None:
        self.logger.info('Received {mp} and {dp}, with output path {op}'.format(mp=metadata_path, dp=data_path, op=output_path))
        self.logger.error('process() not defined')

    def run(self):
        for pair in list_pairs_at_path(self.input_path):
            if not pair.metadata_path.exists():
                self.logger.error('Metadata path does not exist: {}'.format(pair.metadata_path))
            elif not pair.data_path.exists():
                self.logger.error('Data path does not exist: {}'.format(pair.data_path))
            else:
                self.process(pair.metadata_path, pair.data_path, self.output_path)
