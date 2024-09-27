# Social Media API

### Overview
This Social Media API allows users to register, log in, create posts, like posts, and comment on them. 
JWT authentication is used to manage user sessions, and the API supports file uploads (e.g., images) for posts. 
Additionally, users can log out by blacklisting their JWT tokens.

Live: https://social-media-api-e19j.onrender.com/swagger

### Features
* User Registration & Authentication:

  * Create an account and log in to receive a JWT token.
  * Sessions are managed using JWT, allowing for multiple logins.
* Post Creation:

  * Users can create text posts, or posts that include media files (images).
* Like & Comment on Posts:

  * Users can like and comment on posts, with the ability to view the total number of likes and comments for each post.
* Logout:

  * Users can log out by blacklisting their JWT token.
 
### Endpoints
### User Authentication
  1. Register a User
  * URL: /register
  * Method: POST
  * Description: Create a new user account.
  * Request Body:

  ``` json
     {
        "username": "your_username",
        "password": "your_password",
        "email": "your_email"
     }
  ```
  * Response:
    * Success: 201 Created
    * Error: 400 Bad Request, 500 Internal Server Error
   
  2. Login
  * URL: /login
  * Method: POST
  * Description: Authenticate a user and receive a JWT token.
  * Request Body:

    ``` json
     {
        "username": "your_username",
        "email": "your_email"
     }
    ```
  * Response:
    * Success: 200 OK with JWT token.
    * Error: 401 Unauthorized, 500 Internal Server Error
### Post Management

  3. Create a Post
  * URL: /posts
  * Method: POST
  * Description: Create a new post (text and/or file upload).
  * Authorization: Requires JWT Token.
  * Request Body (Multipart/form-data for file upload):
    * text: Post content (optional if file is provided)
    * file: Image/Video file (optional if text is provided)
   
  * Response:
    * Success: 201 Created
    * Error: 400 Bad Request, 401 Unauthorized, 500 Internal Server Error
   
  4. Get All Posts
  * URL: /posts
  * Method: GET
  * Description: Retrieve all posts.
  * Authorization: Requires JWT Token.
  
  * Response:
    * Success: 200 OK with list of posts.
    * Error: 204 No Content, 401 Unauthorized, 500 Internal Server Error
   
### Like & Comment Management
  5. Like a Post
  * URL: /posts/<int:pid>/like
  * Method: POST
  * Description: Like a specific post.
  * Authorization: Requires JWT Token.

  * Response:
    * Success: 201 Created (liked successfully)
    * Error: 401 Unauthorized, 500 Internal Server Error
  
  6. Get Post Likes
  * URL: /posts/<int:pid>/like
  * Method: GET
  * Description: Get the total number of likes for a post.
  * Authorization: Requires JWT Token.
 
  * Response:
    * Success: 200 OK with like count.
    * Error: 204 No Content, 401 Unauthorized, 500 Internal Server Error
   
  7. Comment on a Post
  * URL: /posts/<int:pid>/comment
  * Method: POST
  * Description: Add a comment to a post.
  * Authorization: Requires JWT Token.
 
  * Request Body:
    ``` json
     {
        "content_": "your_comment"
     }
    ```
  * Response:
    * Success: 201 Created
    * Error: 401 Unauthorized, 500 Internal Server Error
   
  8. Get Post Comments
  * URL: /posts/<int:pid>/comment
  * Method: GET
  * Description: Get all comments on a specific post.
  * Authorization: Requires JWT Token.
  
  * Response:
    * Success: 200 OK with list of comments.
    * Error: 204 No Content, 401 Unauthorized, 500 Internal Server Error
   
  ### Logout
  9. Logout User
  * URL: /logout
  * Method: POST
  * Description: Logout a user by blacklisting their JWT token.
  * Authorization: Requires JWT Token.
 
  * Response:
    * Success: 200 OK (successfully logged out)
    * Error: 500 Internal Server Error
## Setup and Installation
### Prerequisites
  * Python 3.x
  * Flask
  * SQLAlchemy
  * Flask-JWT-Extended
  * Marshmallow
  * PostgreSQL (or any other database supported by SQLAlchemy)

### Installation
  1. Clone the repository:

  ``` bash
       git clone https://github.com/8adiq/social-media-api/
       cd social-media-api

  ```
  2. Set up a virtual environment and activate it:
   ``` bash
       python3 -m venv venv
       source venv/bin/activate
  ```
  3. Install the required dependencies:
  ``` bash
       pip install -r requirements.txt
  ```
  4. Set up the PostgreSQL database and configure your database URI in the app's configuration.
  5. Run database migrations (if applicable):
   ``` bash
       flask db init
       flask db migrate
       flask db upgrade
  ```
  6. Run the app:
  ``` bash
       cd app
       flask run
  ```
### Authentication
This API uses JWT (JSON Web Tokens) for authentication. Users must log in to receive a token, which 
should be included in the Authorization header of each request to protected routes, as follows:
``` bash
       Authorization: Bearer <your-jwt-token>
  ```
### Error Handling
  * 400 Bad Request: Input validation errors or missing data.
  * 401 Unauthorized: Authentication errors or missing JWT token.
  * 500 Internal Server Error: General server or database errors.


