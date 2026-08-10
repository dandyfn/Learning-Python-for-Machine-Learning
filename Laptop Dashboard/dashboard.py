import tkinter as tk
import getpass
import socket
import platform
import psutil
import time
import uuid
import winreg
import subprocess

# =====================================
# FUNGSI CEK INTERNET
# =====================================

def cek_internet():
    try:
        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )
        return "ONLINE"
    except:
        return "OFFLINE"

def get_gateway_dns():

    gateway = "Unknown"
    dns = "Unknown"

    try:

        hasil = subprocess.check_output(
            "ipconfig /all",
            shell=True,
            text=True,
            encoding="utf-8"
        )

        lines = hasil.splitlines()

        for i, line in enumerate(lines):

            # Cari gateway yang tidak kosong

            if "Default Gateway" in line:

                bagian = line.split(":")

                if len(bagian) > 1:

                    kandidat = bagian[1].strip()

                    if kandidat != "":
                        gateway = kandidat

            # Cari DNS yang tidak kosong

            if "DNS Servers" in line:

                bagian = line.split(":")

                if len(bagian) > 1:

                    kandidat = bagian[1].strip()

                    if kandidat != "":
                        dns = kandidat

            # Kalau keduanya sudah ketemu, berhenti

            if gateway != "Unknown" and dns != "Unknown":
                break

    except:

        pass

    return gateway, dns

# =====================================
# HITUNG UPTIME
# =====================================

def hitung_uptime():

    boot_time = psutil.boot_time()

    sekarang = time.time()

    selisih = int(sekarang - boot_time)

    jam = selisih // 3600

    menit = (selisih % 3600) // 60

    return f"{jam} Jam {menit} Menit"


# =====================================
# WARNA STATUS
# =====================================

def warna_cpu(cpu):

    if cpu < 50:
        return "lime"

    elif cpu < 80:
        return "yellow"

    else:
        return "red"


def warna_ram(ram):

    if ram < 50:
        return "lime"

    elif ram < 80:
        return "yellow"

    else:
        return "red"


# =====================================
# REFRESH DATA
# =====================================

def refresh_data():

    user = getpass.getuser()

    hostname = socket.gethostname()

    key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    )

    windows_version = winreg.QueryValueEx(
        key,
        "ProductName"
    )[0]

    python_version = platform.python_version()

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory()

    cpu_name = platform.processor()

    cpu_core = psutil.cpu_count()

    ram_used = round(
        ram.used / (1024**3),
        2
    )

    ram_free = round(
        ram.available / (1024**3),
        2
    )

    ram_total = round(
        ram.total / (1024**3),
        2
    )

    disk = psutil.disk_usage("C:\\")

    try:

        disk_d = psutil.disk_usage("D:\\")

        disk_d_total = round(
            disk_d.total / (1024**3),
            2
        )

        disk_d_used = round(
            disk_d.used / (1024**3),
            2
        )

        disk_d_free = round(
            disk_d.free / (1024**3),
            2
        )

        disk_d_percent = disk_d.percent

    except:

        disk_d_total = "N/A"
        disk_d_used = "N/A"
        disk_d_free = "N/A"
        disk_d_percent = "N/A"

    disk_total = round(
        disk.total / (1024**3),
        2
    )

    disk_used = round(
        disk.used / (1024**3),
        2
    )

    disk_free = round(
        disk.free / (1024**3),
        2
    )

    disk_d_total_value.config(
        text=f"{disk_d_total} GB"
        if disk_d_total != "N/A"
        else "N/A"
    )

    disk_d_used_value.config(
        text=f"{disk_d_used} GB"
        if disk_d_used != "N/A"
        else "N/A"
    )

    disk_d_free_value.config(
        text=f"{disk_d_free} GB"
        if disk_d_free != "N/A"
        else "N/A"
    )


    ip_address = socket.gethostbyname(
        hostname
    )

    gateway, dns = get_gateway_dns()

    gateway_value.config(
    text=gateway
    )

    dns_value.config(
        text=dns
    )

    mac_address = ':'.join([
        '{:02X}'.format(
            (uuid.getnode() >> ele) & 0xff
        )
        for ele in range(40, -1, -8)
    ])

    internet = cek_internet()

    battery = psutil.sensors_battery()

    if battery:
        battery_percent = f"{battery.percent}%"

        charging = (
            "Yes"
            if battery.power_plugged
            else "No"
        )

    else:
        battery_percent = "N/A"
        charging = "N/A"

    uptime = hitung_uptime()

    cpu_name_value.config(
        text=cpu_name
    )

    cpu_core_value.config(
        text=cpu_core
    )

    ram_used_value.config(
        text=f"{ram_used} GB"
    )

    ram_free_value.config(
        text=f"{ram_free} GB"
    )

    disk_total_value.config(
        text=f"{disk_total} GB"
    )

    disk_used_value.config(
        text=f"{disk_used} GB"
    )

    mac_value.config(
        text=mac_address
    )

    battery_value.config(
        text=battery_percent
    )

    charging_value.config(
        text=charging
    )



    # =========================
    # UPDATE LABEL
    # =========================

    user_value.config(text=user)

    host_value.config(text=hostname)

    windows_value.config(text=windows_version)

    python_value.config(text=python_version)

    cpu_value.config(
        text=f"{cpu} %",
        fg=warna_cpu(cpu)
    )

    ram_value.config(
        text=f"{ram.percent} %",
        fg=warna_ram(ram.percent)
    )

    ram_total_value.config(
        text=f"{ram_total} GB"
    )

    disk_value.config(
        text=f"{disk_free} GB"
    )

    ip_value.config(
        text=ip_address
    )

    gateway_value.config(
    text=gateway
)

    dns_value.config(
        text=dns
    )

    if internet == "ONLINE":

        internet_value.config(
            text=internet,
            fg="lime"
        )

    else:

        internet_value.config(
            text=internet,
            fg="red"
        )

    uptime_value.config(
        text=uptime
    )

    # AUTO REFRESH 5 DETIK

    window.after(
        5000,
        refresh_data
    )


