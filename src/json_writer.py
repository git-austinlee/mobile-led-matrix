from pathlib import Path
import json


class JsonWriter:
    def write(self, filepath: Path, payload: dict) -> None:
        ''' convert payload to json and write to file
        '''
        with filepath.open('w') as fs:
            json.dump(payload, fs)
