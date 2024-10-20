# Main source file to perform ML on Nvidia Stock Price Dataset
# https://www.kaggle.com/datasets/syedfaizanalii/nividia-stock-dataset-2023-2024

# Test Change
# Objective: 
# Given: a day's open, high, low, close, Adj close, and volume, 
# Determine: next day's close using machine learning


#### Get updates
# git pull

##### Push to GIT
# git add .
# git commit -m "MESSAGE"
# git push origin main




########################### SETUP #####################################
# Import Libs   
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
from matplotlib.ticker import MaxNLocator
from yfin_handle import yf_Dataframe, yf_Dataframe2
import tkinter as tk
from tkinter import ttk
from tkinter.constants import LEFT, TOP
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


########################### CONFIG #####################################
ticker = 'NVDA'
days_of_data = 365




class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        

        self.title("Stock App")
        self.geometry("800x600")
        self.icon = tk.PhotoImage(file="money_icon.ico")
        self.iconphoto(False, self.icon)

        
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)  # Set the menubar to the root window
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.exit_program)
        
        self.frame1 = tk.LabelFrame(self, text = 'Config')
        self.frame1.place(relx=0.05, rely=0.01, relwidth=.9, relheight=.1)
        
        self.frame2 = tk.LabelFrame(self, text = 'Analysis')
        self.frame2.place(relx=0.05, rely=0.15, relwidth=.8, relheight=.8)
        
        self.frame3 = tk.LabelFrame(self, text = 'Constants')
        self.frame3.place(relx=0.85, rely=0.15, relwidth=.1, relheight=.8)
        
        
        
        self.notebook = ttk.Notebook(self.frame2)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Opens")
        self.notebook.add(self.tab2, text="Closes")
        self.notebook.pack(expand=True, fill="both")
        
        
        
        self.stock_ticker_label = tk.Label(self.frame1, text = "Ticker")
        self.stock_ticker_label.pack(side = LEFT)
        self.stock_ticker_entry = tk.Entry(self.frame1)
        self.stock_ticker_entry.pack(side = LEFT)
        self.stock_enter_button = tk.Button(self.frame1, text="Generate Plots", command=self.create_analysis_plots)
        self.stock_enter_button.pack(side = LEFT)
        
        self.start_date_label = tk.Label(self.frame1, 
                                         text = "         Start Date")
        self.start_date_label.pack(side = LEFT)
        self.cal_start=DateEntry(self.frame1,selectmode='day',
                                 year=(datetime.now() - timedelta(days=365)).year, 
                                 month=(datetime.now() - timedelta(days=365)).month, 
                                 day=(datetime.now() - timedelta(days=365)).day)
        self.cal_start.pack(side = LEFT)
        
        self.end_date_label = tk.Label(self.frame1, text = "           End Date")
        self.end_date_label.pack(side = LEFT)
        self.cal_end=DateEntry(self.frame1,selectmode='day')
        self.cal_end.pack(side = LEFT)
        
        
        
        ########### Frame 3 Stats ############
        # 52 Week High
        self.y_high_label = tk.Label(self.frame3, text = "52 Week High")
        self.y_high_label.pack(side = TOP)
        self.y_high_entry = ttk.Entry(self.frame3, justify="center")
        self.y_high_entry.insert(0, "-")
        self.y_high_entry.pack(side = TOP)
        self.y_high_entry.config(state = "readonly")
        # 52 Week Low
        self.y_low_label = tk.Label(self.frame3, text = "52 Week low")
        self.y_low_label.pack(side = TOP)
        self.y_low_entry = ttk.Entry(self.frame3, justify="center")
        self.y_low_entry.insert(0, "-")
        self.y_low_entry.pack(side = TOP)
        self.y_low_entry.config(state = "readonly")
        # Market Cap
        self.y_mc_label = tk.Label(self.frame3, text = "Market Cap")
        self.y_mc_label.pack(side = TOP)
        self.y_mc_entry = ttk.Entry(self.frame3, justify="center")
        self.y_mc_entry.insert(0, "-")
        self.y_mc_entry.pack(side = TOP)
        self.y_mc_entry.config(state = "readonly")
        # Dividend 
        self.y_div_label = tk.Label(self.frame3, text = "Dividend")
        self.y_div_label.pack(side = TOP)
        self.y_div_entry = ttk.Entry(self.frame3, justify="center")
        self.y_div_entry.insert(0, "-")
        self.y_div_entry.pack(side = TOP)
        self.y_div_entry.config(state = "readonly")
        
        
        
        
        # self.create_analysis_plots()
        
        
    def create_analysis_plots(self):
        plt.clf()
        ticker = self.stock_ticker_entry.get()
        start_date = self.cal_start.get()
        end_date = self.cal_end.get()
        
        
        stock = yf.Ticker(ticker)
        info = stock.info
        self.normal_state()
        self.clear_all_entry()
        market_cap = info.get('marketCap')
        if market_cap >= 1000000000:
            market_cap = str(round(int(market_cap) / 1000000000,1)) + "B"
        else:
            market_cap = str(round(int(market_cap) / 1000000,1)) + "M"
        dividend_yield = info.get('dividendYield')
        fifty_two_week_high = info.get('fiftyTwoWeekHigh')
        fifty_two_week_low = info.get('fiftyTwoWeekLow')
        print(fifty_two_week_high)
        
        self.y_high_entry.insert(0, str(fifty_two_week_high))
        self.y_low_entry.insert(0, fifty_two_week_low)
        self.y_mc_entry.insert(0, market_cap)
        self.y_div_entry.insert(0, dividend_yield)
        
        self.read_only()
        
        
        
        
        print(ticker)
        print(start_date)
        stock_df=[]
        stock_df = yf_Dataframe2(ticker, start_date, end_date)
        stock_df.reset_index(inplace=True)
        dates      = stock_df['Date']
        opens      = stock_df['Open']
        highs      = stock_df['High']
        lows       = stock_df['Low']
        closes     = stock_df['Close']
        adj_closes = stock_df['Adj Close']
        volume     = stock_df['Volume']
        
        # Clear any previous plots
        

        # Plot using plt.plot()
        plt.plot(dates, opens, label = 'Opens')
        plt.title(f"{ticker} Stock Opening Prices")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")

        mean_line_1 = np.mean(opens)
        plt.axhline(mean_line_1, color = 'b', linestyle = '--', label = f'Mean: {mean_line_1:.2f}')
        plt.legend()
        # Embed the plot in tkinter
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.tab1)  # plt.gcf() gets the current figure
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        
        # Plot for tab2
        plt.figure()  # Create another figure for tab2
        plt.plot(dates, closes, label='Closes', color='red')
        plt.title(f"{ticker} Stock Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        
        # Embed plot in tab2
        if hasattr(self, 'canvas2'):
            self.canvas2.get_tk_widget().destroy()
        self.canvas2 = FigureCanvasTkAgg(plt.gcf(), master=self.tab2)  # Embed in tab2
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        
        
    def clear_all_entry(self):
        self.y_high_entry.delete(0,tk.END)
        self.y_low_entry.delete(0,tk.END)
        self.y_mc_entry.delete(0,tk.END)
        self.y_div_entry.delete(0,tk.END)
        
    def read_only(self):
        self.y_high_entry.config(state = "readonly")
        self.y_low_entry.config(state = "readonly")
        self.y_mc_entry.config(state = "readonly")
        self.y_div_entry.config(state = "readonly")
        
    def normal_state(self):
        self.y_high_entry.config(state = "normal")
        self.y_low_entry.config(state = "normal")
        self.y_mc_entry.config(state = "normal")
        self.y_div_entry.config(state = "normal")
        
        
        
        

        
        
        

    def exit_program(self):
        self.destroy()


    # # Function to open the date picker dialog
    # def open_date_picker(self):
    #     # Create a new top-level window for date selection
    #     self.top = tk.Toplevel(self)
    #     self.top.title("Pick a Date")

    #     # Create DateEntry widget to select a date
    #     self.cal = DateEntry(self.top, width=12, background='darkblue', foreground='white', borderwidth=2)
    #     self.cal.pack(pady=20)

    #     # Button to confirm the date selection
    #     confirm_button = ttk.Button(self.top, text="Confirm Date", command=self.confirm_date)
    #     confirm_button.pack(pady=10)

    # # Function to confirm the selected date and update the label
    # def confirm_date(self):
    #     selected_date = self.cal.get_date()
    #     self.date_label.config(text=f"Selected Date: {selected_date}")
    #     self.top.destroy()  # Close the top-level window after confirming the date


# Main block to run the Tkinter loop
if __name__ == "__main__":
    app = StockApp()
    app.mainloop()

















########################### ANALYSIS #####################################
stock_df = yf_Dataframe(ticker, days_of_data)
stock_df.reset_index(inplace=True)


# # Break out Columns
dates      = stock_df['Date']
opens      = stock_df['Open']
highs      = stock_df['High']
lows       = stock_df['Low']
closes     = stock_df['Close']
adj_closes = stock_df['Adj Close']
volume     = stock_df['Volume']










# Plot the open and close on a line graph
plt.plot(dates, opens, label = 'Opens')
plt.plot(dates, closes, label = 'Closes')
plt.xlabel('dates')
plt.ylabel('open price ($)')
plt.title(f'{ticker} opening price')
plt.grid(True)
plt.legend()
plt.show()

# Plot the daily volume on a scatter
colors = volume/1000000
plt.scatter(dates, volume/1000000, c=colors, cmap='viridis')
plt.xlabel('dates')
plt.ylabel('# of Shares in Millions')
plt.title(f'{ticker} Volume')
plt.colorbar(label='Gradient scale')
plt.grid(True)
plt.legend()
plt.show()








daily_variation =[]
for i,j in zip(opens, closes):
    daily_variation.append(j - i)
    
std_dev = np.std(daily_variation)
mean = np.mean(daily_variation)

box_df = pd.DataFrame(opens, closes)

# plt.boxplot(box_df)
# plt.show()

print(f'Standard Deviation: {std_dev}')
print(f'Mean: {mean}')

