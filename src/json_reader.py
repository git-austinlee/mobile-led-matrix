import json
from pathlib import Path


class JsonReader:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath) as fs:
            self.data = json.load(fs)

    def re_read(self):
        self.__init__(self.filepath)


class MatrixSettingsReader(JsonReader):
    def __init__(self, filepath):
        super().__init__(filepath)

    def get_settings(self) -> list:
        ''' get the matrix params from the provided file
        '''
        res = []

        for k, v in self.data.items():
            v = str(v)
            if v == '':
                res.append(k)
            else:
                res.append(k + '=' + v)

        return res


class InitImagesReader(JsonReader):
    def __init__(self, filepath: Path):
        super().__init__(filepath)

    def get_images(self) -> dict:
        return self.data['images']

    def get_order(self) -> list:
        return self.data['order']
