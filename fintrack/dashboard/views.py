from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Data, limitData
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
import json
from .forms import ReportForm
import pandas as pd
import threading
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import warnings
warnings.simplefilter("ignore", UserWarning)
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(custom_login)  # Redirect to the home page after successful registration
    else:
        form = SignupForm()
    return render(request, 'dashboard/signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(dashboard)  # Redirect to the home page after successful login
        else:
            return HttpResponse('Invalid login credentials')
    return render(request, 'dashboard/login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def categories(request):
    entries = Data.objects.all()
    return render(request, 'dashboard/categories.html',{'entries':entries})

@login_required
def budget(request):
    entries = limitData.objects.all()
    return render(request, 'dashboard/budget.html',{'entries':entries})

@login_required
def expenseprediction(request):
    return render(request, 'dashboard/expenseprediction.html')

@login_required
def generatereport(request):
    return render(request, 'dashboard/reportdash.html')

@login_required
def analysis(request):
    return render(request, 'dashboard/analysis.html')


def form_view(request):
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        account = request.POST.get('account')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        category_type = request.POST.get('category_type')
        # Create and save the expense record to the database
        expense = Data(
            amount=amount,
            category=category,
            account=account,
            date=date,
            time=time,
            description=description,
            category_type=category_type
        )
        print(expense)
        expense.save()
        
        return redirect('/categories')  # Replace 'success_url' with your desired URL

    return render(request, 'dashboard/categories.html')  # Render the form initially

def limitGraph():
        data_from_database = limitData.objects.all()
        print(data_from_database)
# Organize the data into the desired format
        budget_data = {
            'Category': [entry.category for entry in data_from_database],
            'Budget_Limit': [entry.limit for entry in data_from_database]
        }
        # budget_data = {
        #     'Category': ['Food', 'Housing', 'Transportation', 'Entertainment'],
        #     'Budget_Limit': [1000, 2000, 500, 300]
        # }
        budget_df = pd.DataFrame(budget_data)

        # Step 2: Load Expense Data (Replace this with your expense data loading logic)
        # expense_data = {
        #     'Category': ['Food', 'Housing', 'Transportation', 'Food', 'Entertainment'],
        #     'Amount': [1100, 1900, 450, 1200, 350]
        # }
        data_from_data = Data.objects.filter(category_type='Expense')
        print(data_from_data)
# Organize the data into the desired format
        expense_data = {
            'Category': [entry.category for entry in data_from_data],
            'Amount': [entry.amount for entry in data_from_data]
        }
        expense_df = pd.DataFrame(expense_data)

        # Step 3: Calculate Category-wise Expenses
        category_expenses = expense_df.groupby('Category')['Amount'].sum().reset_index()

        # Step 4: Check Budget Exceedance
        category_expenses['Exceeds_Budget'] = category_expenses['Amount'] > budget_df['Budget_Limit']

        # Step 5: Plot Expenses
        plt.figure(figsize=(10, 6))
        plt.bar(category_expenses['Category'], category_expenses['Amount'], color=['green' if not exceeds else 'red' for exceeds in category_expenses['Exceeds_Budget']])
        plt.xlabel('Expense Category')
        plt.ylabel('Total Expense Amount')
        plt.title('Category-wise Expenses')
        plt.axhline(y=budget_df['Budget_Limit'].values[0], color='green', linestyle='--', label='Budget Limit')
        plt.legend()
        plt.grid(True)

        # Add alerts for exceeded budgets
        for i, exceeds in enumerate(category_expenses['Exceeds_Budget']):
            if exceeds:
                plt.text(i, category_expenses['Amount'].iloc[i] + 50, 'Exceeds Budget', color='red', ha='center')

        # Check if expenses exceed the budget limits and set a flag
        budget_alert = {}
        for category, limit in budget_data.items():
            if category in expense_data:
                if expense_data[category] > limit:
                    budget_alert[category] = True  # Set the budget alert flag for this category
                else:
                    budget_alert[category] = False
            else:
                budget_alert[category] = False

        # Function to display budget alerts
        def display_budget_alerts(alerts):
            for category, is_alert in alerts.items():
                if is_alert:
                    print(f'Alert: Budget for {category} exceeded!')
                    messagebox.showwarning('Budget Alert', f'Budget for {category} exceeded!')
                else:
                    print(f'Budget for {category} is within limit.')

        # Display budget alerts
        display_budget_alerts(budget_alert)

        # Show the plot
        plt.show()
        #return render(request, 'dashboard/budget.html')

def limitdata(request):
    print("limitdata")
    if request.method == 'POST':
        limit = request.POST.get('limit')
        category = request.POST.get('category')
        date = request.POST.get('date')
        # Create and save the expense record to the database
        expense = limitData(
            category=category,
            limit=limit,
            date=date
        )
        expense.save()
        # budget_data = {
        #     'Category': ['Food', 'Housing', 'Transportation', 'Entertainment'],
        #     'Budget_Limit': [1000, 2000, 500, 300]
        # }
        # budget_df = pd.DataFrame(budget_data)

        # # Step 2: Load Expense Data (Replace this with your expense data loading logic)
        # expense_data = {
        #     'Category': ['Food', 'Housing', 'Transportation', 'Food', 'Entertainment'],
        #     'Amount': [1100, 1900, 450, 1200, 350]
        # }
        # expense_df = pd.DataFrame(expense_data)

        # # Step 3: Calculate Category-wise Expenses
        # category_expenses = expense_df.groupby('Category')['Amount'].sum().reset_index()

        # # Step 4: Check Budget Exceedance
        # category_expenses['Exceeds_Budget'] = category_expenses['Amount'] > budget_df['Budget_Limit']

        # # Step 5: Plot Expenses
        # plt.figure(figsize=(10, 6))
        # plt.bar(category_expenses['Category'], category_expenses['Amount'], color=['green' if not exceeds else 'red' for exceeds in category_expenses['Exceeds_Budget']])
        # plt.xlabel('Expense Category')
        # plt.ylabel('Total Expense Amount')
        # plt.title('Category-wise Expenses')
        # plt.axhline(y=budget_df['Budget_Limit'].values[0], color='green', linestyle='--', label='Budget Limit')
        # plt.legend()
        # plt.grid(True)

        # # Add alerts for exceeded budgets
        # for i, exceeds in enumerate(category_expenses['Exceeds_Budget']):
        #     if exceeds:
        #         plt.text(i, category_expenses['Amount'].iloc[i] + 50, 'Exceeds Budget', color='red', ha='center')

        # # Check if expenses exceed the budget limits and set a flag
        # budget_alert = {}
        # for category, limit in budget_data.items():
        #     if category in expense_data:
        #         if expense_data[category] > limit:
        #             budget_alert[category] = True  # Set the budget alert flag for this category
        #         else:
        #             budget_alert[category] = False
        #     else:
        #         budget_alert[category] = False

        # # Function to display budget alerts
        # def display_budget_alerts(alerts):
        #     for category, is_alert in alerts.items():
        #         if is_alert:
        #             print(f'Alert: Budget for {category} exceeded!')
        #             messagebox.showwarning('Budget Alert', f'Budget for {category} exceeded!')
        #         else:
        #             print(f'Budget for {category} is within limit.')

        # # Display budget alerts
        # display_budget_alerts(budget_alert)

        # # Show the plot
        # plt.show()
        def on_closing():
    # Perform any cleanup or resource release here
            root.destroy()
        root = tk.Tk()
        root.attributes('-topmost', True)
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.withdraw()
# Use threading to run the message box call in the main thread
        t = threading.Thread(target=limitGraph)
        t.start()
        root.mainloop()

    return redirect('/budget')  # Replace 'success_url' with your desired URL


def predict_expense(request):
    data_from_database = Data.objects.all()

    # Initialize empty lists for each field in your format
    expense_list = []
    category_list = []
    amount_list = []
    date_list = []
    time_list = []

    # Iterate through the data and populate the lists
    for entry in data_from_database:
        expense_list.append(entry.category_type)
        category_list.append(entry.category)
        amount_list.append(entry.amount)
        date_list.append(entry.date.strftime('%m-%d-%Y'))
        time_list.append(entry.time.strftime('%H:%M'))

    # Create a dictionary in the desired format
    data = {
        'expense': expense_list,
        'category': category_list,
        'amount': amount_list,
        'date': date_list,
        'time': time_list
    }

# Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Split the 'date' column into 'day', 'month', and 'year'
    df[['day', 'month', 'year']] = df['date'].str.split('-', expand=True)

    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Split the 'datetime' column into 'day', 'month', 'year', 'hour', 'minute'
    df['day'] = df['datetime'].dt.day
    df['month'] = df['datetime'].dt.month
    df['year'] = df['datetime'].dt.year
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    # Encode categorical variables using one-hot encoding
    df_encoded = pd.get_dummies(df, columns=['expense', 'category'])

    # Split data into features (X) and target (y)
    X = df_encoded[['day', 'month', 'year', 'hour', 'minute']]
    y = df_encoded['amount']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Select a machine learning model (Linear Regression)
    model = LinearRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Predict future expenses
    # Let's predict expenses for some future dates
    # You can replace these dates with your own desired prediction dates
    future_dates = pd.date_range(start='2023-03-01', end='2023-4-30', freq='D')
    future_data = pd.DataFrame({'day': future_dates.day,
                                'month': future_dates.month,
                                'year': future_dates.year,
                                'hour': 0,
                                'minute': 0})

    # Predict future expenses using the trained model
    future_predictions = model.predict(future_data)

    # Visualize the predictions
    plt.figure(figsize=(12, 6))
    plt.plot(future_dates, future_predictions, label='Predicted Expenses', color='b')
    plt.xlabel('Date')
    plt.ylabel('Expense Amount')
    plt.title('Predicted Future Expenses')
    plt.legend()
    plt.grid(True)
    plt.show()
    return render(request, 'dashboard/expenseprediction.html')

def showanalysis(request):
    expenses = Data.objects.filter(category_type='Expense').values('amount', 'category')
    expenses_serialized = json.dumps(list(expenses.values()), cls=DjangoJSONEncoder)
    return render(request, 'dashboard/showanalysis.html',{'expenses_json': expenses_serialized})

def export_report(request, period):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            print(period)
            if period == 'monthly':
                # Generate monthly report based on user input
                data = Data.objects.filter(date__year=year, date__month=month)
            elif period == 'yearly':
                # Generate yearly report based on user input
                data = Data.objects.filter(date__year=year)
            else:
                # Handle invalid period parameter
                return HttpResponse("Invalid period parameter")
            
            df = pd.DataFrame(list(data.values()))
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename={period}_report.xlsx'
            df.to_excel(response, index=False, engine='openpyxl')
            return response
    else:
        form = ReportForm()
    context = {'form': form, 'period': period}
    return render(request, 'dashboard/generatereport.html', context)