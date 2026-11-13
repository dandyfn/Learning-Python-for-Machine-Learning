import socket
import json  # Menggunakan JSON untuk format pesan
import time  # Untuk mensimulasikan pesan yang terpecah (E2.3)

class ProcessB:
    def __init__(self):
        self.logical_clock = 0
        self.balance = 1000  # Saldo awal
        self.reader = None  # [E2.3] pembaca baris dari socket, dibuat sekali saja

    def increment_clock(self):
        self.logical_clock += 1

    def send_message(self, message, conn):
        self.increment_clock()
        message_dict = {
            "message": message,
            "balance": self.balance,
            "timestamp": self.logical_clock
        }
        message_with_timestamp = json.dumps(message_dict)  # Convert ke JSON
        # [E2.3] Framing: setiap pesan diakhiri '\n' sebagai penanda batas pesan
        data = (message_with_timestamp + "\n").encode()
        # [E2.3] Uji: kirim pesan dalam 2 potongan dengan jeda 1 detik
        conn.sendall(data[:15])
        print("[uji] 15 byte pertama terkirim, jeda 1 detik...")
        time.sleep(1)
        conn.sendall(data[15:])
        print(f"Sent: {message_with_timestamp}")

    def receive_message(self, conn):
        # [E2.3] Baca sampai ketemu '\n', berapa pun potongan TCP yang datang
        if self.reader is None:
            self.reader = conn.makefile("r", encoding="utf-8")
        data = self.reader.readline()
        if not data:
            print("Koneksi ditutup sebelum pesan utuh diterima.")
            return
        print(f"Raw received data: {data.strip()}")  # Debugging line
        try:
            message_dict = json.loads(data)  # Parse JSON
            message = message_dict["message"]
            balance = message_dict["balance"]
            timestamp = message_dict["timestamp"]
            self.logical_clock = max(self.logical_clock, timestamp) + 1
            self.balance = balance  # Update saldo dengan yang terbaru dari Proses A
            print(f"Received: {message} | Updated balance: {self.balance} | Updated clock: {self.logical_clock}")
        except ValueError:
            print("Error: Received data in unexpected format.")
            return

    def subtract_balance(self, amount):
        self.balance -= amount
        print(f"New balance after subtracting {amount}: {self.balance}")


def main():
    process_b = ProcessB()

    # Membuat socket client dan menghubungkan ke Proses A
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to Process A")

    # Terima pesan dari Proses A
    process_b.receive_message(client_socket)

    # Kurangi saldo dan kirim pesan ke Proses A
    process_b.subtract_balance(50)
    process_b.send_message(f"Subtract $50", client_socket)

    client_socket.close()

if __name__ == "__main__":
    main()
