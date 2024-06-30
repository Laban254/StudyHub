# StudyHub

StudyHub is a Django-powered platform designed to streamline study tasks. It offers note-taking, task management, and homework tracking features. Integrated with Google Books and a dictionary API, StudyHub enhances productivity with a user-friendly interface and dynamic calendar view, ensuring efficient study management.

## Features

- **User Registration and Authentication**: Secure registration and login system.
- **Notes Management**: Create, edit, delete, and share notes. Mark notes as favorites.
- **Task Management**: Create, update, and delete tasks. Track progress and manage deadlines.
- **Homework Tracking**: Add, edit, and delete homework assignments. View deadlines in a calendar view.
- **Google Books Integration**: Search for books and view details from Google Books API.
- **Dictionary Integration**: Look up word definitions using a dictionary API.
- **Dynamic Calendar View**: Visualize homework deadlines and other important dates.

## Installation

### Prerequisites

- Python 3.10
- Docker

### Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/StudyHub.git
   cd StudyHub` 

2.  Create a `.env` file based on the provided `.env.example` and update it with your configuration:
    
    
    `cp .env.example .env` 
    
3.  Build and run the Docker container:
    
    
    `docker build -t studyhub .
    docker run -p 80:8080 studyhub` 
    
4.  The application should now be accessible at `http://localhost`.
## Usage

### Registration

-   Visit `/register` to create a new account.

### Notes

-   Access the notes management interface at `/notes` to create, edit, delete, and share notes.

### Tasks

-   Visit `/tasks` to manage your tasks, including creating, updating, and deleting tasks.

### Homework

-   Track and manage your homework assignments at `/homework`.

### Books

-   Use the book search feature at `/books` to find books via the Google Books API.

### Dictionary

-   Look up word definitions at `/dictionary` using the integrated dictionary API.

## Contributing

If you want to contribute to this project, please create a fork, make your changes, and submit a pull request. We welcome all contributions!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

If you have any questions or feedback, please feel free to reach out at labanrotich6544@gmail.com.


 `Feel free to adjust any sections to better fit your project's specifics.`
