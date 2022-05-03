from image_data_generator import ImageDataGenerator, InitImageDataGenerator
from json_reader import MatrixSettingsReader, InitImagesReader
from json_writer import JsonWriter
from manager import ImageManager, OrderManager
from pathlib import Path
from subprocess import PIPE, Popen
from time import sleep
import threading
import signal

PROCESS = str(Path(__file__, '..', '..', 'rpi-rgb-led-matrix', 'examples-api-use',
                   'image-example').resolve())
RESOURCES_FOLDER = Path(__file__, '..', '..', 'resources').resolve()
IMAGES_FOLDER = Path(__file__, '..', '..', 'images').resolve()
INIT_IMAGES_JSON = RESOURCES_FOLDER / 'init_images.json'
MATRIX_SETTINGS_JSON = RESOURCES_FOLDER / 'matrix_settings.json'
EVENT_LOOP = str(Path(__file__, '..', 'event_loop.py').resolve())


def setup(writer: JsonWriter) -> None:
    ''' create the init_images.json if it doesn't exist
    '''
    if not INIT_IMAGES_JSON.exists():
        init_image_data_generator = InitImageDataGenerator()
        writer.write(INIT_IMAGES_JSON,
                     init_image_data_generator.generate_init_images_json(IMAGES_FOLDER))


def run(process: str, matrix_settings: list, image_manager: ImageManager, order_manager: OrderManager):
    proc = None
    cmd = [PROCESS] + matrix_settings + [None]
    t = threading.current_thread()
    while getattr(t, "running", True):
        current = order_manager.next()
        duration = image_manager.get_duration(current)
        path = image_manager.get_image_full_path(current)
        cmd[-1] = str(path)
        print(cmd)
        proc = Popen(cmd)
        sleep(duration)
        proc.kill()

    if proc:
        proc.kill()


def main():
    writer = JsonWriter()
    setup(writer)

    matrix_reader = MatrixSettingsReader(MATRIX_SETTINGS_JSON)
    init_images_reader = InitImagesReader(INIT_IMAGES_JSON)
    image_data_generator = ImageDataGenerator()

    matrix_settings = matrix_reader.get_settings()
    image_manager = ImageManager(init_images_reader.get_images())
    order_manager = OrderManager(init_images_reader.get_order())

    t = threading.Thread(target=run, args=(
        PROCESS, matrix_settings, image_manager, order_manager))
    t.start()

    def signal_handler(signal, frame):
        forever.set()
        t.running = False

    signal.signal(signal.SIGINT, signal_handler)
    forever = threading.Event()
    forever.wait()


if __name__ == "__main__":
    main()
