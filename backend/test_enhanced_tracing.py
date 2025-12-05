#!/usr/bin/env python3
"""Test script to verify enhanced Langfuse tracing with the document agent"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.document_agent import DocumentAgent
from app.core.logger import logger
import time

def test_enhanced_tracing():
    """Test that enhanced Langfuse tracing captures agent workflow"""
    
    print("=" * 70)
    print("Enhanced Langfuse Tracing Test")
    print("=" * 70)
    
    # Initialize agent
    print("\n1. Initializing DocumentAgent...")
    agent = DocumentAgent()
    
    if not agent.langfuse_client:
        print("❌ Langfuse client not initialized. Cannot test tracing.")
        return False
    
    print("✓ Agent initialized with Langfuse client")
    
    # Test query
    test_question = "What is 2 + 2?"  # Simple question that won't require tools
    print(f"\n2. Testing with question: '{test_question}'")
    
    try:
        result = agent.query(test_question)
        print(f"✓ Query completed successfully")
        print(f"   Answer: {result['answer'][:100]}...")
        
        # Give Langfuse time to flush
        print("\n3. Waiting for Langfuse to flush traces...")
        time.sleep(2)
        
        print("\n" + "=" * 70)
        print("✅ Test completed successfully!")
        print("=" * 70)
        print("\nNow check the Langfuse UI at http://localhost:3000")
        print("You should see a trace with:")
        print("  ├── agent_query (main trace)")
        print("  │   ├── graph_execution (span)")
        print("  │   │   ├── agent_reasoning (span)")
        print("  │   │   │   └── LLM call (via callback)")
        print("  │   └── metadata (model, status, etc.)")
        print("\nIf tools were called, you would also see:")
        print("  │   │   ├── tools_execution (span)")
        print("  │   │   │   └── tool_<name> (span for each tool)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during query: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enhanced_tracing()
    sys.exit(0 if success else 1)
