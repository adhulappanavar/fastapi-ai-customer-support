#!/usr/bin/env python3
"""
SQLite Database Module for Ticket Management System
Handles database initialization, schema creation, and sample data
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json

class TicketDatabase:
    def __init__(self, db_path: str = "tickets.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn
    
    def init_database(self):
        """Initialize database with schema and sample data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create tables
        self.create_tables(cursor)
        
        # Insert sample data if tables are empty
        if self.is_empty(cursor):
            self.insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized: {self.db_path}")
    
    def create_tables(self, cursor):
        """Create all necessary tables"""
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                role VARCHAR(20) DEFAULT 'customer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) UNIQUE NOT NULL,
                description TEXT,
                sla_hours INTEGER DEFAULT 24,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Priority levels table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS priority_levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(20) UNIQUE NOT NULL,
                description TEXT,
                sla_hours INTEGER NOT NULL,
                color VARCHAR(7) DEFAULT '#000000',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Status table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) UNIQUE NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                color VARCHAR(7) DEFAULT '#000000',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tickets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_number VARCHAR(20) UNIQUE NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                priority_id INTEGER NOT NULL,
                status_id INTEGER NOT NULL,
                assigned_to INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                due_date TIMESTAMP,
                tags TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (category_id) REFERENCES categories (id),
                FOREIGN KEY (priority_id) REFERENCES priority_levels (id),
                FOREIGN KEY (status_id) REFERENCES statuses (id),
                FOREIGN KEY (assigned_to) REFERENCES users (id)
            )
        """)
        
        # Ticket comments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticket_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                comment TEXT NOT NULL,
                is_internal BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Ticket history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticket_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                action VARCHAR(100) NOT NULL,
                old_value TEXT,
                new_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON tickets(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_status_id ON tickets(status_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_priority_id ON tickets(priority_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_category_id ON tickets(category_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ticket_comments_ticket_id ON ticket_comments(ticket_id)")
    
    def is_empty(self, cursor) -> bool:
        """Check if tables are empty"""
        cursor.execute("SELECT COUNT(*) FROM tickets")
        return cursor.fetchone()[0] == 0
    
    def insert_sample_data(self, cursor):
        """Insert sample data for demonstration"""
        
        # Insert users
        users_data = [
            ('john_doe', 'john.doe@example.com', 'John Doe', 'customer'),
            ('jane_smith', 'jane.smith@example.com', 'Jane Smith', 'customer'),
            ('bob_wilson', 'bob.wilson@example.com', 'Bob Wilson', 'customer'),
            ('support_agent1', 'support1@company.com', 'Sarah Johnson', 'support_agent'),
            ('support_agent2', 'support2@company.com', 'Mike Chen', 'support_agent'),
            ('admin_user', 'admin@company.com', 'Admin User', 'admin')
        ]
        
        cursor.executemany("""
            INSERT INTO users (username, email, full_name, role)
            VALUES (?, ?, ?, ?)
        """, users_data)
        
        # Insert categories
        categories_data = [
            ('Account Access', 'Login, password, and account management issues', 4),
            ('Billing & Payments', 'Payment processing, invoices, and subscription issues', 6),
            ('Technical Support', 'Software bugs, performance issues, and technical problems', 8),
            ('Product Features', 'How-to questions and feature requests', 12),
            ('Security Issues', 'Security concerns and account compromise', 2),
            ('General Support', 'General inquiries and other support needs', 24)
        ]
        
        cursor.executemany("""
            INSERT INTO categories (name, description, sla_hours)
            VALUES (?, ?, ?)
        """, categories_data)
        
        # Insert priority levels
        priority_data = [
            ('Critical', 'System down or security breach', 1, '#dc2626'),
            ('High', 'Cannot access account or critical functionality', 4, '#ea580c'),
            ('Medium', 'Feature not working or performance issues', 8, '#ca8a04'),
            ('Low', 'General questions or minor issues', 24, '#16a34a')
        ]
        
        cursor.executemany("""
            INSERT INTO priority_levels (name, description, sla_hours, color)
            VALUES (?, ?, ?, ?)
        """, priority_data)
        
        # Insert statuses
        status_data = [
            ('Open', 'Ticket is open and awaiting response', '#16a34a'),
            ('In Progress', 'Ticket is being worked on', '#ca8a04'),
            ('Waiting for Customer', 'Awaiting customer response', '#ea580c'),
            ('Resolved', 'Issue has been resolved', '#059669'),
            ('Closed', 'Ticket has been closed', '#6b7280'),
            ('Escalated', 'Ticket has been escalated to higher level', '#dc2626')
        ]
        
        cursor.executemany("""
            INSERT INTO statuses (name, description, color)
            VALUES (?, ?, ?)
        """, status_data)
        
        # Insert sample tickets
        tickets_data = [
            ('TKT-001', 'Cannot log into account after password change', 
             'I changed my password yesterday and now I cannot log into my account. I\'ve tried the new password multiple times but it keeps saying "invalid credentials".', 
             1, 1, 2, 1, None, datetime.now() - timedelta(hours=2), None, 'login,password,account'),
            
            ('TKT-002', 'Payment declined for subscription renewal',
             'My credit card payment was declined when trying to renew my subscription. The card has sufficient funds and is not expired. I need help resolving this issue.',
             2, 2, 2, 1, None, datetime.now() - timedelta(hours=1), None, 'payment,subscription,billing'),
            
            ('TKT-003', 'App crashes when opening settings page',
             'Every time I try to open the settings page in the mobile app, it crashes immediately. This happens on both iOS and Android devices. I need to access my preferences.',
             3, 3, 3, 1, None, datetime.now() - timedelta(minutes=30), None, 'crash,bug,mobile,settings'),
            
            ('TKT-004', 'How to enable two-factor authentication',
             'I want to set up two-factor authentication for my account but I cannot find the option in the security settings. Can you guide me through the process?',
             4, 4, 4, 1, None, datetime.now() - timedelta(hours=3), None, '2fa,security,authentication'),
            
            ('TKT-005', 'Suspicious login attempt detected',
             'I received an email about a suspicious login attempt from an unknown location. I want to secure my account and investigate this security concern.',
             5, 5, 1, 1, None, datetime.now() - timedelta(minutes=15), None, 'security,breach,login'),
            
            ('TKT-006', 'Slow performance on dashboard',
             'The dashboard is loading very slowly, taking 10-15 seconds to display data. This has been happening for the past week and affects my productivity.',
             3, 3, 3, 2, 4, datetime.now() - timedelta(days=1), None, 'performance,slow,dashboard'),
            
            ('TKT-007', 'Invoice not received for last month',
             'I haven\'t received an invoice for last month\'s usage. I need the invoice for my records and accounting purposes. Can you resend it?',
             2, 2, 4, 1, None, datetime.now() - timedelta(hours=4), None, 'invoice,billing,missing'),
            
            ('TKT-008', 'Feature request: Dark mode theme',
             'I would like to request a dark mode theme for the application. This would be very helpful for users who work in low-light environments.',
             4, 4, 4, 1, None, datetime.now() - timedelta(days=2), None, 'feature,request,dark-mode,theme')
        ]
        
        cursor.executemany("""
            INSERT INTO tickets (ticket_number, title, description, user_id, category_id, priority_id, status_id, assigned_to, created_at, due_date, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tickets_data)
        
        # Insert sample comments
        comments_data = [
            (1, 4, 'Thank you for reporting this issue. I can see from our logs that there was a recent password change. Let me help you troubleshoot this.', 0),
            (1, 4, 'I\'ve reset your password and sent a new temporary password to your email. Please check your inbox and let me know if you need any further assistance.', 0),
            (2, 4, 'I can see the payment was declined due to a security flag. I\'ve cleared this and you should be able to retry the payment now.', 0),
            (6, 4, 'I\'m investigating the performance issue. I can see increased response times in our monitoring. This should be resolved within the next few hours.', 0),
            (6, 4, 'The performance issue has been resolved. The dashboard should now load much faster. Please test and let me know if you still experience any delays.', 0)
        ]
        
        cursor.executemany("""
            INSERT INTO ticket_comments (ticket_id, user_id, comment, is_internal)
            VALUES (?, ?, ?, ?)
        """, comments_data)
        
        # Insert sample history
        history_data = [
            (1, 4, 'Status Changed', 'Open', 'In Progress'),
            (1, 4, 'Status Changed', 'In Progress', 'Resolved'),
            (2, 4, 'Status Changed', 'Open', 'In Progress'),
            (6, 4, 'Status Changed', 'Open', 'In Progress'),
            (6, 4, 'Status Changed', 'In Progress', 'Resolved')
        ]
        
        cursor.executemany("""
            INSERT INTO ticket_history (ticket_id, user_id, action, old_value, new_value)
            VALUES (?, ?, ?, ?, ?)
        """, history_data)
        
        print("✅ Sample data inserted successfully")
    
    def get_tickets(self, limit: int = 50, offset: int = 0, status_id: Optional[int] = None, 
                    priority_id: Optional[int] = None, category_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get tickets with optional filtering"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                t.*,
                u.username as user_username,
                u.full_name as user_full_name,
                c.name as category_name,
                p.name as priority_name,
                p.color as priority_color,
                s.name as status_name,
                s.color as status_color,
                a.username as assigned_username,
                a.full_name as assigned_full_name
            FROM tickets t
            JOIN users u ON t.user_id = u.id
            JOIN categories c ON t.category_id = c.id
            JOIN priority_levels p ON t.priority_id = p.id
            JOIN statuses s ON t.status_id = s.id
            LEFT JOIN users a ON t.assigned_to = a.id
        """
        
        params = []
        where_clauses = []
        
        if status_id:
            where_clauses.append("t.status_id = ?")
            params.append(status_id)
        
        if priority_id:
            where_clauses.append("t.priority_id = ?")
            params.append(priority_id)
        
        if category_id:
            where_clauses.append("t.category_id = ?")
            params.append(category_id)
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " ORDER BY t.created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        tickets = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return tickets
    
    def get_ticket(self, ticket_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific ticket by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                t.*,
                u.username as user_username,
                u.full_name as user_full_name,
                c.name as category_name,
                p.name as priority_name,
                p.color as priority_color,
                s.name as status_name,
                s.color as status_color,
                a.username as assigned_username,
                a.full_name as assigned_full_name
            FROM tickets t
            JOIN users u ON t.user_id = u.id
            JOIN categories c ON t.category_id = c.id
            JOIN priority_levels p ON t.priority_id = p.id
            JOIN statuses s ON t.status_id = s.id
            LEFT JOIN users a ON t.assigned_to = a.id
            WHERE t.id = ?
        """, (ticket_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def create_ticket(self, ticket_data: Dict[str, Any]) -> int:
        """Create a new ticket"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Generate ticket number
        cursor.execute("SELECT COUNT(*) FROM tickets")
        count = cursor.fetchone()[0]
        ticket_number = f"TKT-{str(count + 1).zfill(3)}"
        
        cursor.execute("""
            INSERT INTO tickets (ticket_number, title, description, user_id, category_id, priority_id, status_id, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_number,
            ticket_data['title'],
            ticket_data['description'],
            ticket_data['user_id'],
            ticket_data['category_id'],
            ticket_data['priority_id'],
            ticket_data['status_id'],
            ticket_data.get('tags', '')
        ))
        
        ticket_id = cursor.lastrowid
        
        # Add to history
        cursor.execute("""
            INSERT INTO ticket_history (ticket_id, user_id, action, new_value)
            VALUES (?, ?, ?, ?)
        """, (ticket_id, ticket_data['user_id'], 'Ticket Created', ticket_data['title']))
        
        conn.commit()
        conn.close()
        
        return ticket_id
    
    def update_ticket(self, ticket_id: int, update_data: Dict[str, Any], user_id: int) -> bool:
        """Update a ticket"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current values for history
        cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        current = cursor.fetchone()
        if not current:
            conn.close()
            return False
        
        # Build update query
        set_clauses = []
        params = []
        
        for key, value in update_data.items():
            if key in ['title', 'description', 'category_id', 'priority_id', 'status_id', 'assigned_to', 'tags']:
                set_clauses.append(f"{key} = ?")
                params.append(value)
        
        if not set_clauses:
            conn.close()
            return False
        
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        params.append(ticket_id)
        
        query = f"UPDATE tickets SET {', '.join(set_clauses)} WHERE id = ?"
        cursor.execute(query, params)
        
        # Add to history
        for key, value in update_data.items():
            if key in ['title', 'description', 'category_id', 'priority_id', 'status_id', 'assigned_to']:
                old_value = str(current[key])
                new_value = str(value)
                if old_value != new_value:
                    cursor.execute("""
                        INSERT INTO ticket_history (ticket_id, user_id, action, old_value, new_value)
                        VALUES (?, ?, ?, ?, ?)
                    """, (ticket_id, user_id, f'{key.title()} Changed', old_value, new_value))
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return categories
    
    def get_priority_levels(self) -> List[Dict[str, Any]]:
        """Get all priority levels"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM priority_levels ORDER BY sla_hours")
        priorities = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return priorities
    
    def get_statuses(self) -> List[Dict[str, Any]]:
        """Get all statuses"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM statuses WHERE is_active = 1 ORDER BY name")
        statuses = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return statuses
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users ORDER BY full_name")
        users = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return users
    
    def get_ticket_stats(self) -> Dict[str, Any]:
        """Get ticket statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total tickets
        cursor.execute("SELECT COUNT(*) FROM tickets")
        total_tickets = cursor.fetchone()[0]
        
        # Open tickets
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status_id IN (1, 2, 3)")
        open_tickets = cursor.fetchone()[0]
        
        # Resolved tickets
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status_id = 4")
        resolved_tickets = cursor.fetchone()[0]
        
        # Critical priority tickets
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority_id = 1 AND status_id IN (1, 2, 3)")
        critical_tickets = cursor.fetchone()[0]
        
        # Tickets by category
        cursor.execute("""
            SELECT c.name, COUNT(*) as count
            FROM tickets t
            JOIN categories c ON t.category_id = c.id
            GROUP BY c.id, c.name
            ORDER BY count DESC
        """)
        tickets_by_category = [dict(row) for row in cursor.fetchall()]
        
        # Tickets by priority
        cursor.execute("""
            SELECT p.name, COUNT(*) as count
            FROM tickets t
            JOIN priority_levels p ON t.priority_id = p.id
            GROUP BY p.id, p.name
            ORDER BY p.sla_hours
        """)
        tickets_by_priority = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'resolved_tickets': resolved_tickets,
            'critical_tickets': critical_tickets,
            'tickets_by_category': tickets_by_category,
            'tickets_by_priority': tickets_by_priority
        }

# Initialize database when module is imported
db = TicketDatabase()
