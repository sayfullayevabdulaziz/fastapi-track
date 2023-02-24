# Backup your databases
```docker exec -t db-track pg_dumpall -c -U postgres > dump_`db-track`.sql```

# Restore your databases ( is not working )
```cat dump_db-track.sql | docker exec -i db-track psql -U postgres```

# Run the project using Docker containers and forcing build containers

```docker compose -f docker-compose.yml up --build```


https://stackoverflow.com/questions/24718706/backup-restore-a-dockerized-postgresql-database
