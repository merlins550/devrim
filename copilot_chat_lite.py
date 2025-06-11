import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
from copilot_bridge import CopilotBridge


class CopilotChatApp:
    """Minimal desktop chat UI forwarding prompts to VS Code Copilot."""

    def __init__(self, workspace: str | Path):
        self.bridge = CopilotBridge(workspace)
        self.root = tk.Tk()
        self.root.title("Copilot Lite Chat")
        self.history = ScrolledText(self.root, width=80, height=20, state="disabled")
        self.history.pack(padx=10, pady=10)
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(fill="x", padx=10)
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(entry_frame, textvariable=self.input_var)
        self.entry.pack(side="left", fill="x", expand=True)
        send_btn = tk.Button(entry_frame, text="Send", command=self.send_message)
        send_btn.pack(side="right", padx=5)
        self.entry.bind("<Return>", lambda _event: self.send_message())

    def append_history(self, prefix: str, message: str) -> None:
        self.history.configure(state="normal")
        self.history.insert(tk.END, f"{prefix}: {message}\n")
        self.history.configure(state="disabled")
        self.history.see(tk.END)

    def send_message(self) -> None:
        text = self.input_var.get().strip()
        if not text:
            return
        self.append_history("You", text)
        self.input_var.set("")
        response = self.bridge.ask(text)
        self.append_history("Copilot", response)

    def run(self) -> None:
        self.entry.focus()
        self.root.mainloop()


def main() -> None:
    workspace = Path.cwd()
    app = CopilotChatApp(workspace)
    app.run()


if __name__ == "__main__":
    main()
