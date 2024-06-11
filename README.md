# Chat Application

Welcome to our Flask-based chat application! This application allows users to register, create groups, send messages in real-time, and more.

## Features

- **User Registration and Login**: Users can create accounts and log in securely.
- **Group Creation and Management**: Users can create groups, add members, and manage group settings.
- **Real-time Messaging**: The application uses WebSockets for real-time communication, enabling instant messaging between users within a group.
- **Profile Management**: Users can update their profile information, such as username, email, and phone number.
- **Authentication**: Token-based authentication ensures secure access to the application's features.
- **Responsive Design**: The application interface is designed to work seamlessly across various devices, including desktops, tablets, and smartphones.

## Installation

To run the application locally, follow these steps:

1. **Clone the Repository**: Clone this GitHub repository to your local machine using the following command:
   ```
   git clone https://github.com/yourusername/chat-application.git
   ```

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies using pip:
   ```
   cd chat-application
   pip install -r requirements.txt
   ```

3. **Run the Flask Application**: Start the Flask server by running the following command:
   ```
   python app.py
   ```

4. **Access the Application**: Once the server is running, access the application in your web browser at [http://localhost:5000/](http://localhost:5000/).

## Usage

1. **User Registration**: New users can register for an account by providing their username, email, phone number, and password.
2. **Login**: Existing users can log in using their credentials.
3. **Create Groups**: Logged-in users can create new groups, specifying the group name and adding members.
4. **Send Messages**: Users can send messages within a group in real-time. Messages are displayed instantly to all group members.
5. **Manage Profile**: Users can update their profile information, including username, email, and phone number.
6. **Edit Groups**: Group creators/administrators can edit group details, such as the group name and members.
7. **Logout**: Users can log out of their accounts to securely end their session.

## Contributing

We welcome contributions from the community to improve and enhance the application. If you'd like to contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure that the code follows the project's style and conventions.
4. Write tests to cover your changes if applicable.
5. Submit a pull request with a clear description of your changes.

## Support

If you encounter any issues or have questions about the application, please feel free to [open an issue](https://github.com/yourusername/chat-application/issues). We'll do our best to assist you.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.