import subprocess
import threading
import tkinter as tk
from tkinter import ttk

POWERSHELL_COMMAND = (
    "[System.Text.Encoding]::ASCII.GetString((Get-SecureBootUEFI db).Bytes)"
    " -match 'Windows UEFI CA 2023'"
)

COLOR_BG = "#1e1e2e"
COLOR_FG = "#cdd6f4"
COLOR_GREEN = "#a6e3a1"
COLOR_RED = "#f38ba8"
COLOR_YELLOW = "#f9e2af"
COLOR_SURFACE = "#313244"
COLOR_BTN = "#89b4fa"
COLOR_BTN_FG = "#1e1e2e"


def run_check(
    result_var: tk.StringVar,
    status_var: tk.StringVar,
    result_label: tk.Label,
    btn: tk.Button,
) -> None:
    btn.config(state=tk.DISABLED)
    status_var.set("チェック中...")
    result_var.set("")

    def task() -> None:
        try:
            proc = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", POWERSHELL_COMMAND],
                capture_output=True,
                timeout=30,
            )
            stdout = (proc.stdout or b"").decode("utf-8", errors="replace").strip()
            stderr = (proc.stderr or b"").decode("utf-8", errors="replace").strip()

            if proc.returncode != 0 and not stdout:
                raise RuntimeError(stderr or f"exit code {proc.returncode}")

            found = stdout.lower() == "true"
            btn.after(0, lambda: _update_ui(found, result_var, status_var, result_label, btn))
        except FileNotFoundError:
            btn.after(0, lambda: _show_error(
                "powershell.exe が見つかりません。\nWindows 環境で実行してください。",
                result_var, status_var, result_label, btn,
            ))
        except subprocess.TimeoutExpired:
            btn.after(0, lambda: _show_error(
                "タイムアウトしました（30秒）。",
                result_var, status_var, result_label, btn,
            ))
        except Exception as exc:
            msg = str(exc)
            btn.after(0, lambda: _show_error(msg, result_var, status_var, result_label, btn))

    threading.Thread(target=task, daemon=True).start()


def _update_ui(
    found: bool,
    result_var: tk.StringVar,
    status_var: tk.StringVar,
    result_label: tk.Label,
    btn: tk.Button,
) -> None:
    if found:
        result_var.set("✔  Windows UEFI CA 2023 が登録されています")
        status_var.set("result: True")
        result_label.config(foreground=COLOR_GREEN)
    else:
        result_var.set("✘  Windows UEFI CA 2023 が登録されていません")
        status_var.set("result: False")
        result_label.config(foreground=COLOR_RED)
    btn.config(state=tk.NORMAL)


def _show_error(
    msg: str,
    result_var: tk.StringVar,
    status_var: tk.StringVar,
    result_label: tk.Label,
    btn: tk.Button,
) -> None:
    result_var.set(f"エラー: {msg}")
    status_var.set("エラーが発生しました")
    result_label.config(foreground=COLOR_YELLOW)
    btn.config(state=tk.NORMAL)


def build_ui(root: tk.Tk) -> None:
    root.title("Secure Boot UEFI CA 2023 Checker")
    root.resizable(False, False)
    root.configure(bg=COLOR_BG)

    ttk.Style().theme_use("clam")

    padding = {"padx": 24, "pady": 12}

    # header
    header = tk.Frame(root, bg=COLOR_BG)
    header.pack(fill="x", **padding)

    tk.Label(
        header,
        text="Secure Boot UEFI CA 2023 Checker",
        font=("Yu Gothic UI", 14, "bold"),
        bg=COLOR_BG,
        fg=COLOR_FG,
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Secure Boot データベース (db) に Windows UEFI CA 2023 が\n含まれているかを確認します。",
        font=("Yu Gothic UI", 9),
        bg=COLOR_BG,
        fg=COLOR_FG,
        justify="left",
    ).pack(anchor="w", pady=(4, 0))

    ttk.Separator(root, orient="horizontal").pack(fill="x", padx=24)

    # result area
    result_frame = tk.Frame(root, bg=COLOR_SURFACE, bd=0)
    result_frame.pack(fill="x", padx=24, pady=16)

    result_var = tk.StringVar(value="「チェック開始」を押してください")
    result_label = tk.Label(
        result_frame,
        textvariable=result_var,
        font=("Yu Gothic UI", 11),
        bg=COLOR_SURFACE,
        fg=COLOR_FG,
        wraplength=420,
        justify="left",
        pady=16,
        padx=16,
    )
    result_label.pack(fill="x")

    # status bar
    status_var = tk.StringVar(value="待機中")
    tk.Label(
        root,
        textvariable=status_var,
        font=("Yu Gothic UI", 8),
        bg=COLOR_BG,
        fg="#6c7086",
        anchor="w",
    ).pack(fill="x", padx=24)

    # button row
    btn_frame = tk.Frame(root, bg=COLOR_BG)
    btn_frame.pack(fill="x", padx=24, pady=(8, 20))

    check_btn = tk.Button(
        btn_frame,
        text="チェック開始",
        font=("Yu Gothic UI", 10, "bold"),
        bg=COLOR_BTN,
        fg=COLOR_BTN_FG,
        activebackground="#74c7ec",
        activeforeground=COLOR_BTN_FG,
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2",
        bd=0,
    )
    check_btn.config(
        command=lambda: run_check(result_var, status_var, result_label, check_btn)
    )
    check_btn.pack(side="left")

    tk.Button(
        btn_frame,
        text="閉じる",
        font=("Yu Gothic UI", 10),
        bg=COLOR_SURFACE,
        fg=COLOR_FG,
        activebackground="#45475a",
        activeforeground=COLOR_FG,
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2",
        bd=0,
        command=root.destroy,
    ).pack(side="left", padx=(8, 0))

    # center window
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")


def main() -> None:
    root = tk.Tk()
    build_ui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
