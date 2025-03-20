import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from drive_manager import get_drive_structure, upload_file, create_folder, download_file
import drive_auth

class GoogleDriveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Drive Manager")
        self.root.geometry("500x500")

        self.service = drive_auth.authenticate_google_drive()
        self.folder_dict = {}

        self.setup_ui()
        self.build_folder_tree()

    def setup_ui(self):
        frame_left = tk.Frame(self.root)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        frame_right = tk.Frame(self.root)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(frame_left)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.file_listbox = tk.Listbox(frame_right, height=10)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

        tk.Button(self.root, text="🔄 Refresh", command=self.build_folder_tree).pack(pady=5)
        tk.Button(self.root, text="📂 Create directory", command=self.create_folder).pack(pady=5)
        tk.Button(self.root, text="⬆️ Upload File", command=self.upload_file).pack(pady=5)
        tk.Button(self.root, text="⬇️ Download File", command=self.download_file).pack(pady=5)

    # def build_folder_tree(self):
    #     self.tree.delete(*self.tree.get_children())
    #     self.folder_dict.clear()
    #     root_node = self.tree.insert("", "end", "root", text="📁 Google Drive", open=True)
    #     self.folder_dict["root"] = None
    #     self.add_nodes(None, root_node)
    
    def build_folder_tree(self):
      self.tree.delete(*self.tree.get_children())
      self.folder_dict.clear()
      root_node = self.tree.insert("", "end", "root", text="📁 Google Drive", open=True)
      self.folder_dict["root"] = None
      self.add_nodes(None, root_node)

    def add_nodes(self, parent_id, parent_node):
        items = get_drive_structure(self.service, parent_id)
        for item in items:
            item_name = f"📂 {item['name']}" if item["mimeType"] == "application/vnd.google-apps.folder" else f"📄 {item['name']}"
            node = self.tree.insert(parent_node, "end", item["id"], text=item_name, open=False)
            self.folder_dict[item["id"]] = item["id"]
            if item["mimeType"] == "application/vnd.google-apps.folder":
                self.add_nodes(item["id"], node)

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        selected_folder_id = self.folder_dict.get(selected_item, None)
        self.list_files(selected_folder_id)

    def list_files(self, folder_id):
        self.file_listbox.delete(0, tk.END)
        files = get_drive_structure(self.service, folder_id)
        for file in files:
            if file["mimeType"] != "application/vnd.google-apps.folder":
                self.file_listbox.insert(tk.END, file["name"])

    def upload_file(self):
        selected_item = self.tree.focus()
        parent_id = self.folder_dict.get(selected_item, None)
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        upload_file(self.service, file_path, parent_id)
        messagebox.showinfo("Successfully", "File has been upload!")
        self.build_folder_tree()

    def create_folder(self):
        folder_name = simpledialog.askstring("Create Directory", "Enter new directory name:")
        if not folder_name:
            return

        selected_item = self.tree.focus()
        parent_id = self.folder_dict.get(selected_item, None)
        create_folder(self.service, folder_name, parent_id)
        messagebox.showinfo("Successfully", "Directory has been tạo!")
        self.build_folder_tree()

    def download_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if not selected_file:
            messagebox.showerror("Error", "You have not selected a file!")
            return

        results = self.service.files().list(q=f"name='{selected_file}'", fields="files(id, name)").execute()
        files = results.get("files", [])
        if not files:
            messagebox.showerror("Error", "File not found!")
            return

        file_id = files[0]["id"]
        save_path = filedialog.asksaveasfilename(initialfile=selected_file, defaultextension="")
        if not save_path:
            return

        download_file(self.service, file_id, selected_file, save_path)
        messagebox.showinfo("Successfully", f"File {selected_file} has been download {save_path}")
