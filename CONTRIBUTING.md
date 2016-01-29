# How to Contribute to this Project



## Basic Structure of the Repository

If you are an admin or interested in the project, please be aware of the structure of branches of this project:

- **`master`**: the last stable version of the bot. No changes are added to this branch until they have been properly tested.
- **`dev`**: version in which we work adding new features. It is mainly used to do tests.
- **`feature/name-of-the-feature`**: to develop each feature independently. This branch must always be merged with `dev`.
- **`hotfix/name-of-the-hotfix`**: to fix small errors. This branch must always be merged with `dev`.



## How to Contribute

If you want to contribute to this project, please follow these rules:

1. Before start working, **check the repository issues**. Maybe someone is already working on it. If not, **create a new issue**. Expose your ideas or your requests, and wait for a moderator to inform you about it.
   
2. If an admin has given you green light to a new feature, **fork this repository** to your own account and perform the changes in there. 
   
3. Once you develop and test your code, you can ask for a **pull request**. Pull requests would only be accepted if:
   
   - The name of the new function is representative and is not used before.
     
   - The code does **not use tab characters**. Please use 4 spaces instead.
     
   - The new function contains a multi-line comment (using Python's `"""`) right after the definition of the function, with: 
     
     - A short description of the function. 
     - A new line that contains: `hand: command` if it is a command function (using `/`) or `hand: message` if it is a message reader.
     
     ​