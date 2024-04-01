## MongoDB

1. (recommended) Install `MongoDB for VS Code` extension
2. Start MongoDB server
3. Import each csv file from `mongo/data-files` into a separate collection using the command:
   ```
   mongoimport --db db-name  --collection collection-name --type csv --file file-name.csv --headerline
   ```
