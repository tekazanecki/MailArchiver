import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
import os
from imap_module import login_to_imap, get_mail_folders, archive_emails


def browse_folder(folder_path):
    folder_selected = filedialog.askdirectory()  # Otwiera dialog wyboru folderu
    if folder_selected:  # Sprawdza, czy użytkownik wybrał folder
        folder_path.set(folder_selected)  # Aktualizuje zmienną tk.StringVar z wybraną ścieżką


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Archiver")
        self.style = ttk.Style()
        self.style.theme_use('darkly')  # Możesz zmienić temat na dowolny dostępny w ttkbootstrap

        # Ustawiamy okno jako nierozszerzalne przez użytkownika
        self.root.wm_resizable(False, False)

        self.folder_path = ttk.StringVar(root)
        self.setup_archive_folder(self.folder_path)

        self.frm_credentials = ttk.Frame(root)
        self.frm_credentials.pack(padx=20, pady=5)

        self.lbl_host = ttk.Label(self.frm_credentials, text="IMAP Host:")
        self.lbl_host.pack()
        self.ent_host = ttk.Entry(self.frm_credentials, justify=CENTER)
        self.ent_host.pack()
        self.ent_host.insert(0, "imap.gmail.com")  # Domyślna wartość

        self.lbl_email = ttk.Label(self.frm_credentials, text="Email:")
        self.lbl_email.pack()
        self.ent_email = ttk.Entry(self.frm_credentials, justify=CENTER)
        self.ent_email.pack()
        # self.ent_email.insert(0, "")

        self.lbl_login = ttk.Label(self.frm_credentials, text="Password:")
        self.lbl_login.pack()
        self.ent_password = ttk.Entry(self.frm_credentials, show="*", justify=CENTER)
        self.ent_password.pack()
        self.ent_password.bind('<KeyRelease>', self.validate_password)

        self.btn_login = ttk.Button(self.frm_credentials, text="Login", command=self.login, bootstyle=INFO)
        self.btn_login.pack(pady=5)
        self.btn_login.config(state=DISABLED)

        separator = ttk.Separator(root, orient='horizontal')
        separator.pack(fill='x', padx=20)

        self.frm_folders = ttk.Frame(root)
        self.frm_folders.pack(fill='both', expand=True, padx=5, pady=5)
        self.lbl_folders = ttk.Label(self.frm_folders, text="Folders with emails")
        self.lbl_folders.pack(padx=20, pady=20)
        self.folder_vars = {}

        separator = ttk.Separator(root, orient='horizontal')
        separator.pack(fill='x', padx=20)

        self.frm_path = ttk.Frame(root)
        self.frm_path.pack(padx=20, pady=5)

        self.lbl_location = ttk.Label(self.frm_path, text="Save location:")
        self.lbl_location.pack()

        self.ent_location = ttk.Entry(self.frm_path, textvariable=self.folder_path, width=50, justify=CENTER)
        self.ent_location.pack(padx=20)
        self.btn_browse = ttk.Button(self.frm_path, text="Wybierz folder",
                                     command=lambda folder_path=self.folder_path: browse_folder(folder_path),
                                     bootstyle=INFO)
        self.btn_browse.pack(pady=5)

        separator = ttk.Separator(root, orient='horizontal')
        separator.pack(fill='x', padx=20)

        self.btn_archive = ttk.Button(self.root, text="Archive", command=self.archive, bootstyle=SUCCESS)
        self.btn_archive.pack(padx=20, pady=20)

    def setup_archive_folder(self, folder_path):
        default_folder_path = os.path.abspath("archive")
        folder_path.set(default_folder_path)
        if not os.path.exists(default_folder_path):
            os.makedirs(default_folder_path)

    def login(self):
        # Usunięcie istniejących checkboxów, jeśli istnieją
        for widget in self.frm_folders.winfo_children():
            widget.destroy()

        try:
            self.login_to_imap()
            folders = get_mail_folders(self.imap)

            # Usunięcie istniejących checkboxów, jeśli istnieją
            for widget in self.frm_folders.winfo_children():
                widget.destroy()

            if not folders:
                # Wyświetlanie komunikatu o błędzie, jeśli brak folderów
                error_label = ttk.Label(self.frm_folders, text="No folders found.", foreground="red")
                error_label.pack()
                return

            # Przygotowanie nowej struktury ramek do pakowania checkboxów
            folder_frames = []  # lista ramek
            current_frame = ttk.Frame(self.frm_folders, width=100)
            current_frame.pack(side=LEFT, pady=5, fill=BOTH)
            folder_frames.append(current_frame)
            count = 0

            # Dodawanie checkboxów w ramkach
            for i, folder in enumerate(folders):
                if count >= 10:  # Jeśli osiągnięto limit 10 checkboxów w ramce
                    current_frame = ttk.Frame(self.frm_folders, width=100)
                    current_frame.pack(side=LEFT, pady=5, fill=BOTH)
                    folder_frames.append(current_frame)
                    count = 0  # Reset licznika dla nowej ramki
                var = ttk.BooleanVar()
                chk = ttk.Checkbutton(current_frame, text=folder, variable=var, width=30)
                chk.pack(anchor='w')
                self.folder_vars[folder] = var
                count += 1

            # Zmiana rozmiaru okna po zalogowaniu, zależnie od liczby folderów
            num_frames = len(folder_frames)
            window_height = 150 + num_frames * 40 + 220  # Podstawowa wysokość + 40px na każdy frame
            window_width = 200 * len(folder_frames)  # Szerokość okna
            self.root.geometry(f"{window_width}x{window_height}")

            self.imap.logout()
        except Exception as e:
            # W przypadku błędu połączenia lub innego błędu technicznego
            if not hasattr(self, 'lbl_error'):
                self.lbl_error = ttk.Label(self.frm_folders, text="Something went wrong: " + str(e), foreground="red")
                self.lbl_error.pack()

    def login_to_imap(self):
        host = self.ent_host.get()
        email = self.ent_email.get()
        password = self.ent_password.get()
        self.imap = login_to_imap(host, email, password)

    def archive(self):
        self.login_to_imap()
        selected_folders = [folder for folder, var in self.folder_vars.items() if var.get()]
        save_location = self.ent_location.get()
        try:
            archive_emails(self.imap, selected_folders, save_location, is_verbose=True)
        except Exception as e:
            print(f"Błąd archiwizacji: {e}")
        finally:
            try:
                self.imap.logout()
            except Exception as e:
                print(f"Błąd przy wylogowywaniu: {e}")

    def validate_password(self, event=None):
        if self.ent_password.get():
            self.btn_login.config(state=NORMAL)
        else:
            self.btn_login.config(state=DISABLED)


if __name__ == "__main__":
    root = ttk.Window(themename='darkly')  # Możesz zmienić temat na dowolny dostępny w ttkbootstrap
    app = App(root)
    root.mainloop()
