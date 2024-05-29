import sys

def sanitize_filename(filename):
    """
    Funkcja czyszcząca nazwę pliku z niedozwolonych znaków i skracająca długie nazwy.
    """
    import re
    filename = re.sub(r'[\\/*?:"<>|\r\n\t]+', '_', filename)
    return filename[:50]  # Skrócenie nazwy pliku, jeśli jest zbyt długa

def update_progress(progress_dict):
    bar_length = 50  # Możesz dostosować długość paska
    sys.stdout.write('\x1b[2J\x1b[H')
    main_progress = generate_update_text("main progress",
                                         progress_dict['total_progress']['step'],
                                         progress_dict['total_progress']['size'],
                                         bar_length)
    sys.stdout.write(main_progress + '\n')

    ended_progress_string = ""
    for category in progress_dict["ended_progress"]:
        ended_progress = generate_update_text(category, 100, 100, bar_length)
        ended_progress_string += ended_progress + '\n'

    current_progress = generate_update_text(progress_dict['current_progress']['name'],
                                            progress_dict['current_progress']['step'],
                                            progress_dict['current_progress']['size'],
                                            bar_length)

    sys.stdout.write('\r' + main_progress + '\r\n' + ended_progress_string + '\r\n' + current_progress + '\r')
    sys.stdout.flush()

def generate_update_text(progress_text, step, size, bar_length):
    progress = step / size
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1
    block = int(round(bar_length * progress))
    return "\r{0}: [{1}] {2}%".format(progress_text, "#" * block + "-" * (bar_length - block), progress * 100)
