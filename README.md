## Introduction
Fluky is a real-time chat application built using Django, HTML, CSS, and JavaScript. It enables instant messaging between users, providing a fast and efficient communication experience with modern web technologies.


### Screenshots

![Register Screen](screenshots/resiter_page.png)
![Profile section](screenshots/profile.png)
![Chats section](screenshots/my_chats.png)
![Random chat section](screenshots/random_chat.png)


### Setup Steps

1. **Clone the Repository**:

    Open your terminal or command prompt and run the following command to clone the repository from GitHub:

    ```bash
    git clone https://github.com/ismailerd1/Fluky.git
    cd news-website
    ```

2. **Create and Activate a Virtual Environment**:
   
    - For macOS/Linux:

      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - For Windows:

      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

3. **Install Required Packages**:

    ```bash
    pip install -r requirements.txt
    ```
4. **Apply Database Migrations**:

   ```bash
    python manage.py migrate
    ```
5. **Start the development server**:
   
   ```bash
    python manage.py runserver
    ```

6. **Open the Application in Your Browser**:

  Go to http://127.0.0.1:8000 in your browser and start exploring Fluky!


## Contributing
If you would like to contribute, please submit a pull request or open an issue. I welcome all feedback!


## License
This project is licensed under the MIT License. For more information, see the LICENSE file.

### CONTACT
If you have any questions or need assistance, please feel free to reach out.
my e-mail: ismailerdogan2003@gmail.com
