"""Admin screen module for Airport ERP system with user management capabilities."""
from basewindow import BaseWindow
import customtkinter as ctk
from tkinter import ttk, messagebox
from config import get_logger, mydb

logger = get_logger(__name__)

class AdminScreen(BaseWindow):

    def __init__(self, root, view_manager=None, user_id=None, username=None):
        super().__init__(root, "Admin Panel", menu_buttons=["help", "about", "exit", "logout"])

        self.view_manager = view_manager
        self.user_id = user_id
        self.username = username
        self.selected_user = None
        self.cursor = mydb.cursor(dictionary=True)

        for widget in root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        self.frame_main = ctk.CTkFrame(root)
        self.frame_main.pack(fill="both", expand=True)

        self.frame_main.grid_columnconfigure(1, weight=1)
        self.frame_main.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self.frame_main, width=230)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        self.right_frame = ctk.CTkFrame(self.frame_main)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=0)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=0)

        self.bottom_button_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent", height=50)
        self.bottom_button_frame.grid(row=2, column=0, sticky="w", pady=(10, 0), padx=(10, 10))

        self.btn_add = ctk.CTkButton(self.bottom_button_frame, text="Add User", command=self._add_user)
        self.btn_add.grid(row=0, column=0, sticky="w", padx=(10, 10), pady=(10, 10))

        self.btn_edit = ctk.CTkButton(self.bottom_button_frame, text="Edit User", command=self._edit_user, state="disabled")
        self.btn_edit.grid(row=0, column=1, sticky="w", padx=(10, 10), pady=(10, 10))

        self.btn_delete = ctk.CTkButton(self.bottom_button_frame, text="Delete User", fg_color="red", command=self._delete_user, state="disabled")
        self.btn_delete.grid(row=0, column=2, sticky="w", padx=(10, 10), pady=(10, 10))

        self._create_header()
        self._create_users_table()
        self._fetch_users()

        self.menu_bar.lift()

    def _create_header(self):
        self.title_label = ctk.CTkLabel(
            self.right_frame,
            text="Admin Panel - User Management",
            font=("Arial", 25, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=(2, 30))

    def _create_users_table(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        fieldbackground="#2a2d2e",
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background="#3b3b3b",
                        foreground="white",
                        font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', '#22559b')])

        self.tree = ttk.Treeview(self.right_frame, show="headings", selectmode="browse")
        self.tree.grid(row=1, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.tree["columns"] = ["ID", "Username", "First Name", "Last Name", "Role"]
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.bind("<<TreeviewSelect>>", self._on_user_select)

    def _fetch_users(self):
        self.tree.delete(*self.tree.get_children())
        self.users_data = {}

        try:
            self.cursor.execute("SELECT id, username, role, first_name, last_name FROM users")
            for row in self.cursor.fetchall():
                values = [row["id"], row["username"], row["first_name"], row["last_name"], row["role"]]
                item_id = self.tree.insert("", "end", values=values)
                self.users_data[item_id] = row
        except Exception as e:
            logger.error(f"User fetch error: {str(e)}")
            messagebox.showerror("Error", "Failed to load user data")

    def _on_user_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            self.selected_user = None
            self.btn_edit.configure(state="disabled")
            self.btn_delete.configure(state="disabled")
            return

        try:
            item_id = selected_items[0]
            self.selected_user = self.users_data[item_id]
            self.btn_edit.configure(state="normal")
            self.btn_delete.configure(state="normal")
        except Exception as e:
            logger.error(f"User selection error: {str(e)}")
            messagebox.showerror("Error", "Could not process user data")
            self.selected_user = None

    def _add_user(self):
        self._open_user_form("Add User")

    def _edit_user(self):
        if self.selected_user:
            self._open_user_form("Edit User", self.selected_user)

    def _delete_user(self):
        if not self.selected_user:
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Delete user '{self.selected_user['username']}'?")
        if not confirm:
            return
        try:
            self.cursor.execute("DELETE FROM users WHERE id = %s", (self.selected_user["id"],))
            mydb.commit()
            self._fetch_users()
            self.selected_user = None
            self.btn_edit.configure(state="disabled")
            self.btn_delete.configure(state="disabled")
        except Exception as e:
            logger.error(f"Delete user error: {str(e)}")
            messagebox.showerror("Error", "Failed to delete user")

    def _open_user_form(self, title, user=None):
        form = ctk.CTkToplevel(self.frame_main)
        form.title(title)
        form.geometry("300x500")
        form.grab_set()

        ctk.CTkLabel(form, text="Username:").pack(pady=(20, 5))
        entry_username = ctk.CTkEntry(form)
        entry_username.pack()
        if user:
            entry_username.insert(0, user["username"])

        ctk.CTkLabel(form, text="Role:").pack(pady=(10, 5))
        entry_role = ctk.CTkEntry(form)
        entry_role.pack()
        if user:
            entry_role.insert(0, user["role"])

        ctk.CTkLabel(form, text="First Name:").pack(pady=(10, 5))
        entry_first_name = ctk.CTkEntry(form)
        entry_first_name.pack()
        if user:
            entry_first_name.insert(0, user["first_name"])

        ctk.CTkLabel(form, text="Last Name:").pack(pady=(10, 5))
        entry_last_name = ctk.CTkEntry(form)
        entry_last_name.pack()
        if user:
            entry_last_name.insert(0, user["last_name"])

        ctk.CTkLabel(form, text="Password:").pack(pady=(10, 5))
        entry_password = ctk.CTkEntry(form, show="*")
        entry_password.pack()
        if user:
            entry_password.insert(0, "")

        def save():
            username = entry_username.get().strip()
            role = entry_role.get().strip()
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            password = entry_password.get().strip()

            if not username or not role or not first_name or not last_name or (not user and not password):
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                if user:
                    # Update user
                    if password:
                        self.cursor.execute(
                            "UPDATE users SET username=%s, role=%s, first_name=%s, last_name=%s, password=%s WHERE id=%s",
                            (username, role, first_name, last_name, password, user["id"])
                        )
                    else:
                        self.cursor.execute(
                            "UPDATE users SET username=%s, role=%s, first_name=%s, last_name=%s WHERE id=%s",
                            (username, role, first_name, last_name, user["id"])
                        )
                else:
                    # Add user
                    self.cursor.execute(
                        "INSERT INTO users (username, role, first_name, last_name, password) VALUES (%s, %s, %s, %s, %s)",
                        (username, role, first_name, last_name, password)
                    )
                mydb.commit()
                self._fetch_users()
                form.destroy()
            except Exception as e:
                logger.error(f"Save user error: {str(e)}")
                messagebox.showerror("Error", "Failed to save user")

        ctk.CTkButton(form, text="Save", command=save).pack(pady=(20, 10))

    def cleanup(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'frame_main') and self.frame_main.winfo_exists():
            self.frame_main.destroy()

