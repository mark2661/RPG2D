import pytmx.pytmx
from pyexcel_ods import get_data
import os
from settings import *
from pytmx.util_pygame import load_pygame
import json


def get_spawn_point_object_data(spawn_point_code: int) -> tuple[int, pytmx.pytmx.TiledObject]:
    # spawn point code = -1 indicates spawn not yet implemented
    if spawn_point_code != -1:
        file_extention = ".ods"
        ods_data = get_data(os.path.join(DATA_FILE_PATH, f"transition_spawn_point_mappings{file_extention}"))
        data = json.loads(json.dumps(ods_data))

        # print(data["spawn_point_mapping"])
        spawn_point_information = [info for info in data["spawn_point_mapping"] if info[0] == spawn_point_code][0]
        code, spawn_point_name, map_file, obj_id = spawn_point_information
        map_data = load_pygame(os.path.join(MAPS_FILE_PATH, map_file))
        spawn_point_object = map_data.get_object_by_id(obj_id)
        print(dir(spawn_point_object))
        print(spawn_point_object.x, spawn_point_object.y)
        map_id = int(map_file.split('.')[0])
        return (map_id, spawn_point_object)

    else:
        return None


def get_spawn_point_id(spawn_point_code: int) -> int:
    # spawn point code = -1 indicates spawn not yet implemented
    if spawn_point_code != -1:
        file_extention = ".ods"
        ods_data = get_data(os.path.join(DATA_FILE_PATH, f"transition_spawn_point_mappings{file_extention}"))
        data = json.loads(json.dumps(ods_data))

        spawn_point_information = [info for info in data["spawn_point_mapping"] if info[0] == spawn_point_code][0]
        obj_id = spawn_point_information[3]
        return obj_id

    else:
        return -1

# if __name__ == "__main__":
