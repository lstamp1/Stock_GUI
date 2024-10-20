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
from tkinter.constants import LEFT
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
        
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)  # Set the menubar to the root window
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.exit_program)
        
        self.frame1 = tk.LabelFrame(self, text = 'Config')
        self.frame1.place(relx=0.05, rely=0.01, relwidth=.9, relheight=.1)
        
        self.frame2 = tk.LabelFrame(self, text = 'Analysis')
        self.frame2.place(relx=0.05, rely=0.15, relwidth=.9, relheight=.8)
        
        
        
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
        
        
        # self.create_analysis_plots()
        
        
    def create_analysis_plots(self):
        plt.clf()
        ticker = self.stock_ticker_entry.get()
        start_date = self.cal_start.get()
        end_date = self.cal_end.get()
        
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
        plt.title(f"{ticker} Stock Prices")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()

        # Embed the plot in tkinter
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame2)  # plt.gcf() gets the current figure
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        
        
        
        
        
        
        

        
        
        

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





























# # Generate the DataFrame from Yahoo Finance Data
# #data_timeframe = 365
# #today = datetime.today().strftime('%Y-%m-%d')
# #one_year_ago = (datetime.today() - timedelta(days=data_timeframe)).strftime('%Y-%m-%d')
# #symbol = "nvda"
# #yf_nvda_data = yf.download(symbol, start=today, end=one_year_ago)

# #print(f"the data looks like \n {yf_nvda_data}")


# #msft = yf.Ticker("MSFT")


# #msft.info
# #print(f"the data looks like \n {msft.info}")




# # Generate the DataFrame from CSV Data
# df = pd.read_csv("nvidia_stock_data.csv")
# print(f"The df structure looks like... \n {df}")

# # Create a second DF that will hold the new data analysis
# df_gen = df


# # Break out Columns
# dates      = df['Date']
# opens      = df['Open']
# highs      = df['High']
# lows       = df['Low']
# closes     = df['Close']
# adj_closes = df['Adj Close']
# volume     = df['Volume']


# ########################### COLUMN GEN ##################################

# # Daily Price Change
# day_results = []
# for i,j in zip(opens, closes):
#     if j > i:
#         day_results.append('Higher') # Ended Higher
#     else:
#         day_results.append('Lower') # Ended Lower
# df_gen['Daily Moves'] = day_results # Add column to new DF

# # Create column for daily moves ($)
# daily_moves_value = []
# for i,j in zip(opens, closes):
#     daily_moves_value.append(j-i)
# df_gen["Daily Moves ($)"] = daily_moves_value

# # Create column for daily moves (%)
# daily_moves_percent = []
# for i,j in zip(opens, closes):
#     daily_moves_percent.append(((j-i)/i)*100)
# df_gen["Daily Moves (%)"] = daily_moves_percent 

# # Intraday Value Change (% Change from yesterday to today)
# df_gen['Intraday Change (%)'] = df_gen['Close'].diff()

# # Volitility
# df_gen['Daily Volatility (30-day)'] = df_gen['Daily Moves (%)'].rolling(window=30).std() * np.sqrt(252)

# # High Low Daily Difference
# daily_difference_value = []
# for c,b in zip(highs, lows):
#     daily_difference_value.append(c-b)
# df_gen["High Low Daily Difference"] = daily_difference_value

# # Closes Adj_closes Daily Difference
# daily_close_diff_value = []
# for n,m in zip(closes, adj_closes):
#     daily_close_diff_value.append(m-n)
# df_gen["closes adj_closes daily difference"] = daily_close_diff_value







# print(f"New dataset = \n {df_gen}")

# ########################### ANALYSIS ##################################

# # Generate Plot
# df.plot.scatter(x = 'Date', y = 'Close')
# plt.xlabel('Date')  
# plt.ylabel('Price ($)')  
# plt.title('NVDA Price Close') 
# plt.gca().xaxis.set_major_locator(MaxNLocator(5))
# plt.grid()
# plt.show()
# #plt.plot()












# # My BreakPoint