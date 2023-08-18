class ConfigRepository:
    def __init__(self):
        # Initialize with default configurations or load from a file, database, etc.
        self.config = {
            'acl': [],
            'left_disk': 'local',
            'right_disk': 'remote',
            # ... other configurations
        }

    def get_acl(self):
        return self.config['acl']

    def get_left_disk(self):
        return self.config['left_disk']

    def get_right_disk(self):
        return self.config['right_disk']

    def get_disk_list(self):
        return self.config['disks']

    def get_cache(self):
        return self.config['cache']

    # ... other methods to access specific configurations
