#!/usr/bin/env python3
"""
Test script to verify sync functionality works correctly
"""
import requests
import time
import json
import sys

def test_sync_endpoint():
    """Test the sync endpoint and monitor progress"""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Jira Sync Endpoint...")
    print("=" * 50)
    
    # Step 1: Trigger sync
    print("1. Triggering sync operation...")
    try:
        response = requests.post(f"{base_url}/sync")
        if response.status_code != 200:
            print(f"❌ Failed to trigger sync: {response.status_code} - {response.text}")
            return False
        
        data = response.json()
        operation_id = data.get('operation_id')
        if not operation_id:
            print(f"❌ No operation_id returned: {data}")
            return False
            
        print(f"✅ Sync triggered successfully, operation_id: {operation_id}")
        
    except Exception as e:
        print(f"❌ Error triggering sync: {e}")
        return False
    
    # Step 2: Monitor progress
    print(f"\n2. Monitoring progress for operation {operation_id}...")
    completed = False
    max_attempts = 60  # 2 minutes max
    attempt = 0
    
    while not completed and attempt < max_attempts:
        try:
            progress_response = requests.get(f"{base_url}/api/progress/{operation_id}")
            if progress_response.status_code == 200:
                progress_data = progress_response.json()
                status = progress_data.get('status', 'unknown')
                percentage = progress_data.get('percentage', 0)
                message = progress_data.get('status_message', 'No message')
                
                print(f"   Progress: {percentage}% - {status} - {message}")
                
                if status in ['completed', 'failed']:
                    completed = True
                    if status == 'completed':
                        results = progress_data.get('results', {})
                        synced_count = results.get('synced_tickets', 0)
                        print(f"✅ Sync completed successfully! Synced {synced_count} tickets")
                        return True
                    else:
                        print(f"❌ Sync failed: {message}")
                        return False
            else:
                print(f"⚠️  Progress check failed: {progress_response.status_code}")
                
        except Exception as e:
            print(f"⚠️  Error checking progress: {e}")
        
        attempt += 1
        time.sleep(2)
    
    if not completed:
        print(f"❌ Sync did not complete within {max_attempts * 2} seconds")
        return False
    
    return True

def test_ticket_data():
    """Test that ticket data is properly updated"""
    base_url = "http://localhost:5001"
    
    print("\n3. Verifying ticket data...")
    try:
        response = requests.get(f"{base_url}/api/tickets")
        if response.status_code != 200:
            print(f"❌ Failed to fetch tickets: {response.status_code}")
            return False
        
        tickets = response.json()
        if isinstance(tickets, dict) and 'error' in tickets:
            print(f"❌ Error fetching tickets: {tickets['error']}")
            return False
        
        print(f"✅ Retrieved {len(tickets)} tickets from API")
        
        # Check for some basic ticket properties
        if tickets:
            sample_ticket = tickets[0]
            required_fields = ['key', 'summary', 'status', 'issue_type', 'updated']
            missing_fields = [field for field in required_fields if field not in sample_ticket]
            
            if missing_fields:
                print(f"⚠️  Sample ticket missing fields: {missing_fields}")
            else:
                print(f"✅ Sample ticket ({sample_ticket['key']}) has all required fields")
                print(f"   Status: {sample_ticket['status']}")
                print(f"   Type: {sample_ticket['issue_type']}")
                print(f"   Updated: {sample_ticket['updated']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking ticket data: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Jira Sync Integration Tests")
    print("Make sure the Flask app is running on localhost:5001")
    print("Press Enter to continue or Ctrl+C to cancel...")
    try:
        input()
    except KeyboardInterrupt:
        print("\nTest cancelled.")
        return
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Sync endpoint
    if test_sync_endpoint():
        tests_passed += 1
    
    # Test 2: Ticket data
    if test_ticket_data():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Sync functionality is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()