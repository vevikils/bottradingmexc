import tkinter as tk
from tkinter import ttk, messagebox
from ccxt import mexc
from dotenv import load_dotenv
import os

# Cargar variables de entorno (API Key y API Secret)
load_dotenv()

# Variables de la API (fuera de la interfaz gráfica)
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

# Clase principal de la aplicación
class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot de Trading - MEXC")
        self.root.geometry("600x400")

        # Título
        tk.Label(root, text="Bot de Trading para MEXC", font=("Arial", 16)).pack(pady=10)

        # Par de Trading
        tk.Label(root, text="Par de Trading:").pack(anchor="w", padx=20, pady=5)
        self.pair = ttk.Combobox(root, values=["BTC/USDT", "ETH/USDT", "BNB/USDT"], state="readonly", width=20)
        self.pair.pack(padx=20)
        self.pair.set("BTC/USDT")  # Valor por defecto

        # Estrategias de trading
        tk.Label(root, text="Estrategia:").pack(anchor="w", padx=20, pady=5)
        self.strategy = ttk.Combobox(root, values=["SMA", "EMA", "RSI"], state="readonly", width=20)
        self.strategy.pack(padx=20)
        self.strategy.set("SMA")  # Valor por defecto

        # Monto de la operación
        tk.Label(root, text="Monto a Tradear:").pack(anchor="w", padx=20, pady=5)
        self.amount = tk.DoubleVar()
        tk.Entry(root, textvariable=self.amount, width=50).pack(padx=20, pady=5)

        # Botones de control
        tk.Button(root, text="Iniciar Bot", command=self.start_bot, bg="green", fg="white").pack(pady=10)
        tk.Button(root, text="Detener Bot", command=self.stop_bot, bg="red", fg="white").pack(pady=10)

        # Botones de compra y venta
        tk.Button(root, text="Comprar", command=self.buy_btc, bg="blue", fg="white").pack(pady=5)
        tk.Button(root, text="Vender", command=self.sell_btc, bg="blue", fg="white").pack(pady=5)

        # Área de logs
        tk.Label(root, text="Logs:").pack(anchor="w", padx=20, pady=5)
        self.log_area = tk.Text(root, height=10, width=70)
        self.log_area.pack(padx=20, pady=10)

        # Variables de control
        self.bot_running = False

    def start_bot(self):
        if not api_key or not api_secret:
            messagebox.showerror("Error", "Por favor ingresa las claves de API.")
            return
        
        # Conectar a la API de MEXC
        try:
            self.exchange = mexc({
                'apiKey': api_key,
                'secret': api_secret,
            })
            balance = self.exchange.fetch_balance()
            self.log_area.insert("end", "Bot iniciado correctamente.\n")
            self.log_area.insert("end", f"Balance inicial: {balance['total']}\n")
            self.bot_running = True
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar: {e}")

    def stop_bot(self):
        if self.bot_running:
            self.log_area.insert("end", "Bot detenido.\n")
            self.bot_running = False
        else:
            messagebox.showinfo("Info", "El bot no está en ejecución.")

    def buy_btc(self):
        if not self.bot_running:
            messagebox.showerror("Error", "El bot no está en ejecución.")
            return

        amount = self.amount.get()
        if amount <= 0:
            messagebox.showerror("Error", "El monto debe ser mayor a 0.")
            return

        pair = self.pair.get()
        try:
            # Realizar una orden de compra de mercado
            order = self.exchange.create_market_buy_order(pair, amount)
            self.log_area.insert("end", f"Orden de compra ejecutada: {order}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando la compra: {e}")

    def sell_btc(self):
        if not self.bot_running:
            messagebox.showerror("Error", "El bot no está en ejecución.")
            return

        amount = self.amount.get()
        if amount <= 0:
            messagebox.showerror("Error", "El monto debe ser mayor a 0.")
            return

        pair = self.pair.get()
        try:
            # Realizar una orden de venta de mercado
            order = self.exchange.create_market_sell_order(pair, amount)
            self.log_area.insert("end", f"Orden de venta ejecutada: {order}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando la venta: {e}")

# Crear ventana principal
root = tk.Tk()
app = TradingBotApp(root)
root.mainloop()
