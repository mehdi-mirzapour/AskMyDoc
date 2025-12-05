#!/usr/bin/env python3
"""Test script to verify Langfuse configuration"""

from app.core.config import get_settings
from langfuse.callback import CallbackHandler as LangfuseHandler

def test_langfuse_config():
    """Test if Langfuse environment variables are loaded correctly"""
    settings = get_settings()
    
    print("=" * 60)
    print("Langfuse Configuration Test")
    print("=" * 60)
    
    # Check environment variables
    print(f"\n✓ Langfuse Public Key: {settings.langfuse_public_key[:15]}..." if len(settings.langfuse_public_key) > 15 else settings.langfuse_public_key)
    print(f"✓ Langfuse Secret Key: {settings.langfuse_secret_key[:15]}..." if len(settings.langfuse_secret_key) > 15 else settings.langfuse_secret_key)
    print(f"✓ Langfuse Host: {settings.langfuse_host}")
    
    # Validate values are not defaults
    if settings.langfuse_public_key == "XXXX":
        print("\n❌ WARNING: Langfuse public key is still set to default 'XXXX'")
        print("   Make sure LANGFUSE_PUBLIC_KEY is set in .env file")
        return False
    
    if settings.langfuse_secret_key == "XXXX":
        print("\n❌ WARNING: Langfuse secret key is still set to default 'XXXX'")
        print("   Make sure LANGFUSE_SECRET_KEY is set in .env file")
        return False
    
    # Try to initialize Langfuse handler
    print("\n" + "=" * 60)
    print("Testing Langfuse Handler Initialization")
    print("=" * 60)
    
    try:
        handler = LangfuseHandler(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host
        )
        print("\n✓ Langfuse handler initialized successfully!")
        print("✓ Integration is working correctly")
        return True
    except Exception as e:
        print(f"\n❌ Error initializing Langfuse handler: {e}")
        return False

if __name__ == "__main__":
    success = test_langfuse_config()
    exit(0 if success else 1)
