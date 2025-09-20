# Load SQL Server module
Import-Module SqlServer

# Parameters - customize these for your environment
$agName = "MyAG"
$databaseName = "MyDatabase"
$primaryNode = "SQLNode1.domain.com"
$secondaryNodes = @("SQLNode2.domain.com")
$endpointPort = 5022
$listenerName = "MyAGListener"
$listenerIP = "10.0.0.100"
$subnetMask = "255.255.255.0"

# Backup path for database
$backupPath = "C:\AGBackup\"

# Create backup folder if it doesn't exist
if (!(Test-Path -Path $backupPath)) {
    New-Item -ItemType Directory -Path $backupPath
}

# Function to run a SQL command
function Invoke-Sql($server, $query) {
    Invoke-Sqlcmd -ServerInstance $server -Query $query
}

# Step 1: Backup the database on primary node
$fullBackup = "$backupPath$databaseName-full.bak"
$logBackup = "$backupPath$databaseName-log.bak"

Write-Host "Backing up database on primary node..."
Invoke-Sql $primaryNode "BACKUP DATABASE [$databaseName] TO DISK = N'$fullBackup' WITH INIT"
Invoke-Sql $primaryNode "BACKUP LOG [$databaseName] TO DISK = N'$logBackup' WITH INIT"

# Step 2: Restore backup on secondary nodes with NORECOVERY
foreach ($node in $secondaryNodes) {
    Write-Host "Copying backups to $node and restoring..."
    # You need to copy the backup files to the secondary node manually or with a script like robocopy
    # For simplicity, assume backups are accessible from the secondary nodes at the same path

    Invoke-Sql $node "RESTORE DATABASE [$databaseName] FROM DISK = N'$fullBackup' WITH NORECOVERY, REPLACE"
    Invoke-Sql $node "RESTORE LOG [$databaseName] FROM DISK = N'$logBackup' WITH NORECOVERY"
}

# Step 3: Create the Availability Group on primary node
$replicaString = @()
$replicaString += "N'$primaryNode' WITH (ENDPOINT_URL = N'TCP://$primaryNode:$endpointPort', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = AUTOMATIC, SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY))"
foreach ($node in $secondaryNodes) {
    $replicaString += "N'$node' WITH (ENDPOINT_URL = N'TCP://$node:$endpointPort', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = AUTOMATIC, SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY))"
}
$replicaSql = $replicaString -join ",`n    "

$createAGQuery = @"
CREATE AVAILABILITY GROUP [$agName]
WITH (CLUSTER_TYPE = WSFC)
FOR DATABASE [$databaseName]
REPLICA ON
    $replicaSql
"@

Write-Host "Creating Availability Group..."
Invoke-Sql $primaryNode $createAGQuery

# Step 4: Join secondary replicas
foreach ($node in $secondaryNodes) {
    Write-Host "Joining Availability Group on $node..."
    Invoke-Sql $node "ALTER AVAILABILITY GROUP [$agName] JOIN"
}

# Step 5: Start data synchronization on primary node
Write-Host "Starting data synchronization on primary node..."
Invoke-Sql $primaryNode "ALTER DATABASE [$databaseName] SET HADR AVAILABILITY GROUP = [$agName]"

# Step 6: Create the Availability Group Listener
$createListenerQuery = @"
ALTER AVAILABILITY GROUP [$agName]
ADD LISTENER N'$listenerName'
(
    WITH IP = (('$listenerIP', '$subnetMask')),
    PORT = 1433
);
"@

Write-Host "Creating Availability Group Listener..."
Invoke-Sql $primaryNode $createListenerQuery

Write-Host "Always On Availability Group setup completed successfully."
