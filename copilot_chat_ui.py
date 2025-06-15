import os
import customtkinter as ctk

from copilot_api import CopilotAPI, load_project_summary


class CopilotChatUI(ctk.CTk):
    """Simple desktop UI to chat with GitHub Copilot."""

    def __init__(self, api: CopilotAPI):
        super().__init__()
        self.api = api
        self.context = load_project_summary()
        self.messages = [
            {"role": "system", "content": self.context}
        ]
        self.title("Copilot Chat")
        self.geometry("600x500")

        self.chat_log = ctk.CTkTextbox(self, width=580, height=420)
        self.chat_log.pack(padx=10, pady=10)

        self.entry = ctk.CTkEntry(self, width=480)
        self.entry.pack(side="left", padx=10, pady=10)
        self.send_btn = ctk.CTkButton(self, text="Send", command=self.send)
        self.send_btn.pack(side="left")

    def send(self) -> None:
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, "end")
        self.chat_log.insert("end", f"You: {user_text}\n")
        self.chat_log.see("end")

        self.messages.append({"role": "user", "content": user_text})
        try:
            response = self.api.chat(self.messages)
        except Exception as exc:  # pragma: no cover - network
            response = f"Error: {exc}"
        self.messages.append({"role": "assistant", "content": response})
        self.chat_log.insert("end", f"Copilot: {response}\n")
        self.chat_log.see("end")


if __name__ == "__main__":
    token = os.environ.get("COPILOT_TOKEN")
    if not token:
        raise SystemExit("Set the COPILOT_TOKEN environment variable.")
    api = CopilotAPI(token)
    app = CopilotChatUI(api)
    app.mainloop()
