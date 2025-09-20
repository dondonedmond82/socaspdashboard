import subprocess

def backup_postgres(db_name, user, host, port, backup_file):
    """
    Backup PostgreSQL database to a file using pg_dump.

    Args:
        db_name (str): Database name to backup
        user (str): DB user
        host (str): DB host address
        port (int): DB port number
        backup_file (str): Path to output backup file (e.g., backup.sql or backup.backup)
    """
    try:
        # Command to dump DB as plain SQL text
        cmd = [
            "pg_dump",
            "-h", host,
            "-p", str(port),
            "-U", user,
            "-F", "c",  # custom format for pg_restore, or 'p' for plain SQL
            "-b",       # include blobs
            "-f", backup_file,
            db_name
        ]

        # Run pg_dump, pass environment variable PGPASSWORD if needed
        subprocess.run(cmd, check=True, env={"PGPASSWORD": "your_password_here"})
        print(f"Backup successful: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")

# Example usage:
# backup_postgres("mydatabase",_
