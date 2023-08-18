from flask import send_file
import shutil
import os

class FileManager:
    # ...
    def __init__(self, config_repository):
        self.config_repository = config_repository

    def tree(self, disk, path):
        directories = self.get_directories_tree(disk, path)
        return {'result': {'status': 'success', 'message': None}, 'directories': directories}

    def upload(self, disk, path, files, overwrite):
        for file in files:
            if not overwrite and os.path.exists(os.path.join(disk, path, file.filename)):
                continue
            file.save(os.path.join(disk, path, file.filename))
        return {'result': {'status': 'success', 'message': 'uploaded'}}

    def delete(self, disk, items):
        for item in items:
            item_path = os.path.join(disk, item['path'])
            if os.path.exists(item_path):
                if item['type'] == 'dir':
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
        return {'result': {'status': 'success', 'message': 'deleted'}}

    def paste(self, disk, path, clipboard):
        # Logic for copying/cutting files and directories
        # This would depend on the specific structure of the clipboard object
        # ...
        return None

    def rename(self, disk, new_name, old_name):
        os.rename(os.path.join(disk, old_name), os.path.join(disk, new_name))
        return {'result': {'status': 'success', 'message': 'renamed'}}

    def download(self, disk, path):
        return send_file(os.path.join(disk, path), as_attachment=True)

    def preview(self, disk, path):
        # Assuming the file is an image
        return send_file(os.path.join(disk, path))

    def url(self, disk, path):
        # Assuming a public URL can be generated for the file
        return {'result': {'status': 'success', 'message': None}, 'url': os.path.join(disk, path)}

    def create_directory(self, disk, path, name):
        os.makedirs(os.path.join(disk, path, name))
        return {'result': {'status': 'success', 'message': 'dirCreated'}}

    def create_file(self, disk, path, name):
        open(os.path.join(disk, path, name), 'w').close()
        return {'result': {'status': 'success', 'message': 'fileCreated'}}

    def update_file(self, disk, path, file):
        file.save(os.path.join(disk, path, file.filename))
        return {'result': {'status': 'success', 'message': 'fileUpdated'}}

    def stream_file(self, disk, path):
        # Assuming the file is a video or audio file
        return send_file(os.path.join(disk, path))