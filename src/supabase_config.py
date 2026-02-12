"""
VORTEX Supabase Configuration
Real database connection with Anon Key
"""
import os
from supabase import create_client, Client
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class VortexSupabase:
    """Supabase client for VORTEX real database"""
    
    def __init__(self):
        self.url = "https://ofoylamviehwpeukmdei.supabase.co"
        self.anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9mb3lsYW12aWVod3BldWttZGVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA4NjAyNjQsImV4cCI6MjA4NjQzNjI2NH0.Bo5cKKKxW2Qfe_XmEUHmX2Ur5N7jMnNyR-FHUqX7ArE"
        self.client: Optional[Client] = None
        
    def connect(self) -> Client:
        """Establish connection to Supabase"""
        try:
            self.client = create_client(self.url, self.anon_key)
            logger.info("✅ Connected to VORTEX Supabase database")
            return self.client
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            raise
    
    def get_client(self) -> Client:
        """Get or create Supabase client"""
        if not self.client:
            self.connect()
        return self.client

# Singleton instance
vortex_db = VortexSupabase()