# =====================================
# CARD
# =====================================

def buat_card(parent, judul):

    frame = tk.LabelFrame(
        parent,
        text=judul,
        bg="#1e293b",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=10,
        pady=10
    )

    return frame


# =====================================
# WINDOW
# =====================================

window = tk.Tk()

window.title(
    "Dandy's Device Information Dashboard"
)

window.geometry("1400x850")
window.state("zoomed")

window.configure(
    bg="#0f172a"
)


# =====================================
# JUDUL
# =====================================

judul = tk.Label(

    window,

    text="Dandy's Device Information Dashboard",

    font=("Segoe UI", 22, "bold"),

    bg="#0f172a",

    fg="#38bdf8"
)

judul.pack(
    pady=20
)

# =====================================
# MAIN LAYOUT
# =====================================

main_frame = tk.Frame(
    window,
    bg="#0f172a"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

# Baris atas
top_frame = tk.Frame(
    main_frame,
    bg="#0f172a"
)

top_frame.pack(
    fill="both",
    expand=True
)

# Kolom kiri
left_frame = tk.Frame(
    top_frame,
    bg="#0f172a"
)

left_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)

# Kolom kanan
right_frame = tk.Frame(
    top_frame,
    bg="#0f172a"
)

right_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10
)

# Baris bawah
bottom_frame = tk.Frame(
    main_frame,
    bg="#0f172a"
)

bottom_frame.pack(
    fill="x",
    pady=10
)


# =====================================
# SYSTEM CARD
# =====================================

system_card = buat_card(
    window,
    "👤 SYSTEM"
)

system_card.pack(
    in_=left_frame,
    fill="x",
    pady=5
)

tk.Label(system_card,
         text="User",
         bg="#1e293b",
         fg="white").grid(row=0, column=0, sticky="w")

user_value = tk.Label(system_card,
                      bg="#1e293b",
                      fg="white")

user_value.grid(row=0, column=1, sticky="w")


tk.Label(system_card,
         text="Hostname",
         bg="#1e293b",
         fg="white").grid(row=1, column=0, sticky="w")

host_value = tk.Label(system_card,
                      bg="#1e293b",
                      fg="white")

host_value.grid(row=1, column=1, sticky="w")


tk.Label(system_card,
         text="Windows",
         bg="#1e293b",
         fg="white").grid(row=2, column=0, sticky="w")

windows_value = tk.Label(system_card,
                         bg="#1e293b",
                         fg="white")

windows_value.grid(row=2, column=1, sticky="w")


tk.Label(system_card,
         text="Python",
         bg="#1e293b",
         fg="white").grid(row=3, column=0, sticky="w")

python_value = tk.Label(system_card,
                        bg="#1e293b",
                        fg="white")

python_value.grid(row=3, column=1, sticky="w")


# =====================================
# HARDWARE CARD
# =====================================

