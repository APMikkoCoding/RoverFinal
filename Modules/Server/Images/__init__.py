import FindObjects

def evauluate_image(file_path) -> list:
    objects = FindObjects.Objects()
    return objects.make_list(file_path)
