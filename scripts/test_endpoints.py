#!/usr/bin/env python3
"""
Test Endpoints Script for APP_BE_MENTANA

This script demonstrates all the test endpoints and their functionality.
Run this script to test the complete API functionality.
"""

import requests
import json
import time
from typing import Dict, Any
import sys


class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def print_section(self, title: str):
        """Print a formatted section header"""
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_result(self, endpoint: str, response: requests.Response, data: Dict[str, Any] = None):
        """Print formatted test result"""
        status_emoji = "✅" if response.status_code < 400 else "❌"
        print(f"{status_emoji} {endpoint}")
        print(f"   Status: {response.status_code}")
        print(f"   Time: {response.elapsed.total_seconds():.3f}s")
        
        if data:
            print(f"   Response: {json.dumps(data, indent=2)}")
        print()
    
    def test_basic_endpoints(self):
        """Test basic application endpoints"""
        self.print_section("Basic Endpoints")
        
        # Test root endpoint
        response = self.session.get(f"{self.base_url}/")
        data = response.json()
        self.print_result("GET /", response, data)
        
        # Test basic health check
        response = self.session.get(f"{self.base_url}/health")
        data = response.json()
        self.print_result("GET /health", response, data)
        
        # Test API health check
        response = self.session.get(f"{self.base_url}/api/v1/health")
        data = response.json()
        self.print_result("GET /api/v1/health", response, data)
        
        # Test readiness check
        response = self.session.get(f"{self.base_url}/api/v1/health/ready")
        data = response.json()
        self.print_result("GET /api/v1/health/ready", response, data)
        
        # Test liveness check
        response = self.session.get(f"{self.base_url}/api/v1/health/live")
        data = response.json()
        self.print_result("GET /api/v1/health/live", response, data)
    
    def test_comprehensive_health_check(self):
        """Test comprehensive health check endpoint"""
        self.print_section("Comprehensive Health Check")
        
        response = self.session.get(f"{self.base_url}/api/v1/test/health")
        data = response.json()
        self.print_result("GET /api/v1/test/health", response, data)
        
        # Analyze health status
        if data.get("status") == "healthy":
            print("🎉 All services are healthy!")
        elif data.get("status") == "degraded":
            print("⚠️  Some services are degraded:")
            for service in data.get("unhealthy_services", []):
                print(f"   - {service}")
        else:
            print("❌ Health check failed")
    
    def test_architecture_demo(self):
        """Test architecture demonstration endpoint"""
        self.print_section("Architecture Demonstration")
        
        response = self.session.get(f"{self.base_url}/api/v1/test/architecture")
        data = response.json()
        self.print_result("GET /api/v1/test/architecture", response, data)
        
        # Display architecture information
        if "architecture" in data:
            arch = data["architecture"]
            print("🏗️  Hexagonal Architecture Components:")
            for layer, info in arch.get("layers", {}).items():
                print(f"   📁 {layer}: {info.get('description', '')}")
                for component in info.get("components", []):
                    print(f"      - {component}")
    
    def test_factories_demo(self):
        """Test factory pattern demonstration endpoint"""
        self.print_section("Factory Pattern Demonstration")
        
        response = self.session.get(f"{self.base_url}/api/v1/test/factories")
        data = response.json()
        self.print_result("GET /api/v1/test/factories", response, data)
        
        # Display factory information
        if "factories" in data:
            factories = data["factories"]
            print("🏭 Factory Pattern Implementation:")
            for factory_name, factory_info in factories.get("factories_implemented", {}).items():
                print(f"   🔧 {factory_name}: {factory_info.get('description', '')}")
                for method in factory_info.get("methods", []):
                    print(f"      - {method}")
    
    def test_user_operations(self):
        """Test user-related operations"""
        self.print_section("User Operations")
        
        # Test user creation
        user_data = {
            "email": f"test-{int(time.time())}@example.com",
            "name": "Test User"
        }
        
        response = self.session.post(f"{self.base_url}/api/v1/users", json=user_data)
        data = response.json()
        self.print_result("POST /api/v1/users", response, data)
        
        if response.status_code == 201 and "id" in data:
            user_id = data["id"]
            
            # Test get user by ID
            response = self.session.get(f"{self.base_url}/api/v1/users/{user_id}")
            data = response.json()
            self.print_result(f"GET /api/v1/users/{user_id}", response, data)
            
            # Test get all users
            response = self.session.get(f"{self.base_url}/api/v1/users")
            data = response.json()
            self.print_result("GET /api/v1/users", response, data)
    
    def test_test_user_creation(self):
        """Test the test user creation endpoint"""
        self.print_section("Test User Creation (Hexagonal Architecture Demo)")
        
        response = self.session.post(f"{self.base_url}/api/v1/test/user")
        data = response.json()
        self.print_result("POST /api/v1/test/user", response, data)
        
        # Display architecture demonstration
        if "architecture_demo" in data:
            print("🏗️  Architecture Demonstration:")
            for layer, description in data["architecture_demo"].items():
                print(f"   📋 {layer}: {description}")
    
    def test_user_retrieval(self):
        """Test the test user retrieval endpoint"""
        self.print_section("Test User Retrieval (Repository Pattern Demo)")
        
        response = self.session.get(f"{self.base_url}/api/v1/test/users")
        data = response.json()
        self.print_result("GET /api/v1/test/users", response, data)
        
        # Display repository demonstration
        if "repository_demo" in data:
            print("🗄️  Repository Pattern Demonstration:")
            for pattern, description in data["repository_demo"].items():
                print(f"   📋 {pattern}: {description}")
    
    def test_s3_operations(self):
        """Test S3 operations endpoint"""
        self.print_section("S3 Operations (AWS Service Demo)")
        
        response = self.session.post(f"{self.base_url}/api/v1/test/s3")
        data = response.json()
        self.print_result("POST /api/v1/test/s3", response, data)
        
        # Display S3 operation details
        if "s3_operations" in data:
            print("☁️  S3 Operations:")
            for operation, value in data["s3_operations"].items():
                print(f"   📁 {operation}: {value}")
        
        # Display service demonstration
        if "service_demo" in data:
            print("🔧 Service Pattern Demonstration:")
            for pattern, description in data["service_demo"].items():
                print(f"   📋 {pattern}: {description}")
    
    def test_performance(self):
        """Test performance monitoring endpoint"""
        self.print_section("Performance Monitoring")
        
        response = self.session.get(f"{self.base_url}/api/v1/test/performance")
        data = response.json()
        self.print_result("GET /api/v1/test/performance", response, data)
        
        # Display performance metrics
        if "metrics" in data:
            print("⚡ Performance Metrics:")
            for metric, value in data["metrics"].items():
                print(f"   📊 {metric}: {value}")
        
        # Display recommendations
        if "recommendations" in data:
            print("💡 Performance Recommendations:")
            for recommendation in data["recommendations"]:
                print(f"   💭 {recommendation}")
    
    def test_cleanup(self):
        """Test cleanup endpoint"""
        self.print_section("Cleanup Operations")
        
        response = self.session.delete(f"{self.base_url}/api/v1/test/cleanup")
        data = response.json()
        self.print_result("DELETE /api/v1/test/cleanup", response, data)
        
        # Display cleanup information
        if "recommendations" in data:
            print("🧹 Cleanup Recommendations:")
            for recommendation in data["recommendations"]:
                print(f"   💭 {recommendation}")
    
    def run_all_tests(self):
        """Run all test endpoints"""
        print("🚀 APP_BE_MENTANA - Complete API Test Suite")
        print("=" * 60)
        print(f"Testing API at: {self.base_url}")
        print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Test basic endpoints
            self.test_basic_endpoints()
            
            # Test comprehensive health check
            self.test_comprehensive_health_check()
            
            # Test architecture demo
            self.test_architecture_demo()
            
            # Test factory pattern demo
            self.test_factories_demo()
            
            # Test user operations
            self.test_user_operations()
            
            # Test hexagonal architecture demo
            self.test_test_user_creation()
            
            # Test repository pattern demo
            self.test_user_retrieval()
            
            # Test S3 operations
            self.test_s3_operations()
            
            # Test performance monitoring
            self.test_performance()
            
            # Test cleanup
            self.test_cleanup()
            
            print("\n" + "=" * 60)
            print("🎉 All tests completed!")
            print("=" * 60)
            
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to the API server.")
            print("Make sure the server is running with: python run.py dev")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            sys.exit(1)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test all API endpoints")
    parser.add_argument(
        "--url", 
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    tester = APITester(args.url)
    tester.run_all_tests()


if __name__ == "__main__":
    main() 