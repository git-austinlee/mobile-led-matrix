import uuid
from pathlib import Path


class ImageManager:
    def __init__(self, images):
        self.images = images

    def add_image(self) -> None:
        raise NotImplementedError

    def delete_image(self, uuid: uuid) -> None:
        del self.images[uuid]

    def get_image_full_path(self, uuid: uuid) -> Path:
        return Path(self.images[uuid]['location'], self.images[uuid]['name'])

    def get_duration(self, uuid: uuid) -> int:
        return self.images[uuid]['duration']

    def set_duration(self, uuid: uuid, duration: int) -> None:
        self.images[uuid]['duration'] = duration

    def get_visible(self, uuid: uuid) -> bool:
        return self.images[uuid]['visible']

    def set_visible(self, uuid: uuid, visible: bool) -> None:
        self.images[uuid]['visible'] = visible


class OrderManager:
    def __init__(self, order: list):
        self.order = order
        self.index = -1

    def append_order(self, image_uuid: uuid) -> None:
        self.order.append(image_uuid)

    def get_full_order(self) -> list:
        return self.order

    def set_full_order(self, new_order: list) -> None:
        self.order = new_order

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
        print(self.index)
        return self.order[self.index]
