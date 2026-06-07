import sys
import os
from datetime import datetime
from typing import Tuple, List, Optional

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.db import (
    add_expense,
    get_expense,
    get_user_expenses,
    get_user_expenses_by_month,
    delete_expense,
    get_total_expenses,
    get_current_month_expenses,
    get_expense_count,
    get_category_wise_summary,
    get_monthly_summary,
    get_user
)
from models.models import Expense


def create_expense(user_id: int, amount: float, category: str, expense_date: datetime, description: str = "") -> Tuple[bool, str]:
    """
    Create a new expense for user.
    
    Args:
        user_id: User ID
        amount: Expense amount
        category: Expense category
        expense_date: Date of expense
        description: Optional description
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Validate inputs
        if amount <= 0:
            return False, "Amount must be greater than 0"
        
        if not category:
            return False, "Please select a category"
        
        success, message, expense_id = add_expense(user_id, amount, category, expense_date, description)
        return success, message
    
    except Exception as e:
        return False, f"Error creating expense: {str(e)}"


def get_user_expense_history(user_id: int) -> Tuple[bool, str, List[dict]]:
    """
    Get expense history for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        Tuple of (success: bool, message: str, expenses: list of dicts)
    """
    try:
        expenses = get_user_expenses(user_id)
        
        expense_list = []
        for expense in expenses:
            expense_list.append({
                "id": expense.id,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date": expense.expense_date.strftime("%d-%m-%Y"),
                "created_at": expense.created_at.strftime("%d-%m-%Y %H:%M:%S")
            })
        
        return True, "Expense history retrieved successfully", expense_list
    
    except Exception as e:
        return False, f"Error retrieving expense history: {str(e)}", []


def remove_expense(expense_id: int, user_id: int) -> Tuple[bool, str]:
    """
    Delete an expense (with user verification).
    
    Args:
        expense_id: Expense ID
        user_id: User ID (to verify ownership)
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Get expense to verify ownership
        expense = get_expense(expense_id)
        
        if not expense:
            return False, "Expense not found"
        
        if expense.user_id != user_id:
            return False, "You are not authorized to delete this expense"
        
        success, message = delete_expense(expense_id)
        return success, message
    
    except Exception as e:
        return False, f"Error deleting expense: {str(e)}"


def get_dashboard_metrics(user_id: int) -> Tuple[bool, str, dict]:
    """
    Get dashboard metrics for user.
    
    Args:
        user_id: User ID
        
    Returns:
        Tuple of (success: bool, message: str, metrics: dict with total, month, count)
    """
    try:
        total_expenses = get_total_expenses(user_id)
        current_month_expenses = get_current_month_expenses(user_id)
        expense_count = get_expense_count(user_id)
        
        metrics = {
            "total_expenses": round(total_expenses, 2),
            "current_month_expenses": round(current_month_expenses, 2),
            "transaction_count": expense_count
        }
        
        return True, "Dashboard metrics retrieved successfully", metrics
    
    except Exception as e:
        return False, f"Error retrieving dashboard metrics: {str(e)}", {}


def get_recent_expenses(user_id: int, limit: int = 5) -> Tuple[bool, str, List[dict]]:
    """
    Get recent expenses for user.
    
    Args:
        user_id: User ID
        limit: Number of recent expenses to return
        
    Returns:
        Tuple of (success: bool, message: str, expenses: list of dicts)
    """
    try:
        expenses = get_user_expenses(user_id)[:limit]
        
        expense_list = []
        for expense in expenses:
            expense_list.append({
                "id": expense.id,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date": expense.expense_date.strftime("%d-%m-%Y")
            })
        
        return True, "Recent expenses retrieved successfully", expense_list
    
    except Exception as e:
        return False, f"Error retrieving recent expenses: {str(e)}", []


def get_category_summary(user_id: int) -> Tuple[bool, str, dict]:
    """
    Get category-wise expense summary for reports.
    
    Args:
        user_id: User ID
        
    Returns:
        Tuple of (success: bool, message: str, summary: dict)
    """
    try:
        summary = get_category_wise_summary(user_id)
        
        # Format for Streamlit chart
        formatted_summary = {
            "Category": list(summary.keys()),
            "Amount": [round(amount, 2) for amount in summary.values()]
        }
        
        return True, "Category summary retrieved successfully", formatted_summary
    
    except Exception as e:
        return False, f"Error retrieving category summary: {str(e)}", {}


def get_monthly_expense_summary(user_id: int, months: int = 12) -> Tuple[bool, str, dict]:
    """
    Get monthly expense summary for reports.
    
    Args:
        user_id: User ID
        months: Number of months to include in summary
        
    Returns:
        Tuple of (success: bool, message: str, summary: dict)
    """
    try:
        summary = get_monthly_summary(user_id, months)
        
        # Format for Streamlit chart
        formatted_summary = {
            "Month": list(summary.keys()),
            "Amount": [round(amount, 2) for amount in summary.values()]
        }
        
        return True, "Monthly summary retrieved successfully", formatted_summary
    
    except Exception as e:
        return False, f"Error retrieving monthly summary: {str(e)}", {}
