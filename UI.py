import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from MainFunctions import IdentityVerificationSystem


class IdentityVerificationUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.system = IdentityVerificationSystem()

        self.title("Blockchain Identity Verification By Clyde")
        self.geometry("900x600")
        self.configure(bg="#f5f5f5")

        self.resizable(False, False)

        self.setupUI()

        # Set up closing event handler
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setupUI(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.register_tab = ttk.Frame(self.notebook)
        self.verify_tab = ttk.Frame(self.notebook)
        self.blockchain_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.register_tab, text="Register Identity")
        self.notebook.add(self.verify_tab, text="Verify Identity")
        self.notebook.add(self.blockchain_tab, text="Blockchain Explorer")

        self.setup_register_tab()
        self.setup_verify_tab()
        self.setup_blockchain_tab()

    def setup_register_tab(self):
        form_frame = ttk.LabelFrame(self.register_tab, text="Identity Registration")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Date of Birth:", "dob"),
            ("Email:", "email"),
            ("Address:", "address")
        ]

        self.register_entries = {}

        for i, (label_text, field_name) in enumerate(fields):
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=i, column=0, sticky=tk.W, padx=10, pady=10)

            if field_name == "dob":
                entry = DateEntry(form_frame, width=47, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(form_frame, width=50)

            entry.grid(row=i, column=1, sticky=tk.W, padx=10, pady=10)
            self.register_entries[field_name] = entry

        register_button = ttk.Button(form_frame, text="Register Identity", command=self.register_identity)
        register_button.grid(row=len(fields), column=0, columnspan=2, pady=20)

        self.register_result_frame = ttk.LabelFrame(self.register_tab, text="Registration Result")
        self.register_result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.register_result_text = tk.Text(self.register_result_frame, height=10, wrap=tk.WORD)
        self.register_result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.register_result_text.config(state=tk.DISABLED)

    def setup_verify_tab(self):

        verify_frame = ttk.LabelFrame(self.verify_tab, text="Identity Verification")
        verify_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        id_label = ttk.Label(verify_frame, text="Identity ID:")
        id_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        self.id_entry = ttk.Entry(verify_frame, width=50)
        self.id_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)

        key_label = ttk.Label(verify_frame, text="Private Key (for challenge response):")
        key_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

        self.key_entry = ttk.Entry(verify_frame, width=50)
        self.key_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

        self.verification_type = tk.StringVar(value="simple")

        simple_radio = ttk.Radiobutton(verify_frame, text="Simple Verification", variable=self.verification_type,
                                       value="simple")
        simple_radio.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        challenge_radio = ttk.Radiobutton(verify_frame, text="Challenge-Response Verification",
                                          variable=self.verification_type, value="challenge")
        challenge_radio.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

        verify_button = ttk.Button(verify_frame, text="Verify Identity", command=self.verify_identity)
        verify_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.verify_result_frame = ttk.LabelFrame(self.verify_tab, text="Verification Result")
        self.verify_result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.verify_result_text = tk.Text(self.verify_result_frame, height=10, wrap=tk.WORD)
        self.verify_result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.verify_result_text.config(state=tk.DISABLED)

    def setup_blockchain_tab(self):
        control_frame = ttk.Frame(self.blockchain_tab)
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        refresh_button = ttk.Button(control_frame, text="Refresh Blockchain Data", command=self.refresh_blockchain_data)
        refresh_button.pack(side=tk.LEFT, padx=10)

        validate_button = ttk.Button(control_frame, text="Validate Blockchain Integrity",
                                     command=self.validate_blockchain)
        validate_button.pack(side=tk.LEFT, padx=10)

        self.blockchain_data_frame = ttk.LabelFrame(self.blockchain_tab, text="Blockchain Data")
        self.blockchain_data_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.setup_blockchain_treeview()

    def setup_blockchain_treeview(self):
        self.blockchain_tree = ttk.Treeview(self.blockchain_data_frame)

        self.blockchain_tree["columns"] = ("index", "timestamp", "hash", "prev_hash")

        self.blockchain_tree.column("#0", width=50, stretch=tk.NO)
        self.blockchain_tree.column("index", width=50, anchor=tk.CENTER)
        self.blockchain_tree.column("timestamp", width=150, anchor=tk.W)
        self.blockchain_tree.column("hash", width=300, anchor=tk.W)
        self.blockchain_tree.column("prev_hash", width=300, anchor=tk.W)

        self.blockchain_tree.heading("#0", text="", anchor=tk.W)
        self.blockchain_tree.heading("index", text="Index", anchor=tk.CENTER)
        self.blockchain_tree.heading("timestamp", text="Timestamp", anchor=tk.W)
        self.blockchain_tree.heading("hash", text="Hash", anchor=tk.W)
        self.blockchain_tree.heading("prev_hash", text="Previous Hash", anchor=tk.W)

        scrollbar = ttk.Scrollbar(self.blockchain_data_frame, orient="vertical", command=self.blockchain_tree.yview)
        self.blockchain_tree.configure(yscrollcommand=scrollbar.set)

        self.blockchain_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_blockchain_data()

    def register_identity(self):
        user_data = {}
        for field, entry in self.register_entries.items():
            user_data[field] = entry.get()

        # debuggin
        print("User Data:", user_data)

        if not all(user_data.values()):
            messagebox.showerror("Registration Error", "All fields are required")
            return

        success, result = self.system.register_user(user_data)
        # debuggin
        print("Registration Success:", success)
        print("Registration Result:", result)

        self.register_result_text.config(state=tk.NORMAL)
        self.register_result_text.delete(1.0, tk.END)

        if success:
            output = f"Registration Successful!\n\n"
            output += f"Identity ID: {result['identity_id']}\n\n"
            output += "IMPORTANT: Save your private key securely. It's required for identity verification:\n"
            output += f"{result['private_key'][:20]}...(truncated)"

            self.refresh_blockchain_data()
        else:
            output = f"Registration Failed: {result['error']}"

        self.register_result_text.insert(tk.END, output)

        self.register_result_text.config(state=tk.DISABLED)

    def verify_identity(self):
        identity_id = self.id_entry.get()

        if not identity_id:
            messagebox.showerror("Verification Error", "Identity ID is required")
            return

        verification_type = self.verification_type.get()

        if verification_type == "simple":
            success, result = self.system.verify_user(identity_id)
        else:
            private_key = self.key_entry.get()

            if not private_key:
                messagebox.showerror("Verification Error", "Private Key is required for challenge verification")
                return

            challenge = self.system.generate_challenge()

            try:
                signature = self.system.identity_manager.sign_data(challenge, private_key)

                challenge_response = {
                    "challenge": challenge,
                    "signature": signature
                }

                success, result = self.system.verify_user(identity_id, challenge_response)
            except Exception as e:
                messagebox.showerror("Verification Error", f"Error in challenge-response: {str(e)}")
                return

        self.verify_result_text.config(state=tk.NORMAL)
        self.verify_result_text.delete(1.0, tk.END)

        if success and result.get("success", False):
            identity_data = result["identity_data"]

            output = f"Identity Verified Successfully!\n\n"
            output += f"Identity ID: {identity_data['identity_id']}\n"
            output += f"Name: {identity_data.get('first_name', '')} {identity_data.get('last_name', '')}\n"
            output += f"Email: {identity_data.get('email', '')}\n"
            output += f"Registered on: {identity_data.get('registration_date', '')}\n"
        else:
            error_msg = result.get("error", "Unknown error")
            output = f"Verification Failed: {error_msg}"

        self.verify_result_text.insert(tk.END, output)

        self.verify_result_text.config(state=tk.DISABLED)

    def refresh_blockchain_data(self):
        for item in self.blockchain_tree.get_children():
            self.blockchain_tree.delete(item)

        for i, block in enumerate(self.system.blockchain.chain):
            timestamp = datetime.fromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S")

            block_id = self.blockchain_tree.insert("", tk.END, text="", values=(
                block.index,
                timestamp,
                block.hash[:20] + "...",
                block.previousHash[:20] + "..."
            ))

            # Better display of identity data in the blockchain
            if isinstance(block.data, dict):
                # Dictionary to map technical field names to user-friendly labels
                field_labels = {
                    "first_name": "First Name",
                    "last_name": "Last Name",
                    "dob": "Date of Birth",
                    "email": "Email",
                    "address": "Address",
                    "public_key": "Public Key",
                    "registration_date": "Registration Date",
                    "identity_id": "Identity ID",
                    "registration_time": "Registration Time"
                }

                for key, value in block.data.items():
                    # Use the friendly label if available, otherwise use the original key
                    display_key = field_labels.get(key, key)

                    # Format the value based on its type
                    if key == "registration_time" and isinstance(value, (int, float)):
                        display_value = datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
                    elif isinstance(value, str) and len(value) > 50:
                        display_value = value[:50] + "..."
                    else:
                        display_value = value

                    self.blockchain_tree.insert(block_id, tk.END, text=display_key, values=("", "", display_value, ""))

    def validate_blockchain(self):
        is_valid = self.system.blockchain.is_chain_valid()

        if is_valid:
            messagebox.showinfo("Blockchain Validation", "The blockchain is valid and intact.")
        else:
            messagebox.showerror("Blockchain Validation", "The blockchain integrity check FAILED!")

    def on_closing(self):
        # Ensure blockchain is saved before closing
        try:
            self.system.blockchain.save_blockchain()
            print("Blockchain saved successfully on program exit")
        except Exception as e:
            print(f"Error saving blockchain on exit: {e}")

        self.destroy()