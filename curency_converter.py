import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from tkinter import font as tkfont

class CurrencyConverter:
    def __init__(self):
        # Initialize API settings
        self.API_KEY = "YOUR_API_KEY_HERE"  # Replace with your API key
        self.BASE_URL = "https://api.exchangerate-api.com/v4/latest/USD"
        
        # Store exchange rates
        self.rates = {}
        # Load exchange rates
        self.load_rates()
        
        # Dictionary of common currencies with symbols
        self.currencies = {
            'USD': '🇺🇸 US Dollar',
            'EUR': '🇪🇺 Euro',
            'GBP': '🇬🇧 British Pound',
            'JPY': '🇯🇵 Japanese Yen',
            'AUD': '🇦🇺 Australian Dollar',
            'CAD': '🇨🇦 Canadian Dollar',
            'CHF': '🇨🇭 Swiss Franc',
            'CNY': '🇨🇳 Chinese Yuan',
            'INR': '🇮🇳 Indian Rupee',
            'NZD': '🇳🇿 New Zealand Dollar',
            'SGD': '🇸🇬 Singapore Dollar',
            'AED': '🇦🇪 UAE Dirham',
            'SAR': '🇸🇦 Saudi Riyal',
            'QAR': '🇶🇦 Qatari Riyal'
        }

    def load_rates(self):
        """Load exchange rates from API"""
        try:
            response = requests.get(self.BASE_URL)
            self.rates = response.json()['rates']
            return True
        except:
            return False

    def convert(self, amount, from_currency, to_currency):
        """Convert currency using loaded rates"""
        if not self.rates:
            if not self.load_rates():
                return None
        
        # Convert to USD first (base currency)
        if from_currency != 'USD':
            amount = amount / self.rates[from_currency]
        
        # Convert from USD to target currency
        if to_currency != 'USD':
            amount = amount * self.rates[to_currency]
            
        return amount

class CurrencyConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x700")
        self.root.configure(bg="#FFE4E1")  # Misty Rose background
        
        # Initialize converter
        self.converter = CurrencyConverter()
        
        # Create and apply styles
        self.create_styles()
        
        # Setup UI
        self.setup_ui()

    def create_styles(self):
        style = ttk.Style()
        
        # Configure frame style
        style.configure(
            "Custom.TFrame",
            background="#FFE4E1"
        )
        
        # Configure label styles
        style.configure(
            "Custom.TLabel",
            background="#FFE4E1",
            font=("Helvetica", 12)
        )
        
        # Configure title style
        style.configure(
            "Title.TLabel",
            background="#FFE4E1",
            font=("Helvetica", 24, "bold"),
            foreground="#FF1493"
        )
        
        # Configure button style
        style.configure(
            "Custom.TButton",
            font=("Helvetica", 14, "bold"),
            padding=10
        )
        
        # Configure result style
        style.configure(
            "Result.TLabel",
            background="#FFE4E1",
            font=("Helvetica", 14, "bold"),
            foreground="#FF69B4"
        )

    def setup_ui(self):
        # Main Frame with padding
        main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title with decorative elements
        title_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        title_frame.pack(pady=20, fill="x")
        
        title_label = ttk.Label(
            title_frame,
            text="💱 Currency Converter 💱",
            style="Title.TLabel"
        )
        title_label.pack()

        # Amount Frame
        amount_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        amount_frame.pack(pady=20, fill="x")
        
        amount_label = ttk.Label(
            amount_frame,
            text="Enter Amount:",
            style="Custom.TLabel"
        )
        amount_label.pack()
        
        # Custom styled entry
        self.amount_entry = tk.Entry(
            amount_frame,
            font=("Helvetica", 14),
            width=20,
            justify="center",
            bg="white",
            relief="solid"
        )
        self.amount_entry.pack(pady=5)
        self.amount_entry.insert(0, "1")

        # Currency Selection Frame
        currency_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        currency_frame.pack(pady=20, fill="x")
        
        # From Currency
        from_label = ttk.Label(
            currency_frame,
            text="From Currency:",
            style="Custom.TLabel"
        )
        from_label.pack()
        
        # Custom styled combobox
        self.from_currency = ttk.Combobox(
            currency_frame,
            values=list(self.converter.currencies.keys()),
            font=("Helvetica", 12),
            width=25,
            justify="center"
        )
        self.from_currency.pack(pady=5)
        self.from_currency.set("USD")

        # To Currency
        to_label = ttk.Label(
            currency_frame,
            text="To Currency:",
            style="Custom.TLabel"
        )
        to_label.pack()
        
        self.to_currency = ttk.Combobox(
            currency_frame,
            values=list(self.converter.currencies.keys()),
            font=("Helvetica", 12),
            width=25,
            justify="center"
        )
        self.to_currency.pack(pady=5)
        self.to_currency.set("EUR")

        # Convert Button with hover effect
        self.convert_button = tk.Button(
            main_frame,
            text="Convert",
            font=("Helvetica", 14, "bold"),
            bg="#FF69B4",
            fg="white",
            relief="raised",
            command=self.convert,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.convert_button.pack(pady=20)
        
        # Bind hover events
        self.convert_button.bind('<Enter>', self.on_enter)
        self.convert_button.bind('<Leave>', self.on_leave)

        # Result Frame
        result_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        result_frame.pack(pady=20, fill="x")
        
        self.result_label = ttk.Label(
            result_frame,
            text="",
            style="Result.TLabel",
            wraplength=400,
            justify="center"
        )
        self.result_label.pack()

    def on_enter(self, event):
        """Button hover effect - darker pink"""
        self.convert_button.configure(bg="#FF1493")

    def on_leave(self, event):
        """Button hover effect - return to original color"""
        self.convert_button.configure(bg="#FF69B4")

    def convert(self):
        try:
            # Get and validate amount
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Please enter a positive number")
            
            # Get selected currencies
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            
            # Perform conversion
            result = self.converter.convert(amount, from_curr, to_curr)
            
            if result is not None:
                # Calculate rate for display
                rate = self.converter.convert(1, from_curr, to_curr)
                
                # Format result text
                result_text = f"{amount:,.2f} {from_curr} = \n{result:,.2f} {to_curr}\n"
                result_text += f"\nExchange Rate:\n1 {from_curr} = {rate:,.4f} {to_curr}"
                
                # Update result label
                self.result_label.config(text=result_text)
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to fetch exchange rates. Please check your internet connection."
                )
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = CurrencyConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()