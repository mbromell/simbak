import logging as _logging
from simbak.backup.base import BackupBase as _BackupBase

_logger = _logging.getLogger(__name__)


class BackupNormal(_BackupBase):
    def __init__(self, sources: list, destinations: list, name: str,
                 compression_level: int = 6):
        """Initialize of the BackupNormal object

        Args:
            sources (list of str): Paths to the files that you are backing up.
            destinations (list of str): Paths of where you want the backup to
                be stored.
            name (str): Name of the backup, this will name the backup files.
            compression_level (int, optional): The gzip compression level that
                you want to use for the backup. Defaults to 6.
        """
        super().__init__(sources, destinations, name, compression_level)

    def backup(self):
        """Standard simbak backup.

        This will backup all the files defined in the sources and store them
        in a gzip'd file in each of the destinations. The name of the gzip file
        will be the name parameter suffixed with a time stamp, the format of
        the timestamp is YYYY-MM-DD--hh-mm-ss
        """
        _logger.info(f'Starting backup [{self.name}]')
        filtered_sources = self._filter_paths(self.sources)
        filtered_destinations = self._filter_paths(
            self.destinations, create=True)
        file_name = self._unique_file_name(self.name)
        _logger.info(f'Backup file name will be {self.name}')

        first_path = self._create_backup(
            filtered_sources,
            filtered_destinations[0],
            file_name,
            self.compression_level
        )
        self._distribute_backup(first_path, filtered_destinations[1:])