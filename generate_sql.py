import os
import sys
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
from Jarvis.database.models import Base, User, Chat

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def generate_ddl():
    ddl_statements = []
    for table in Base.metadata.sorted_tables:
        ddl_statements.append(str(CreateTable(table).compile(dialect=postgresql.dialect())))
    return "\n\n".join(ddl_statements)

if __name__ == "__main__":
    sql_ddl = generate_ddl()
    print(sql_ddl)
