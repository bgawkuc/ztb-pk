# MongoDB

1. (recommended) Install `MongoDB for VS Code` extension
2. Start MongoDB server
3. Import each csv file from `mongo/data-files` into a separate collection using the command:
   ```
   mongoimport --db db_name  --collection collection_name --type csv --file file_name.csv --headerline
   ```
