# Dojo Assignment: Coding Dojo Wall
Learning Objectives:
- Connect a Flask application to a MySQL database.
- Create login and registration within an app.
- Handle a one-to-many relationship that involves users.
- Manipulate and filter data using user ids

Tables & Columns:
- users
    - id
    - first_name
    - last_name
    - email
    - password
    - created_at
    - updated_at
- posts
    - id
    - content
    - created_at
    - updated_at
    - users_id
- comments
    - id
    - comment
    - created_at
    - updated_at
    - posts_id
    - users_id

Routes:
- Visible
    - /
    - /wall
- Hidden
    - /register POST
    - /login POST
    - /publish POST
    - /delete/int:id
    - /logout

Fully functional login and registration with validation
Posts are validated
Comments are validated

User, Post, and Comment classes all get linked appropriately