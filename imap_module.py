import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import os


def login_to_imap(host, email, password):
    imap = imaplib.IMAP4_SSL(host, port=993)
    imap.login(email, password)
    return imap


def get_mail_folders(imap):
    status, folders = imap.list()
    if status == 'OK':
        return [folder.decode('utf-8').split(' "/" ')[1][1:-1] for folder in folders]
    else:
        return []


def archive_emails(imap, selected_folders, save_location, is_verbose):
    from utils import sanitize_filename, update_progress

    progress_dict = {
        "total_progress": {"step": 0, "size": len(selected_folders)},
        "ended_progress": [],
        "current_progress": {"name": "", "step": 0, "size": 0}
    }
    try:
        error_msg = []
        for folder in selected_folders:
            status, _ = imap.select('"' + folder + '"')  # Wybiera folder na serwerze IMAP
            if status != 'OK':
                error_msg.append(f"Error selecting folder {folder}")
                continue

            status, messages = imap.search(None, 'ALL')  # Szuka wszystkich wiadomości w folderze
            if status != 'OK':
                error_msg.append(f"Error searching messages in folder {folder}")
                continue

            # Sprawdzenie i utworzenie katalogu dla folderu
            folder_path = os.path.join(save_location, folder.replace('/',
                                                                     '_'))  # Zastąpienie '/' znakiem '_', jeśli istnieje w nazwie folderu
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            list_of_messages = messages[0].split()
            number_of_messages = len(list_of_messages)
            progress_dict["current_progress"]["size"] = number_of_messages
            progress_dict['current_progress']['name'] = folder

            for idx, num in enumerate(list_of_messages):
                progress_dict["current_progress"]["step"] += 1
                if is_verbose:
                    update_progress(progress_dict)
                typ, data = imap.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                try:
                    msg = email.message_from_bytes(raw_email)
                    date_tuple = parsedate_to_datetime(msg['Date'])
                    date_str = date_tuple.strftime('%Y-%m-%d_%H-%M')
                    subject = decode_header(msg["subject"])[0][0]

                    if isinstance(subject, bytes):
                        subject = subject.decode(errors='ignore')  # Dekodowanie tematu, ignorowanie błędów
                    safe_subject = sanitize_filename(subject[:20])
                    subfolder_name = f"{date_str}_{safe_subject.replace(' ', '').replace('.', '')}"
                    filename = f"{subject[:40]}.eml"
                    subfolder_path = os.path.join(folder_path, subfolder_name)
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path)
                    else:
                        while os.path.exists(subfolder_path):
                            subfolder_path = subfolder_path + "_dub"
                        os.makedirs(subfolder_path)
                    filepath = os.path.join(subfolder_path, sanitize_filename(filename))  # Sanitizacja nazwy pliku
                    print(filepath)

                    # Zapisywanie treści emaila
                    with open(filepath, "wb") as f:
                        f.write(raw_email)

                    # Sprawdzanie załączników i zapisywanie ich
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" in content_disposition:
                                attachment_filename = part.get_filename()
                                if attachment_filename:
                                    attachment_path = os.path.join(subfolder_path,
                                                                   sanitize_filename(attachment_filename))
                                    with open(attachment_path, "wb") as af:
                                        af.write(part.get_payload(decode=True))

                except Exception as e:
                    error_msg.append(f"Error in folder {folder} saving message {subject}: {e}")

        progress_dict["total_progress"]["step"] += 1
        progress_dict["ended_progress"].append(folder)
    except imaplib.IMAP4.error as e:
        print(f"Błąd: {e}")
    finally:
        for msg in error_msg:
            print(msg)
