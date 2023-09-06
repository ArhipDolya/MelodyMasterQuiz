# Django Spotify API Integration

This Django application connects effortlessly with the Spotify API, offering an immersive music experience. With this web app you can discover new information about your favorite songs or play QuizGame.

## Installation

Follow these steps to set up and run the Django application locally:

1. Clone the repository to your local machine: 
git clone https://github.com/yourusername/your-repo.git


2. Navigate to the project directory:
cd your-repo

3. Create a virtual environment:
python -m venv venv

4. Activate the virtual environment:
On Windows:
    venv\Scripts\activate
On macOS and Linux:
    source venv/bin/activate

5. Install project dependencies:
    pip install -r requirements.txt


## Configuration
Before running the application, you need to configure it to work with the Spotify API. Follow these steps:

1. Create a Spotify Developer account and register your application.

2. Obtain your Spotify API credentials (Client ID and Client Secret).

3. Set up environment variables for your credentials. Create a .env file in the project directory and add the following lines:
    SPOTIFY_CLIENT_ID=your-client-id
    SPOTIFY_CLIENT_SECRET=your-client-secret

## USAGE

To run the Django application, use the following commands:
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

Once the server is running, open your web browser and go to http://localhost:8000 to access the application.

## Contributing
We welcome contributions from the community. To contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    git checkout -b feature/your-feature
3. Make your changes and commit them:
    git commit -m "Add your commit message here"
4. Push your changes to your fork:
    git push origin feature/your-feature
5. Create a pull request on the main repository.
6. Wait for your pull request to be reviewed and merged.    

## Contact Information
If you have questions or need assistance, you can reach out to us at arhipdolya6995@gmail.com.
