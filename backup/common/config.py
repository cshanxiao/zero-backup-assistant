from pathlib import Path

import simplejson as json

import settings
from backup.common.util import HashUtil


class ConfigUtil:
    def __init__(self):
        # global_filters: 全局过滤器，过滤不需要备份的文件夹或文件
        self.config = {
            'global_filters': ['System Volume Information',
                               '$360Section',
                               '$RECYCLE.BIN',
                               '$LBak',
                               '$baksd',
                               'desktop.ini'
                               'hiberfil.sys',
                               'swapfile.sys',
                               'pagefile.sys',
                               ],
            'backup_paths': {}
        }
        self.config_path = Path(settings.RESOURCE_PATH) / 'config.json'
        self.config_file = self.config_path.as_posix()
        self.load_config()

    def load_config(self):
        # 载入配置文件
        if not self.config_path.exists():
            self.save_config()
            return

        with open(self.config_file, 'r') as fd:
            self.config = json.loads(fd.read())

    def update_path(self, source_path, target_path, backup_filter=None):
        # 添加备份路径
        source_path = source_path.strip()
        target_path = target_path.strip()
        backup_filter = backup_filter or []

        if not source_path:
            return

        backup_id = HashUtil.calculate_md5(source_path)
        config = {
            'id': backup_id,
            'source_path': source_path,
            'target_path': target_path,
            'backup_filter': backup_filter
        }
        self.config['backup_paths'][backup_id] = config
        self.save_config()

    def remove_path(self, source_path):
        # 移除备份路径
        source_path = source_path.strip()
        if not source_path:
            return

        backup_id = HashUtil.calculate_md5(source_path)
        if backup_id in self.config['backup_paths']:
            self.config['backup_paths'].pop(backup_id)
            self.save_config()

    def save_config(self):
        # 保存配置文件
        with open(self.config_file, 'w') as fd:
            fd.write(json.dumps(self.config))
