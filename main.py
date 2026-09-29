"""
╔══════════════════════════════════════╗
║       PYTHON BANKING SYSTEM          ║
║   Data stored in lists (in-memory)   ║
╚══════════════════════════════════════╝
"""

import os
import datetime

# ─────────────────────────────────────────────
#  DATA STORE  (all lists)
# ─────────────────────────────────────────────
# Each user is a dictionary inside these lists:
#   users[i]        → { username, pin, name, balance }
#   transactions[i] → { username, type, amount, balance_after, date }

users = [
    {"username": "ali123",   "pin": "1234", "name": "Ali Khan",    "balance": 50000.0},
    {"username": "sara99",   "pin": "4321", "name": "Sara Ahmed",  "balance": 25000.0},
    {"username": "john007",  "pin": "0007", "name": "John Smith",  "balance": 100000.0},
]

transactions = []  # will be filled as users transact


# ─────────────────────────────────────────────
#  HELPER UTILITIES
# ─────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("=" * 50)
    print("        🏦  PYTHON NATIONAL BANK  🏦")
    print("=" * 50)


def divider():
    print("-" * 50)


def find_user(username):
    """Return user dict or None."""
    for u in users:
        if u["username"] == username:
            return u
    return None


def log_transaction(username, ttype, amount, balance_after):
    transactions.append({
        "username":      username,
        "type":          ttype,
        "amount":        amount,
        "balance_after": balance_after,
        "date":          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })


def get_user_transactions(username):
    return [t for t in transactions if t["username"] == username]


# ─────────────────────────────────────────────
#  PIN VERIFICATION  (asked every sensitive op)
# ─────────────────────────────────────────────
def verify_pin(user):
    """Ask for PIN and return True if correct, False otherwise."""
    attempts = 3
    while attempts > 0:
        pin = input("   🔑 Enter your PIN: ").strip()
        if pin == user["pin"]:
            return True
        attempts -= 1
        print(f"   ❌ Wrong PIN. {attempts} attempt(s) left.")
    print("   🚫 Too many wrong attempts. Returning to menu.")
    return False


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────
def login():
    clear()
    banner()
    print("\n  ──── LOGIN ────")
    username = input("  Username : ").strip()
    user = find_user(username)
    if not user:
        print("\n  ❌ Username not found.")
        input("  Press Enter to try again...")
        return None

    print()
    if verify_pin(user):
        print(f"\n  ✅ Welcome back, {user['name']}!")
        input("  Press Enter to continue...")
        return user
    return None


# ─────────────────────────────────────────────
#  REGISTER
# ─────────────────────────────────────────────
def register():
    clear()
    banner()
    print("\n  ──── OPEN NEW ACCOUNT ────")
    name     = input("  Full Name : ").strip()
    username = input("  Username  : ").strip()

    if not name or not username:
        print("  ❌ Name and username cannot be empty.")
        input("  Press Enter to go back...")
        return

    if find_user(username):
        print("  ❌ Username already taken.")
        input("  Press Enter to go back...")
        return

    while True:
        pin = input("  Set 4-digit PIN  : ").strip()
        if pin.isdigit() and len(pin) == 4:
            break
        print("  ⚠  PIN must be exactly 4 digits.")

    pin_confirm = input("  Confirm PIN      : ").strip()
    if pin != pin_confirm:
        print("  ❌ PINs do not match.")
        input("  Press Enter to go back...")
        return

    initial = input("  Initial deposit  : Rs. ").strip()
    try:
        initial = float(initial)
        if initial < 0:
            raise ValueError
    except ValueError:
        print("  ❌ Invalid amount.")
        input("  Press Enter to go back...")
        return

    new_user = {"username": username, "pin": pin, "name": name, "balance": initial}
    users.append(new_user)
    log_transaction(username, "Account Opened", initial, initial)

    print(f"\n  🎉 Account created! Welcome, {name}.")
    print(f"  Your username : {username}")
    input("  Press Enter to go to login...")


# ─────────────────────────────────────────────
#  BANKING OPERATIONS
# ─────────────────────────────────────────────
def check_balance(user):
    print("\n  ──── BALANCE ENQUIRY ────")
    print("  🔐 PIN required to view balance.")
    if verify_pin(user):
        print(f"\n  💰 Available Balance : Rs. {user['balance']:,.2f}")
    input("\n  Press Enter to continue...")


def deposit(user):
    print("\n  ──── DEPOSIT ────")
    amount = input("  Enter amount to deposit : Rs. ").strip()
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("  ❌ Invalid amount.")
        input("  Press Enter to continue...")
        return

    print("\n  🔐 Confirm deposit with PIN.")
    if verify_pin(user):
        user["balance"] += amount
        log_transaction(user["username"], "Deposit", amount, user["balance"])
        print(f"\n  ✅ Rs. {amount:,.2f} deposited successfully.")
        print(f"  New Balance : Rs. {user['balance']:,.2f}")
    input("\n  Press Enter to continue...")


def withdraw(user):
    print("\n  ──── WITHDRAWAL ────")
    amount = input("  Enter amount to withdraw : Rs. ").strip()
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("  ❌ Invalid amount.")
        input("  Press Enter to continue...")
        return

    if amount > user["balance"]:
        print("  ❌ Insufficient funds.")
        input("  Press Enter to continue...")
        return

    print("\n  🔐 Confirm withdrawal with PIN.")
    if verify_pin(user):
        user["balance"] -= amount
        log_transaction(user["username"], "Withdrawal", amount, user["balance"])
        print(f"\n  ✅ Rs. {amount:,.2f} withdrawn successfully.")
        print(f"  New Balance : Rs. {user['balance']:,.2f}")
    input("\n  Press Enter to continue...")


