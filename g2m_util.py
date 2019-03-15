def load_file(path_file_tuple):
    """
    :param path_file_tuple: A tuple of (path, filename) to load and read
    :return: an array of strings, one element per line in the file
    """
    file = f"{path_file_tuple[0]}/{path_file_tuple[1]}"
    with open(file, 'r') as myfile:
        content = myfile.readlines()
    return content


def get_root_level_gradle_file(gradle_files):
    """
    This is lame; but to work in both test and production situations
    (where the root level gradle file should always be "."), this
    just finds the shortest path in the list of gradle files and
    assumes that's the "root level" gradle file.
    :param gradle_files: A list of (path, filenames) of gradle-related
    files
    :return: The root level gradle file, or None if none can be found
    """
    shortest_path = 1024
    shortest_tuple = None
    for tuple in gradle_files:
        if len(tuple[0]) < shortest_path:
            shortest_path = len(tuple[0])
            shortest_tuple = tuple
    return shortest_tuple