hardware_card = buat_card(
    window,
    "🖥 HARDWARE"
)

hardware_card.pack(
    in_=left_frame,
    fill="x",
    pady=5
)

tk.Label(hardware_card,
         text="CPU Usage",
         bg="#1e293b",
         fg="white").grid(row=0, column=0, sticky="w")

cpu_value = tk.Label(
    hardware_card,
    bg="#1e293b"
)

cpu_value.grid(row=0, column=1, sticky="w")


tk.Label(hardware_card,
         text="RAM Usage",
         bg="#1e293b",
         fg="white").grid(row=1, column=0, sticky="w")

ram_value = tk.Label(
    hardware_card,
    bg="#1e293b"
)

ram_value.grid(row=1, column=1, sticky="w")


tk.Label(hardware_card,
         text="RAM Total",
         bg="#1e293b",
         fg="white").grid(row=2, column=0, sticky="w")

ram_total_value = tk.Label(
    hardware_card,
    bg="#1e293b",
    fg="white"
)

ram_total_value.grid(row=2, column=1, sticky="w")

tk.Label(
    hardware_card,
    text="CPU Name",
    bg="#1e293b",
    fg="white"
).grid(row=3,column=0,sticky="w")

cpu_name_value = tk.Label(
    hardware_card,
    bg="#1e293b",
    fg="white"
)

cpu_name_value.grid(row=3,column=1,sticky="w")

tk.Label(
    hardware_card,
    text="CPU Core",
    bg="#1e293b",
    fg="white"
).grid(row=4,column=0,sticky="w")

cpu_core_value = tk.Label(
    hardware_card,
    bg="#1e293b",
    fg="white"
)

cpu_core_value.grid(row=4,column=1,sticky="w")

tk.Label(
    hardware_card,
    text="RAM Used",
    bg="#1e293b",
    fg="white"
).grid(row=5,column=0,sticky="w")

ram_used_value = tk.Label(
    hardware_card,
    bg="#1e293b",
    fg="white"
)

ram_used_value.grid(row=5,column=1,sticky="w")

tk.Label(
    hardware_card,
    text="RAM Free",
    bg="#1e293b",
    fg="white"
).grid(row=6,column=0,sticky="w")

ram_free_value = tk.Label(
    hardware_card,
    bg="#1e293b",
    fg="white"
)

ram_free_value.grid(row=6,column=1,sticky="w")


# =====================================
# STORAGE CARD
# =====================================

storage_card = buat_card(
    window,
    "💾 STORAGE"
)

storage_card.pack(
    in_=right_frame,
    fill="x",
    pady=5
)

# Membuat kolom sejajar
storage_card.grid_columnconfigure(
    0,
    minsize=120
)

storage_card.grid_columnconfigure(
    1,
    minsize=150
)

# ==========================
# DISK C
# ==========================

tk.Label(
    storage_card,
    text="Disk C Free",
    bg="#1e293b",
    fg="white"
).grid(row=0, column=0, sticky="w")

disk_value = tk.Label(
    storage_card,
    bg="#1e293b",
    fg="white"
)

disk_value.grid(
    row=0,
    column=1,
    sticky="w"
)


tk.Label(
    storage_card,
    text="Disk C Total",
    bg="#1e293b",
    fg="white"
).grid(row=1, column=0, sticky="w")

disk_total_value = tk.Label(
    storage_card,
    bg="#1e293b",
    fg="white"
)

disk_total_value.grid(
    row=1,
    column=1,
    sticky="w"
)


tk.Label(
    storage_card,
    text="Disk C Used",
    bg="#1e293b",
    fg="white"
).grid(row=2, column=0, sticky="w")

disk_used_value = tk.Label(
    storage_card,
    bg="#1e293b",
    fg="white"
)

disk_used_value.grid(
    row=2,
    column=1,
    sticky="w"
)

# ==========================
# DISK D
# ==========================

tk.Label(
    storage_card,
    text="Disk D Free",
    bg="#1e293b",
    fg="white"
).grid(row=3, column=0, sticky="w")

disk_d_free_value = tk.Label(
    storage_card,
    bg="#1e293b",
    fg="white"
)

disk_d_free_value.grid(
    row=3,
    column=1,
    sticky="w"
)


tk.Label(
    storage_card,
    text="Disk D Total",
    bg="#1e293b",
    fg="white"
).grid(row=4, column=0, sticky="w")

