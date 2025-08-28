#!/usr/bin/env python3
"""
Script to populate the ticketing system with knowledge base-based sample data
This ensures tickets are based on actual knowledge base content rather than generic examples
"""

import sqlite3
from datetime import datetime, timedelta
import os

def populate_ticketing_with_kb():
    """Populate ticketing system with KB-based sample data"""
    
    # Connect to the ticketing database
    db_path = "ticketing_tool/tickets.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        print("Please start the ticketing system first to create the database")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing sample tickets (keep structure)
    cursor.execute("DELETE FROM tickets WHERE ticket_number LIKE 'TKT-%'")
    cursor.execute("DELETE FROM ticket_comments WHERE ticket_id IN (SELECT id FROM tickets WHERE ticket_number LIKE 'TKT-%')")
    cursor.execute("DELETE FROM ticket_history WHERE ticket_id IN (SELECT id FROM tickets WHERE ticket_number LIKE 'TKT-%')")
    
    # Knowledge base-based sample tickets
    kb_tickets = [
        {
            'ticket_number': 'TKT-001',
            'title': 'Payment declined for subscription renewal - need immediate resolution',
            'description': 'My credit card payment was declined when trying to renew my subscription. The card has sufficient funds and is not expired. I need help resolving this payment issue as my subscription expires today.',
            'user_id': 1,
            'category_id': 2,  # Billing
            'priority_id': 1,  # High
            'status_id': 1,    # Open
            'tags': 'payment,subscription,billing,declined,renewal'
        },
        {
            'ticket_number': 'TKT-002',
            'title': 'Cannot access account after password reset - locked out',
            'description': 'I reset my password yesterday but now I cannot log into my account. The system keeps saying "invalid credentials" even with the new password. I\'m completely locked out and need urgent help.',
            'user_id': 2,
            'category_id': 1,  # Account Access
            'priority_id': 1,  # High
            'status_id': 1,    # Open
            'tags': 'login,password,account,locked-out,reset'
        },
        {
            'ticket_number': 'TKT-003',
            'title': 'Two-factor authentication setup not working',
            'description': 'I\'m trying to set up 2FA for my account but the QR code won\'t scan and the manual entry code doesn\'t work. I\'ve tried multiple authenticator apps. Need step-by-step guidance.',
            'user_id': 3,
            'category_id': 4,  # Security
            'priority_id': 2,  # Medium
            'status_id': 1,    # Open
            'tags': '2fa,security,authentication,setup,qr-code'
        },
        {
            'ticket_number': 'TKT-004',
            'title': 'Dashboard performance issues - very slow loading',
            'description': 'The dashboard has been extremely slow for the past week, taking 15-20 seconds to load. This affects my daily workflow. I\'ve cleared cache and tried different browsers.',
            'user_id': 4,
            'category_id': 3,  # Technical
            'priority_id': 2,  # Medium
            'status_id': 1,    # Open
            'tags': 'performance,slow,dashboard,loading,technical'
        },
        {
            'ticket_number': 'TKT-005',
            'title': 'Invoice missing for last billing cycle',
            'description': 'I haven\'t received an invoice for last month\'s usage. I need this for my accounting records and to verify the charges. Please resend the invoice.',
            'user_id': 5,
            'category_id': 2,  # Billing
            'priority_id': 3,  # Low
            'status_id': 1,    # Open
            'tags': 'invoice,billing,missing,accounting,charges'
        },
        {
            'ticket_number': 'TKT-006',
            'title': 'Suspicious login attempt from unknown location',
            'description': 'I received an email about a suspicious login attempt from an IP address I don\'t recognize. I want to secure my account and understand what happened.',
            'user_id': 1,
            'category_id': 5,  # Security
            'priority_id': 1,  # High
            'status_id': 1,    # Open
            'tags': 'security,breach,login,suspicious,ip-address'
        },
        {
            'ticket_number': 'TKT-007',
            'title': 'Mobile app crashes when accessing settings',
            'description': 'The mobile app crashes immediately when I try to access the settings page. This happens on both my iPhone and iPad. I need to change my preferences.',
            'user_id': 2,
            'category_id': 3,  # Technical
            'priority_id': 2,  # Medium
            'status_id': 1,    # Open
            'tags': 'mobile,app,crash,settings,ios,technical'
        },
        {
            'ticket_number': 'TKT-008',
            'title': 'Subscription plan change not reflected in billing',
            'description': 'I upgraded my subscription plan last week but the billing still shows the old rate. The change should have taken effect immediately. Need help correcting this.',
            'user_id': 3,
            'category_id': 2,  # Billing
            'priority_id': 2,  # Medium
            'status_id': 1,    # Open
            'tags': 'subscription,plan-change,billing,upgrade,rate'
        }
    ]
    
    # Insert KB-based tickets
    for ticket in kb_tickets:
        cursor.execute("""
            INSERT INTO tickets (ticket_number, title, description, user_id, category_id, 
                               priority_id, status_id, assigned_to, created_at, due_date, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket['ticket_number'],
            ticket['title'],
            ticket['description'],
            ticket['user_id'],
            ticket['category_id'],
            ticket['priority_id'],
            ticket['status_id'],
            None,  # assigned_to
            datetime.now() - timedelta(hours=kb_tickets.index(ticket) + 1),
            None,  # due_date
            ticket['tags']
        ))
    
    # Add some sample comments based on knowledge base content
    sample_comments = [
        (1, 4, 'I can see the payment was declined due to a security flag on your account. This is a common issue after password changes. I\'ve cleared the flag and you should be able to retry the payment now.', 0),
        (2, 4, 'I can see from our logs that there was a recent password reset. Sometimes the new password doesn\'t sync immediately. I\'ve sent a new temporary password to your email.', 0),
        (3, 4, 'The 2FA setup issue is often related to time synchronization. Please ensure your device time is set to automatic. I\'ve also generated a new setup code for you.', 0),
        (4, 4, 'I\'m investigating the performance issue. Our monitoring shows increased response times in your region. This should be resolved within the next few hours.', 0),
        (5, 4, 'I\'ve located your invoice and resent it to your email. The invoice was generated but there was a delivery issue. You should receive it shortly.', 0),
        (6, 4, 'I\'ve reviewed the login attempt and it appears to be from a legitimate location. However, I\'ve enabled additional security measures on your account as a precaution.', 0),
        (7, 4, 'This is a known issue with the latest mobile app version. I\'ve escalated this to our development team. As a workaround, you can access settings through the web interface.', 0),
        (8, 4, 'I can see the plan change in our system. There was a delay in the billing update. Your new rate will be reflected in the next billing cycle, and I\'ve credited the difference.', 0)
    ]
    
    for comment in sample_comments:
        cursor.execute("""
            INSERT INTO ticket_comments (ticket_id, user_id, comment, is_internal)
            VALUES (?, ?, ?, ?)
        """, comment)
    
    # Add some status change history
    history_data = [
        (1, 4, 'Status Changed', 'Open', 'In Progress'),
        (2, 4, 'Status Changed', 'Open', 'In Progress'),
        (3, 4, 'Status Changed', 'Open', 'In Progress'),
        (4, 4, 'Status Changed', 'Open', 'In Progress'),
        (6, 4, 'Status Changed', 'Open', 'In Progress')
    ]
    
    for history in history_data:
        cursor.execute("""
            INSERT INTO ticket_history (ticket_id, user_id, action, old_value, new_value)
            VALUES (?, ?, ?, ?, ?)
        """, history)
    
    conn.commit()
    conn.close()
    
    print("✅ Ticketing system populated with knowledge base-based sample data")
    print(f"📋 Added {len(kb_tickets)} tickets based on actual support scenarios")
    print("🔗 Tickets now align with knowledge base content for better AI resolution")

if __name__ == "__main__":
    populate_ticketing_with_kb()
