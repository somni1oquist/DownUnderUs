# Coding Rules

## Git

- Copy the executable files in `git-hooks/` in you git folder `<project>/.git/hooks`.
- New branch should use prefix: `features/`, `tests/`, `bugfix/`, `hotfix/`, `release/`.
- Comment concisely and descriptively when commit.

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


### General

- Use version control (e.g., Git) to track changes.
- Write clean and readable code.
- Follow the DRY (Don't Repeat Yourself) principle.
- Test your code with unit tests and integration tests.
- Stay up to date with the latest web development trends and best practices.