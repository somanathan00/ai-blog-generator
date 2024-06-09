# AI Blog Generator

AI Blog Generator is a Django web application that generates blog articles from YouTube video transcriptions. This application uses OpenAI's GPT model for blog content generation and AssemblyAI for audio transcription.

## Features

- User Authentication (Sign Up, Log In, Log Out)
- YouTube video transcription using AssemblyAI
- Blog content generation from transcriptions using OpenAI
- List and view generated blog articles

## Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

- Python 3.6 or later
- Django 3.2 or later
- Node.js (for managing frontend assets, optional)

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ai-blog-generator.git
    cd ai-blog-generator
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project root and add the following variables:

    ```plaintext
    SECRET_KEY=your_django_secret_key
    DEBUG=True  # Set to False in production
    ALLOWED_HOSTS=localhost,127.0.0.1
    OPENAI_API_KEY=your_openai_api_key
    ASSEMBLYAI_API_KEY=your_assemblyai_api_key
    ```

5. **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Collect static files:**

    ```bash
    python manage.py collectstatic
    ```

8. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    Open your browser and navigate to `http://127.0.0.1:8000` to see the application running.

## Usage

1. **Sign Up or Log In:**
    - Create a new account or log in with existing credentials.

2. **Generate a Blog:**
    - Enter a YouTube video link to generate a blog article from its transcription.

3. **View Generated Blogs:**
    - Navigate to the "All Blogs" section to view all your generated blog articles.




## Technologies Used

- Django
- OpenAI GPT-3.5
- AssemblyAI
- Pytube
- Tailwind CSS (for styling)

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request



## Acknowledgments

- [OpenAI](https://www.openai.com/)
- [AssemblyAI](https://www.assemblyai.com/)
- [Django](https://www.djangoproject.com/)
- [Pytube](https://pytube.io/)

