
   # Working with GIT - Clonning, Branching, Commiting
   Do once:

   ```bash
   ssh-keygen -t rsa -b 4096 -C "giladshkalim@gmail.com"
   cat ~/.ssh/id_rsa.pub
   # Copy string to GitHub > Setting > SSH > New SSH Key
   ```
   ```bash
   cd C:\Users\YourUsername\Desktop\YourNewFolder
   git clone <REPOSETOEY_URL>
   ```
   1. **Creating a New Branch**
      ```bash
      # Create and switch to a new branch:
      git checkout -b new-feature-branch
      ```
   
   2. **Making Changes**

      Make your desired changes to the project files.

   4. **Committing Changes**
      ```bash
      # Stage your changes:
      git add .
      ```
      ```bash
      # Commit your changes:
      git commit -m "Add short detail on waht is being commited here"
      ```
   5. **Pushing Changes to the Remote Repository**
   
      ```bash
      git push -u origin new-feature-branch
      ```


      