disk_d_total_value = tk.Label(
    storage_card,
    bg="#1e293b",
    fg="white"
)

disk_d_total_value.grid(
    row=4,
    column=1,
    sticky="w"
)


tk.Label(
    storage_card,
    text="Disk D Used",
    bg="#1e293b",
    fg="white"
).grid(row=5, column=0, sticky="w")

disk_d_used_value = tk.Label(
    storage_card,
    bg="#1e293b",
    fg="white"
)

disk_d_used_value.grid(
    row=5,
    column=1,
    sticky="w"
)

# =====================================
# NETWORK CARD
# =====================================

network_card = buat_card(
    window,
    "🌐 NETWORK"
)

network_card.pack(
    in_=right_frame,
    fill="x",
    pady=5
)

# IP Address

tk.Label(
    network_card,
    text="IP Address",
    width=15,
    anchor="w",
    bg="#1e293b",
    fg="white"
).grid(row=0,column=0,sticky="w")

ip_value = tk.Label(
    network_card,
    bg="#1e293b",
    fg="white"
)

ip_value.grid(row=0,column=1,sticky="w")


# Gateway

tk.Label(
    network_card,
    text="Gateway",
    width=15,
    anchor="w",
    bg="#1e293b",
    fg="white"
).grid(row=1,column=0,sticky="w")

gateway_value = tk.Label(
    network_card,
    bg="#1e293b",
    fg="white"
)

gateway_value.grid(row=1,column=1,sticky="w")


# DNS

tk.Label(
    network_card,
    text="DNS",
    width=15,
    anchor="w",
    bg="#1e293b",
    fg="white"
).grid(row=2,column=0,sticky="w")

dns_value = tk.Label(
    network_card,
    bg="#1e293b",
    fg="white"
)

dns_value.grid(row=2,column=1,sticky="w")


# Internet

tk.Label(
    network_card,
    text="Internet",
    width=15,
    anchor="w",
    bg="#1e293b",
    fg="white"
).grid(row=3,column=0,sticky="w")

internet_value = tk.Label(
    network_card,
    bg="#1e293b"
)

internet_value.grid(row=3,column=1,sticky="w")


# MAC Address

tk.Label(
    network_card,
    text="MAC Address",
    width=15,
    anchor="w",
    bg="#1e293b",
    fg="white"
).grid(row=4,column=0,sticky="w")

mac_value = tk.Label(
    network_card,
    bg="#1e293b",
    fg="white"
)

mac_value.grid(row=4,column=1,sticky="w")

# =====================================
# SYSTEM STATUS CARD
# =====================================

status_card = buat_card(
    window,
    "⚙ SYSTEM STATUS"
)

status_card.pack(
    in_=bottom_frame,
    side="left",
    fill="both",
    expand=True,
    padx=5
)

tk.Label(
    status_card,
    text="Uptime",
    bg="#1e293b",
    fg="white"
).grid(row=0,column=0)

uptime_value = tk.Label(
    status_card,
    bg="#1e293b",
    fg="white"
)

uptime_value.grid(row=0,column=1)

# =====================================
# BATTERY CARD
# =====================================


battery_card = buat_card(
    window,
    "🔋 BATTERY"
)

battery_card.pack(
    in_=bottom_frame,
    side="right",
    fill="both",
    expand=True,
    padx=5
)

tk.Label(
    battery_card,
    text="Battery",
    bg="#1e293b",
    fg="white"
).grid(row=0,column=0)

battery_value = tk.Label(
    battery_card,
    bg="#1e293b",
    fg="white"
)

battery_value.grid(row=0,column=1)

tk.Label(
    battery_card,
    text="Charging",
    bg="#1e293b",
    fg="white"
).grid(row=1,column=0)

charging_value = tk.Label(
    battery_card,
    bg="#1e293b",
    fg="white"
)

charging_value.grid(row=1,column=1)




# =====================================
# BUTTON
# =====================================

button_frame = tk.Frame(
    window,
    bg="#0f172a"
)

button_frame.pack(
    side="bottom",
    pady=15
)

tk.Button(
    button_frame,
    text="Refresh",
    command=refresh_data,
    width=15,
    bg="#2563eb",
    fg="white"
).pack(
    side="left",
    padx=10
)

tk.Button(
    button_frame,
    text="Exit",
    command=window.destroy,
    width=15,
    bg="#dc2626",
    fg="white"
).pack(
    side="left",
    padx=10
)

# =====================================
# START
# =====================================

refresh_data()

window.mainloop()