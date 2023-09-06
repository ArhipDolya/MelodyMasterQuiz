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

