#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discuss.settings')
django.setup()

from django.db import connection

def reset_sequences():
    """Reset all PostgreSQL sequences based on the max ID values in each table"""
    print("Resetting PostgreSQL sequences...")
    with connection.cursor() as cursor:
        # Get a list of all tables with their ID sequences
        cursor.execute("""
            SELECT 
                table_name, 
                column_name,
                pg_get_serial_sequence(quote_ident(table_name), column_name) as sequence_name
            FROM 
                information_schema.columns
            WHERE 
                column_name = 'id' AND 
                table_schema = 'public'
            ORDER BY 
                table_name
        """)
        sequences = cursor.fetchall()
        
        # Reset each sequence based on the max ID in its table
        for table_name, column_name, sequence_name in sequences:
            if sequence_name:
                print(f"Resetting sequence for {table_name}.{column_name}...")
                # Get the max ID value
                cursor.execute(f"SELECT COALESCE(MAX({column_name}), 0) + 1 FROM {table_name}")
                next_id = cursor.fetchone()[0]
                
                # Reset the sequence
                cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH {next_id}")
                print(f"  -> Sequence reset to {next_id}")

if __name__ == "__main__":
    reset_sequences()
    print("All sequences have been reset successfully!")