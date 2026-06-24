import customtkinter as ctk
from tkinter import messagebox, simpledialog
import os
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

FILE_NAME = "savings.txt"
LICENSE_FILE = "license.txt"
GOAL = 10000

# ---------------- LICENSE ----------------
def load_license():
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            return f.read().strip() == "PREMIUM"
    return False


def activate_premium():
    code = simpledialog.askstring("Upgrade", "Enter Premium Code:")
    if code in ["VIP123", "UNLOCK2026"]:
        with open(LICENSE_FILE, "w") as f:
            f.write("PREMIUM")
        global PREMIUM
        PREMIUM = True
        messagebox.showinfo("Success", "Premium Unlocked 🚀")
    else:
        messagebox.showerror("Error", "Invalid Code")


PREMIUM = load_license()

# ---------------- DATA ----------------
def load_data():
    data = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            for line in f:
                try:
                    date, amount = line.strip().split(",")
                    data.append((date, int(amount)))
                except:
                    pass
    return data

savings_data = load_data()

# ---------------- LOGIC ----------------
def get_total():
    return sum(amount for _, amount in savings_data)


def save_amount():
    try:
        amount = int(entry.get())
        today = datetime.now().strftime("%Y-%m-%d")
        savings_data.append((today, amount))

        with open(FILE_NAME, "a") as f:
            f.write(f"{today},{amount}\n")

        entry.delete(0, "end")
        update_ui()
    except:
        messagebox.showerror("Error", "Enter a valid number")


# ---------------- PREMIUM ----------------
def show_stats():
    if not PREMIUM:
        messagebox.showinfo("Premium", "Upgrade to Premium 🚀")
        return

    amounts = [amt for _, amt in savings_data]
    if not amounts:
        return

    avg = sum(amounts) / len(amounts)
    highest = max(amounts)

    messagebox.showinfo("Stats", f"Average: ₹{avg:.2f}\nHighest: ₹{highest}")


def monthly_report():
    if not PREMIUM:
        messagebox.showinfo("Premium", "Upgrade to Premium 🚀")
        return

    report = {}
    for date, amt in savings_data:
        month = date[:7]
        report[month] = report.get(month, 0) + amt

    text = "\n".join([f"{m}: ₹{v}" for m, v in report.items()])
    messagebox.showinfo("Monthly Report", text)


# ---------------- UI UPDATE ----------------
def update_ui():
    total = get_total()
    total_label.configure(text=f"₹ {total}")

    percent = min(total / GOAL, 1)
    progress.set(percent)
    progress_label.configure(text=f"{int(percent*100)}% of ₹{GOAL}")

    # clear
    for widget in history_frame.winfo_children():
        widget.destroy()

    # cards
    for date, amount in savings_data[::-1]:
        card = ctk.CTkFrame(history_frame, corner_radius=12)
        card.pack(fill="x", padx=5, pady=6)

        left = ctk.CTkLabel(card, text=f"📅 {date}", anchor="w")
        left.pack(side="left", padx=12, pady=10)

        right = ctk.CTkLabel(card, text=f"₹{amount}", anchor="e", font=("Arial", 14, "bold"))
        right.pack(side="right", padx=12)


# ---------------- APP ----------------
app = ctk.CTk()
app.geometry("430x650")
app.title("PiggyBank 💸")

# HEADER CARD
header = ctk.CTkFrame(app, corner_radius=15)
header.pack(fill="x", padx=15, pady=10)

ctk.CTkLabel(header, text="Total Savings", font=("Arial", 12)).pack(pady=(10,0))

total_label = ctk.CTkLabel(header, text="₹ 0", font=("Arial", 32, "bold"))
total_label.pack(pady=5)

progress = ctk.CTkProgressBar(header, width=250)
progress.pack(pady=5)
progress.set(0)

progress_label = ctk.CTkLabel(header, text="0%", font=("Arial", 10))
progress_label.pack(pady=(0,10))

# INPUT CARD
input_card = ctk.CTkFrame(app, corner_radius=15)
input_card.pack(fill="x", padx=15, pady=10)

entry = ctk.CTkEntry(input_card, placeholder_text="Enter amount", justify="center")
entry.pack(pady=10, padx=10)

ctk.CTkButton(input_card, text="➕ Add Money", command=save_amount).pack(pady=(0,10))

# PREMIUM CARD
premium_card = ctk.CTkFrame(app, corner_radius=15)
premium_card.pack(fill="x", padx=15, pady=10)

ctk.CTkButton(premium_card, text="🚀 Upgrade to Premium", fg_color="orange", command=activate_premium).pack(pady=5, padx=10, fill="x")
ctk.CTkButton(premium_card, text="📊 View Stats", command=show_stats).pack(pady=5, padx=10, fill="x")
ctk.CTkButton(premium_card, text="📅 Monthly Report", command=monthly_report).pack(pady=5, padx=10, fill="x")

# HISTORY
ctk.CTkLabel(app, text="Recent Activity", font=("Arial", 14, "bold")).pack(pady=5)

history_frame = ctk.CTkScrollableFrame(app, height=250)
history_frame.pack(fill="both", expand=True, padx=15, pady=10)

update_ui()

app.mainloop()
