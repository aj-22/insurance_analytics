create database insurance_sim;
GO

CREATE LOGIN is_dba WITH PASSWORD = 'dba@123'
GO

Use insurance_sim;
GO

IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = N'is_dba')
BEGIN
    CREATE USER is_dba FOR LOGIN is_dba
    EXEC sp_addrolemember N'db_owner', N'is_dba'
END;
GO
