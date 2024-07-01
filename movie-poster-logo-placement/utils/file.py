def save_file(file):
    open(file.name, 'wb').write(file.getbuffer())
    return file.name