def transfer(user):
    print("\n  ──── FUND TRANSFER ────")
    recipient_name = input("  Recipient username : ").strip()
    recipient = find_user(recipient_name)

    if not recipient:
        print("  ❌ Recipient not found.")
        input("  Press Enter to continue...")
        return

    if recipient["username"] == user["username"]:
        print("  ❌ Cannot transfer to yourself.")
        input("  Press Enter to continue...")
        return

    amount = input(f"  Amount to send to {recipient['name']} : Rs. ").strip()
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("  ❌ Invalid amount.")
        input("  Press Enter to continue...")
        return

    if amount > user["balance"]:
        print("  ❌ Insufficient funds.")
        input("  Press Enter to continue...")
        return

    print(f"\n  Transfer Rs. {amount:,.2f} → {recipient['name']}")
    print("  🔐 Confirm with your PIN.")
    if verify_pin(user):
        user["balance"]      -= amount
        recipient["balance"] += amount
        log_transaction(user["username"],      f"Transfer Out → {recipient['username']}", amount, user["balance"])
        log_transaction(recipient["username"], f"Transfer In  ← {user['username']}",      amount, recipient["balance"])
        print(f"\n  ✅ Rs. {amount:,.2f} sent to {recipient['name']}.")
        print(f"  Your Balance : Rs. {user['balance']:,.2f}")
    input("\n  Press Enter to continue...")


def change_pin(user):
    print("\n  ──── CHANGE PIN ────")
    print("  🔐 Verify current PIN first.")
    if not verify_pin(user):
        input("  Press Enter to continue...")
        return

    while True:
        new_pin = input("  New 4-digit PIN : ").strip()
        if new_pin.isdigit() and len(new_pin) == 4:
            break
        print("  ⚠  PIN must be exactly 4 digits.")

    confirm = input("  Confirm new PIN : ").strip()
    if new_pin != confirm:
        print("  ❌ PINs do not match.")
    else:
        user["pin"] = new_pin
        print("  ✅ PIN changed successfully.")
    input("\n  Press Enter to continue...")


def mini_statement(user):
    print("\n  ──── MINI STATEMENT (last 5) ────")
    print("  🔐 PIN required.")
    if not verify_pin(user):
        input("  Press Enter to continue...")
        return

    history = get_user_transactions(user["username"])
    if not history:
        print("  No transactions yet.")
    else:
        recent = history[-5:]
        print()
        print(f"  {'Date':<22} {'Type':<30} {'Amount':>12} {'Balance':>12}")
        print("  " + "─" * 78)
        for t in recent:
            print(f"  {t['date']:<22} {t['type']:<30} Rs.{t['amount']:>9,.2f} Rs.{t['balance_after']:>9,.2f}")
    input("\n  Press Enter to continue...")


def full_statement(user):
    print("\n  ──── FULL STATEMENT ────")
    print("  🔐 PIN required.")
    if not verify_pin(user):
        input("  Press Enter to continue...")
        return

    history = get_user_transactions(user["username"])
    if not history:
        print("  No transactions yet.")
    else:
        print()
        print(f"  {'Date':<22} {'Type':<30} {'Amount':>12} {'Balance':>12}")
        print("  " + "─" * 78)
        for t in history:
            print(f"  {t['date']:<22} {t['type']:<30} Rs.{t['amount']:>9,.2f} Rs.{t['balance_after']:>9,.2f}")
    input("\n  Press Enter to continue...")


# ─────────────────────────────────────────────
#  DASHBOARD (post-login menu)
# ─────────────────────────────────────────────
def dashboard(user):
    while True:
        clear()
        banner()
        print(f"\n  👤  {user['name']}   |   @{user['username']}")
        divider()
        print("  1. Check Balance")
        print("  2. Deposit")
        print("  3. Withdraw")
        print("  4. Transfer Funds")
        print("  5. Mini Statement  (last 5)")
        print("  6. Full Statement")
        print("  7. Change PIN")
        print("  8. Logout")
        divider()
        choice = input("  Select option: ").strip()

        clear()
        banner()

        if   choice == "1": check_balance(user)
        elif choice == "2": deposit(user)
        elif choice == "3": withdraw(user)
        elif choice == "4": transfer(user)
        elif choice == "5": mini_statement(user)
        elif choice == "6": full_statement(user)
        elif choice == "7": change_pin(user)
        elif choice == "8":
            print(f"\n  👋 Goodbye, {user['name']}! Stay safe.")
            input("  Press Enter to exit...")
            break
        else:
            print("  ⚠  Invalid option.")
            input("  Press Enter to continue...")


# ─────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────
def main():
    while True:
        clear()
        banner()
        print("\n  1. Login")
        print("  2. Register / Open Account")
        print("  3. Exit")
        divider()
        choice = input("  Select option: ").strip()

        if choice == "1":
            user = login()
            if user:
                dashboard(user)
        elif choice == "2":
            register()
        elif choice == "3":
            clear()
            print("\n  Thank you for using Python National Bank. Goodbye! 🏦\n")
            break
        else:
            print("  ⚠  Invalid option.")
            input("  Press Enter to try again...")


if __name__ == "__main__":
    main()