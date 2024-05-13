# Coding Rules

## Git

- Copy the executable files in `git-hooks/` in your git folder: `<project directory>/.git/hooks`.
- New branch name should use prefix: `features/`, `tests/`, `bugfix/`, `hotfix/`, `release/` and `refactor/` e.g. `git branch features/edit-profile`
- Comment concisely and descriptively when commit.
- Follow the workflow when developing a new function: 

0. Checkout the new branch `git checkout -b <branch-name>`.
1. Make changes.
2. Stage `git add <modified-files>` and commit `git commit -m "<comment>"` after completing part of your function.
3. Push to remote repository `git push origin <branch-name>`.
4. Continue developing your function iteratively, repeating steps 2-4 as needed until your feature is complete. Remember to pull changes from the remote repository periodically to incorporate updates from other developers: `git pull origin <target-branch>`

- Follow the workflow before creating pull request:

0. Checkout to master branch and confirm the branch is up-to-date by `git pull`.
1. If you have few commits behind `master` branch, rebase using `git rebase -i master`.
2. If necessary, resolve the conflicts manually or using merge tools and then commit all changes **EXCEPT** migration file.
3. Check if there is any new migrations in master. If so, execute `flask db upgrade`.
4. If you've made modifications on `models.py` e.g. create a table, add columns etc. If so, delete your migration directly and use `flask db migrate -m "<comment>"` to generate newly indexed migration. After that, commit and push your migration to remote repository.
5. (Optional) Squash Commits: If you've made multiple commits, consider squashing them into a single commit before merging.
6. Review your changes and make sure the app works properly.
7. Create pull request. 

## Front-End

### HTML

- Use semantic HTML tags to improve accessibility and SEO.
- Indent HTML code with **2** spaces.
- Use double quotes for attribute values.
- Avoid inline styles and scripts.
- Comment your code to improve readability i.e. `<!-- Comment -->`.

### CSS

- Use meaningful class and ID names.
- Organize CSS properties alphabetically.
- Use shorthand properties when possible.
- Avoid using !important.
- Comment your code to explain complex styles i.e. `/* Comment */`.

### JavaScript

- Use **camelCase** for variable and function names.
- Declare variables with `const` or `let` instead of `var`.
- Use strict equality (`===`) for comparisons.
- Avoid global variables and functions.
- Comment your code to explain complex logic: 
```
// For inline description
```
```
/**
 * For multiline description
 */
```
```
/**
 * For functions description
 * @param {*} paramName description
 */
```

### Bootstrap

- Follow Bootstrap's documentation and guidelines.
- Use Bootstrap's grid system for responsive layouts.
- Customize Bootstrap's styles using custom CSS.

### jQuery

- Use jQuery's API documentation for reference.
- Cache jQuery selectors for better performance.
- Use event delegation for dynamically added elements.
- Avoid unnecessary DOM manipulation.
- Comment your code to explain jQuery usage.

### General

- Use version control (e.g., Git) to track changes.
- Write clean and readable code.
- Follow the DRY (Don't Repeat Yourself) principle.
- Test your code in different browsers and devices.
- Stay up to date with the latest web development trends and best practices.

## Back-End

### Python

- Use meaningful variable and function names.
- Follow PEP 8 style guide for code formatting. (Indent python code with **4** spaces)
- Use docstrings to document functions and classes.
- Avoid using global variables.
- Comment your code to explain complex logic or algorithms.

### Flask

- Follow Flask's documentation and best practices.
- Use Flask's routing system for defining routes.
- Use Flask's templates for rendering dynamic HTML.
- Use Flask's request object to handle incoming requests.
- Comment your code to explain Flask-specific functionality.

### SQLite

- Use **snake_case** naming method for tables and columns.
- Use appropriate data types for columns.
- Use indexes for frequently queried columns.
- Use transactions for atomicity and data integrity.
- Comment your code to explain SQL queries and database operations.

### Migrations

- Do NOT upload your local database file `.db`.
- **Always** check if there are new migrations on Git before you commit a migration.
- Follow the migrate-upgrade workflow with command `flask db migrate -m "comment"` then `flask db upgrade` after checking.
- Make **meaningful** comment when you migrate, e.g. `flask db migrate -m "add user table"`.
- Commit your migratio lastly, i.e. right before you are about to make a pull request, in order to avoid version conflict.


### General

- If new libraries/extensions are added, update `requirements.txt` by using `pip freeze > requirements.txt` command.
- Use version control (e.g., Git) to track changes.
- Write clean and readable code.
- Follow the DRY (Don't Repeat Yourself) principle.
- Test your code with unit tests and integration tests.
- Stay up to date with the latest web development trends and best practices.