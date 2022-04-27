from image_data_generator import ImageDataGenerator, InitImageDataGenerator
from json_reader import MatrixSettingsReader, InitImagesReader
from json_writer import JsonWriter
from manager import ImageManager, OrderManager
from pathlib import Path
import subprocess
from time import sleep

PROCESS = Path(__file__, '..', '..', '..', '..',
               'examples-api-use', 'image-example').resolve()
RESOURCES_FOLDER = Path(__file__, '..', '..', 'resources').resolve()
IMAGES_FOLDER = Path(__file__, '..', '..', 'images').resolve()
INIT_IMAGES_JSON = RESOURCES_FOLDER / 'init_images.json'
MATRIX_SETTINGS_JSON = RESOURCES_FOLDER / 'matrix_settings.json'


def setup(writer: JsonWriter) -> None:
    ''' create the init_images.json if it doesn't exist
    '''
    if not INIT_IMAGES_JSON.exists():
        init_image_data_generator = InitImageDataGenerator()
        writer.write(INIT_IMAGES_JSON,
                     init_image_data_generator.generate_init_images_json(IMAGES_FOLDER))


def run(matrix_settings: list, image_manager: ImageManager, order_manager: OrderManager):
    cmd = [PROCESS] + matrix_settings + \
        [str(image_manager.get_image_full_path(order_manager.next()))]
    proc = subprocess.Popen(cmd)
    try:
        while True:
            print(cmd)
            sleep(10)
            proc.kill()
            cmd[-1] = str(image_manager.get_image_full_path(order_manager.next()))
            proc = subprocess.Popen(cmd)
    except KeyboardInterrupt:
        proc.kill()


def main():
    writer = JsonWriter()
    matrix_reader = MatrixSettingsReader(MATRIX_SETTINGS_JSON)
    init_images_reader = InitImagesReader(INIT_IMAGES_JSON)
    image_data_generator = ImageDataGenerator()

    setup(writer)

    matrix_settings = matrix_reader.get_settings()
    image_manager = ImageManager(init_images_reader.get_images())
    order_manager = OrderManager(init_images_reader.get_order())

    run(matrix_settings, image_manager, order_manager)


if __name__ == "__main__":
    main()
