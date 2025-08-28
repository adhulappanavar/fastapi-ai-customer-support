#!/usr/bin/env python3
"""
Test Script for Ticket Management System
Demonstrates the API functionality with sample requests
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on port 8000")
        return False
    return True

def test_get_tickets():
    """Test getting tickets"""
    print("\n🎫 Testing Get Tickets...")
    try:
        response = requests.get(f"{BASE_URL}/tickets?limit=5")
        if response.status_code == 200:
            tickets = response.json()
            print(f"✅ Retrieved {len(tickets)} tickets")
            for ticket in tickets[:3]:  # Show first 3
                print(f"   {ticket['ticket_number']}: {ticket['title']} ({ticket['status_name']})")
        else:
            print(f"❌ Failed to get tickets: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_ticket_details():
    """Test getting a specific ticket"""
    print("\n🔍 Testing Get Ticket Details...")
    try:
        response = requests.get(f"{BASE_URL}/tickets/1")
        if response.status_code == 200:
            ticket = response.json()
            print(f"✅ Retrieved ticket {ticket['ticket_number']}")
            print(f"   Title: {ticket['title']}")
            print(f"   Status: {ticket['status_name']}")
            print(f"   Priority: {ticket['priority_name']}")
            print(f"   Category: {ticket['category_name']}")
            print(f"   User: {ticket['user_full_name']}")
        else:
            print(f"❌ Failed to get ticket: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_create_ticket():
    """Test creating a new ticket"""
    print("\n➕ Testing Create Ticket...")
    
    new_ticket = {
        "title": "Test ticket from API",
        "description": "This is a test ticket created via the API to verify the system is working correctly.",
        "user_id": 1,
        "category_id": 1,
        "priority_id": 3,
        "tags": "test,api,verification"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/tickets", json=new_ticket)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ticket created successfully")
            print(f"   Ticket ID: {result['ticket_id']}")
            print(f"   Ticket Number: {result['ticket_number']}")
            return result['ticket_id']
        else:
            print(f"❌ Failed to create ticket: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

def test_update_ticket(ticket_id):
    """Test updating a ticket"""
    if not ticket_id:
        return
    
    print(f"\n✏️  Testing Update Ticket {ticket_id}...")
    
    update_data = {
        "status_id": 2,  # Change to "In Progress"
        "assigned_to": 4,  # Assign to support agent
        "tags": "test,api,verification,updated"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/tickets/{ticket_id}?user_id=4", json=update_data)
        if response.status_code == 200:
            print("✅ Ticket updated successfully")
            print("   Status changed to 'In Progress'")
            print("   Assigned to support agent")
        else:
            print(f"❌ Failed to update ticket: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_categories():
    """Test getting categories"""
    print("\n📂 Testing Get Categories...")
    try:
        response = requests.get(f"{BASE_URL}/categories")
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Retrieved {len(categories)} categories")
            for category in categories:
                print(f"   {category['name']}: {category['description']} (SLA: {category['sla_hours']}h)")
        else:
            print(f"❌ Failed to get categories: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_priorities():
    """Test getting priority levels"""
    print("\n🚨 Testing Get Priorities...")
    try:
        response = requests.get(f"{BASE_URL}/priorities")
        if response.status_code == 200:
            priorities = response.json()
            print(f"✅ Retrieved {len(priorities)} priority levels")
            for priority in priorities:
                print(f"   {priority['name']}: {priority['description']} (SLA: {priority['sla_hours']}h)")
        else:
            print(f"❌ Failed to get priorities: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_stats():
    """Test getting ticket statistics"""
    print("\n📊 Testing Get Statistics...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Retrieved ticket statistics")
            print(f"   Total Tickets: {stats['total_tickets']}")
            print(f"   Open Tickets: {stats['open_tickets']}")
            print(f"   Resolved Tickets: {stats['resolved_tickets']}")
            print(f"   Critical Tickets: {stats['critical_tickets']}")
            
            print("\n   Tickets by Category:")
            for cat in stats['tickets_by_category']:
                print(f"     {cat['name']}: {cat['count']}")
            
            print("\n   Tickets by Priority:")
            for pri in stats['tickets_by_priority']:
                print(f"     {pri['name']}: {pri['count']}")
        else:
            print(f"❌ Failed to get statistics: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_search_tickets():
    """Test searching tickets"""
    print("\n🔍 Testing Search Tickets...")
    try:
        response = requests.get(f"{BASE_URL}/search?query=login&limit=5")
        if response.status_code == 200:
            search_result = response.json()
            print(f"✅ Search completed")
            print(f"   Query: 'login'")
            print(f"   Total Results: {search_result['total_results']}")
            print(f"   Showing: {len(search_result['results'])} results")
            
            for ticket in search_result['results']:
                print(f"     {ticket['ticket_number']}: {ticket['title']}")
        else:
            print(f"❌ Failed to search tickets: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_dashboard():
    """Test getting dashboard data"""
    print("\n📋 Testing Get Dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            dashboard = response.json()
            print("✅ Dashboard data retrieved")
            print(f"   Stats: {dashboard['stats']['total_tickets']} total tickets")
            print(f"   Recent Tickets: {len(dashboard['recent_tickets'])} shown")
            print(f"   Timestamp: {dashboard['timestamp']}")
        else:
            print(f"❌ Failed to get dashboard: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print("🚀 Ticket Management System - API Test Suite")
    print("=" * 50)
    
    # Check if API is running
    if not test_health_check():
        print("\n❌ API is not running. Please start the server first:")
        print("   cd ticketing_tool")
        print("   python3 main.py")
        return
    
    # Run all tests
    test_get_tickets()
    test_get_ticket_details()
    test_get_categories()
    test_get_priorities()
    test_get_stats()
    test_search_tickets()
    test_dashboard()
    
    # Test ticket creation and update
    new_ticket_id = test_create_ticket()
    test_update_ticket(new_ticket_id)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n📚 API Documentation available at:")
    print(f"   {BASE_URL}/docs")
    print(f"   {BASE_URL}/redoc")

if __name__ == "__main__":
    main()
