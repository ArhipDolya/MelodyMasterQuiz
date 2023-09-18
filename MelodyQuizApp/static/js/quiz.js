const songPreviewElement = document.getElementById('song-preview');
const songGuessElement = document.getElementById('song-guess');
const submitAnswerButton = document.getElementById('submit-answer');
const startQuizButton = document.getElementById('start-quiz-button');
const questionContainer = document.getElementById('question-container');
const dontKnowButton = document.getElementById('dont-know-button')

let correctSongName;
let countdown = 30;
let timerElement = document.getElementById('timer');


function updateTimerDisplay() {
    timerElement.textContent = countdown
    if (countdown <= 0) {
        skipSong();
    }
}


function startTimer() {
    updateTimerDisplay();
    countdown--;
    if (countdown >= 0) {
        setTimeout(startTimer, 1000);
    }
}


// Inside the startQuizButton event listener
startQuizButton.addEventListener('click', () => {
    const playlistUrl = document.getElementById('playlist_url').value;
    countdown = 30
    updateTimerDisplay()
    
    // Fetch a random song from the playlist
    fetch('/quiz/api/get_random_song/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ playlist_url: playlistUrl }),
    })

    .then(response => response.json())

    .then(data => {
        const songPreviewURL = data.song_preview_url;
        correctSongName = data.correct_song_name;
        
        // Set the audio source and play the song
        songPreviewElement.src = songPreviewURL;
        songPreviewElement.volume = 0.1;
        songPreviewElement.play(); // Start playing the audio
        
        // Show the quiz section
        document.getElementById('quiz-section').style.display = 'block';  
    })

    .catch(error => {
        console.error('Error fetching song:', error);
    });
});


submitAnswerButton.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default form submission

    const userGuess = songGuessElement.value.trim();
    if (userGuess) {
        submitUserGuess(userGuess);
    }
});


function submitUserGuess(guess) {
    // Submit the user's guess
    fetch('/quiz/api/submit_guess/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ guess: guess, correct_song_name: correctSongName }),
    })

    .then(response => response.json())
    .then(data => {
        
        const resultMessageElement = document.getElementById('result-message');
        if (data.message === 'Correct guess!') {
            resultMessageElement.textContent = 'Congratulations! Your guess is correct!';
            resultMessageElement.classList.remove('d-none');
            resultMessageElement.classList.remove('alert-danger'); // Remove red styling if previous answer was incorrect
            resultMessageElement.classList.add('alert-success'); // Add green styling for correct answer
        } else {
            console.log('Incorrect guess!'); // Debugging line
            resultMessageElement.textContent = 'Oops! Your guess is incorrect.';
            resultMessageElement.classList.remove('d-none');
            resultMessageElement.classList.add('alert-danger'); // Add red styling for incorrect answer
        }

        // Clear the guess input
        songGuessElement.value = '';

        // Delay for a few seconds before reloading the form
        setTimeout(() => {
            location.reload();
        }, 3000); // Delay for 3 seconds
    })

    .catch(error => {
        console.error('Error submitting guess:', error);
    });
}


dontKnowButton.addEventListener('click', () => {
    const pointsToSubtract = 10;

    fetch('/quiz/api/subtract_points/', {
        'method': 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({points: pointsToSubtract})
    })

    .then(response => response.json())
    .then(data => {
        console.log(data.message)
        setTimeout(() => {
            location.reload()
        }, 1000)
    })

    .catch(error => {
        console.error('Error subtracting points', error)
    })
})


function skipSong() {
    const timeUpMessage = document.getElementById('time-up-message');
    timeUpMessage.style.display = 'block';
    
    // Pause the song
    songPreviewElement.pause();
    
    // Deduct points
    const pointsToSubtract = 10;

    // If there are points to subtract, do so
    if (pointsToSubtract > 0) {
        // Subtract points
        fetch('/quiz/api/subtract_points/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ points: pointsToSubtract }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error(`Error subtracting points: ${error}`);
        });
    }

    // Reload the form after a delay
    setTimeout(() => {
        location.reload();
    }, 3000); // Delay for 3 seconds
}

startTimer()
