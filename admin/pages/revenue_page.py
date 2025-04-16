import tkinter as tk
from tkinter import ttk
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.colors import COLORS
from utils.widgets import Card

class RevenuePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_main"])
        
        # Sample data for demonstration
        self.monthly_revenue = {
            "Jan": 45000, "Feb": 52000, "Mar": 48000,
            "Apr": 51000, "May": 58000, "Jun": 62000,
            "Jul": 57000, "Aug": 64000, "Sep": 67000,
            "Oct": 72000, "Nov": 68000, "Dec": 78000
        }
        
        self.daily_revenue = {
            "Mon": 8500, "Tue": 7800, "Wed": 9200,
            "Thu": 8900, "Fri": 10500, "Sat": 12000, "Sun": 11000
        }
        
        self.category_sales = {
            "South Indian": 35, "North Indian": 25,
            "Chinese": 15, "Dessert": 10, "Beverages": 15
        }
        
        # Page layout
        self.create_header()
        self.create_summary_cards()
        self.create_charts()
    
    def create_header(self):
        # Page header
        self.header = tk.Frame(self, bg=COLORS["bg_main"], height=70)
        self.header.pack(fill=tk.X, padx=20, pady=10)
        
        self.title = tk.Label(
            self.header,
            text="Revenue Dashboard",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"]
        )
        self.title.pack(side=tk.LEFT)
        
        # Period selector
        self.period_frame = tk.Frame(self.header, bg=COLORS["bg_main"])
        self.period_frame.pack(side=tk.RIGHT)
        
        self.period_label = tk.Label(
            self.period_frame,
            text="Time Period:",
            font=("Segoe UI", 11),
            bg=COLORS["bg_main"],
            fg=COLORS["text_primary"]
        )
        self.period_label.pack(side=tk.LEFT, padx=(0, 10))
        
        periods = ["Last 7 Days", "Last 30 Days", "This Month", "Last Month", "This Year"]
        self.period_combobox = ttk.Combobox(
            self.period_frame,
            values=periods,
            font=("Segoe UI", 10),
            state="readonly",
            width=15
        )
        self.period_combobox.current(2)  # Default to This Month
        self.period_combobox.pack(side=tk.RIGHT)
        
        # Style the combobox
        self.style = ttk.Style()
        self.style.configure("TCombobox", 
                            fieldbackground=COLORS["bg_main"], 
                            background=COLORS["bg_main"])
        
        # Add event binding
        self.period_combobox.bind("<<ComboboxSelected>>", self.update_data)
    
    def create_summary_cards(self):
        # Summary statistics cards
        self.summary_frame = tk.Frame(self, bg=COLORS["bg_main"])
        self.summary_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Total Revenue Card
        self.total_revenue_card = Card(self.summary_frame, width=250, height=120)
        self.total_revenue_card.pack(side=tk.LEFT, padx=(0, 10))
        
        total_revenue = sum(self.monthly_revenue.values())
        
        self.total_revenue_title = tk.Label(
            self.total_revenue_card,
            text="TOTAL REVENUE (THIS YEAR)",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        )
        self.total_revenue_title.pack(anchor="w", pady=(5, 0))
        
        self.total_revenue_value = tk.Label(
            self.total_revenue_card,
            text=f"₹{total_revenue:,.2f}",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"]
        )
        self.total_revenue_value.pack(anchor="w", pady=5)
        
        # Percentage increase from previous year
        self.total_revenue_change = tk.Label(
            self.total_revenue_card,
            text="↑ 12.5% from last year",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["secondary"]
        )
        self.total_revenue_change.pack(anchor="w")
        
        # Monthly Average Card
        self.monthly_avg_card = Card(self.summary_frame, width=250, height=120)
        self.monthly_avg_card.pack(side=tk.LEFT, padx=(0, 10))
        
        monthly_avg = sum(self.monthly_revenue.values()) / len(self.monthly_revenue)
        
        self.monthly_avg_title = tk.Label(
            self.monthly_avg_card,
            text="MONTHLY AVERAGE",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        )
        self.monthly_avg_title.pack(anchor="w", pady=(5, 0))
        
        self.monthly_avg_value = tk.Label(
            self.monthly_avg_card,
            text=f"₹{monthly_avg:,.2f}",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"]
        )
        self.monthly_avg_value.pack(anchor="w", pady=5)
        
        # Best vs worst month
        current_month = datetime.datetime.now().strftime("%b")
        self.monthly_avg_info = tk.Label(
            self.monthly_avg_card,
            text=f"Best: Dec | Worst: Jan",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        )
        self.monthly_avg_info.pack(anchor="w")
        
        # This Month Card
        this_month = datetime.datetime.now().strftime("%b")
        this_month_revenue = self.monthly_revenue.get(this_month, 0)
        
        self.this_month_card = Card(self.summary_frame, width=250, height=120)
        self.this_month_card.pack(side=tk.LEFT, padx=(0, 10))
        
        self.this_month_title = tk.Label(
            self.this_month_card,
            text=f"THIS MONTH ({this_month.upper()})",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        )
        self.this_month_title.pack(anchor="w", pady=(5, 0))
        
        self.this_month_value = tk.Label(
            self.this_month_card,
            text=f"₹{this_month_revenue:,.2f}",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"]
        )
        self.this_month_value.pack(anchor="w", pady=5)
        
        # Compare with previous month
        prev_month_idx = list(self.monthly_revenue.keys()).index(this_month) - 1
        if prev_month_idx >= 0:
            prev_month = list(self.monthly_revenue.keys())[prev_month_idx]
            prev_month_revenue = self.monthly_revenue[prev_month]
            change = ((this_month_revenue - prev_month_revenue) / prev_month_revenue) * 100
            change_text = f"↑ {change:.1f}% from {prev_month}" if change >= 0 else f"↓ {-change:.1f}% from {prev_month}"
            change_color = COLORS["secondary"] if change >= 0 else COLORS["danger"]
        else:
            change_text = "No previous data"
            change_color = COLORS["text_secondary"]
        
        self.this_month_change = tk.Label(
            self.this_month_card,
            text=change_text,
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=change_color
        )
        self.this_month_change.pack(anchor="w")
        
        # Daily Average Card
        self.daily_avg_card = Card(self.summary_frame, width=250, height=120)
        self.daily_avg_card.pack(side=tk.LEFT)
        
        daily_avg = sum(self.daily_revenue.values()) / len(self.daily_revenue)
        
        self.daily_avg_title = tk.Label(
            self.daily_avg_card,
            text="DAILY AVERAGE",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        )
        self.daily_avg_title.pack(anchor="w", pady=(5, 0))
        
        self.daily_avg_value = tk.Label(
            self.daily_avg_card,
            text=f"₹{daily_avg:,.2f}",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"]
        )
        self.daily_avg_value.pack(anchor="w", pady=5)
        
        # Best day info
        best_day = max(self.daily_revenue, key=self.daily_revenue.get)
        worst_day = min(self.daily_revenue, key=self.daily_revenue.get)
        self.daily_avg_info = tk.Label(
            self.daily_avg_card,
            text=f"Best: {best_day} | Worst: {worst_day}",
            font=("Segoe UI", 10),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        )
        self.daily_avg_info.pack(anchor="w")
    
    def create_charts(self):
        # Charts container
        self.charts_frame = tk.Frame(self, bg=COLORS["bg_main"])
        self.charts_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Monthly Revenue Chart
        self.monthly_chart_card = Card(self.charts_frame, title="Monthly Revenue")
        self.monthly_chart_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Create matplotlib figure for monthly chart
        self.monthly_fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.monthly_ax = self.monthly_fig.add_subplot(111)
        
        months = list(self.monthly_revenue.keys())
        values = list(self.monthly_revenue.values())
        
        bars = self.monthly_ax.bar(months, values, color=COLORS["primary"])
        
        # Highlight current month
        current_month = datetime.datetime.now().strftime("%b")
        if current_month in months:
            idx = months.index(current_month)
            bars[idx].set_color(COLORS["secondary"])
        
        self.monthly_ax.set_title("Monthly Revenue", fontsize=12)
        self.monthly_ax.set_ylabel("Revenue (₹)", fontsize=10)
        self.monthly_ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add data values on top of bars
        for bar in bars:
            height = bar.get_height()
            self.monthly_ax.text(bar.get_x() + bar.get_width()/2., height + 1000,
                           f'₹{int(height/1000)}K',
                           ha='center', va='bottom', rotation=0, fontsize=8)
        
        # Add the plot to the Tkinter window
        self.monthly_canvas = FigureCanvasTkAgg(self.monthly_fig, master=self.monthly_chart_card)
        self.monthly_canvas.draw()
        self.monthly_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right side - split into two charts
        self.right_charts_frame = tk.Frame(self.charts_frame, bg=COLORS["bg_main"])
        self.right_charts_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Daily Revenue Chart
        self.daily_chart_card = Card(self.right_charts_frame, title="Daily Revenue (Current Week)")
        self.daily_chart_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create matplotlib figure for daily chart
        self.daily_fig = plt.Figure(figsize=(6, 2), dpi=100)
        self.daily_ax = self.daily_fig.add_subplot(111)
        
        days = list(self.daily_revenue.keys())
        daily_values = list(self.daily_revenue.values())
        
        daily_bars = self.daily_ax.bar(days, daily_values, color=COLORS["primary"])
        
        # Highlight current day
        current_day = datetime.datetime.now().strftime("%a")
        if current_day in days:
                idx = days.index(current_day)
                daily_bars[idx].set_color(COLORS["secondary"])
        
        self.daily_ax.set_title("Daily Revenue", fontsize=12)
        self.daily_ax.set_ylabel("Revenue (₹)", fontsize=10)
        self.daily_ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        for bar in daily_bars:
            height = bar.get_height()
            self.daily_ax.text(bar.get_x() + bar.get_width()/2., height + 500,
                               f'₹{int(height/1000)}K',
                               ha='center', va='bottom', rotation=0, fontsize=8)
        
        self.daily_canvas = FigureCanvasTkAgg(self.daily_fig, master=self.daily_chart_card)
        self.daily_canvas.draw()
        self.daily_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Category Sales Chart
        self.category_chart_card = Card(self.right_charts_frame, title="Sales by Category")
        self.category_chart_card.pack(fill=tk.BOTH, expand=True)
        
        self.category_fig = plt.Figure(figsize=(6, 2), dpi=100)
        self.category_ax = self.category_fig.add_subplot(111)
        
        categories = list(self.category_sales.keys())
        sales_values = list(self.category_sales.values())
        
        # Use a safe list of colors that are guaranteed to be in the COLORS dictionary
        chart_colors = [
            COLORS["primary"], 
            COLORS["secondary"], 
            COLORS["warning"], 
            COLORS["danger"],
            COLORS.get("accent", "#9b59b6"),  # Use get() with fallback
            COLORS.get("info", "#1abc9c")     # Use get() with fallback
        ]
        
        self.category_ax.pie(sales_values, labels=categories, autopct='%1.1f%%', colors=chart_colors[:len(categories)])
        self.category_ax.set_title("Sales by Category", fontsize=12)
        
        self.category_canvas = FigureCanvasTkAgg(self.category_fig, master=self.category_chart_card)
        self.category_canvas.draw()
        self.category_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def update_data(self, event=None):
        # Placeholder for updating data based on selected period
        selected_period = self.period_combobox.get()
        print(f"Updating data for: {selected_period}")
