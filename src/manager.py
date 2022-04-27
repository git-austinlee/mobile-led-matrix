import uuid
from pathlib import Path


class ImageManager:
    def __init__(self, images):
        self.images = images

    def add_image(self, image_name: str, duration=10, visible=True) -> None:
        self.images[image_name] = {"duration": duration, "visible": visible}

    def delete_image(self, uuid: uuid):
        try:
            del self.images[uuid]
        except KeyError:
            pass

    def get_image_full_path(self, uuid: uuid) -> Path:
        return Path(self.images[uuid]['location'], self.images[uuid]['name'])

    def set_visible(self, image_name: str, visible: bool):
        raise NotImplementedError


class OrderManager:
    def __init__(self, order: list):
        self.order = order
        self.index = -1

    def append_order(self, image_uuid: uuid) -> None:
        self.order.append(image_uuid)

    def set_full_order(self, new_order: list) -> None:
        self.order = new_order

    def get_full_order(self) -> list:
        return self.order

    def remove_from_order(self, uuid) -> None:
        try:
            self.order.remove(uuid)
        except KeyError:
            pass

    def update_index(self) -> None:
        if self.index >= len(self.order):
            self.index = 0
        else:
            self.index += 1

    def next(self) -> uuid:
        self.update_index()
        return self.order[self.index]
