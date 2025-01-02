document.addEventListener('DOMContentLoaded', function() {
    const telegramLoginButton = document.getElementById('telegramLoginButton');
    const spinner = document.getElementById('spinner');
    const csrfToken = document.getElementById('csrfToken').value;
    const telegramLoginUrl = telegramLoginButton.getAttribute('data-telegram-login-url');
    const errorMessageElement = document.getElementById('error-message');

    function toggleSpinner(isVisible) {
        spinner.style.display = isVisible ? 'block' : 'none';
        telegramLoginButton.style.display = isVisible ? 'none' : 'block';
        telegramLoginButton.style.margin = '0 auto';
    }

    function updateWelcomeText(name) {
        welcomeMessage.innerHTML = welcomeMessage.innerHTML.replace(/Добро пожаловать на мою страничку,\s*[^<]+/, `Добро пожаловать на мою страничку, ${name}`);
    }

    function showErrorMessage(message) {
        errorMessageElement.textContent = message;
        errorMessageElement.style.display = 'block';
    }

    function hideErrorMessage() {
        errorMessageElement.style.display = 'none';
    }

    function handleUserFetch(username) {
        return fetch(`/api/v1/user/${username}`)
            .then(response => {
                if (response.status === 404) {
                    return null; // User not found
                } else if (!response.ok) {
                    showErrorMessage('An error occurred. Please try again');
                    throw new Error('User fetch failed');
                }
                return response.json();
            });
    }

    function createUser(username) {
        return fetch(`/api/v1/user/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ "username": username })
        }).then(response => {
            if (!response.ok) {
                throw new Error('User creation failed');
            }
            return response.json();
        });
    }

    function startPolling(username) {
        const pollingInterval = 5000; // Poll every 5 seconds
        const polling = setInterval(() => {
            fetch(`/api/v1/user/${username}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Polling failed');
                    }
                    return response.json();
                })
                .then(data => handlePollingResponse(data, polling, username))
                .catch(error => {
                    console.error('Polling error:', error);
                    showErrorMessage('An error occurred. Please try again');
                });
        }, pollingInterval);
    }

    function handlePollingResponse(data, polling, username) {
        console.log('Polling data:', data);
        if (data.parent_username) {
            startPolling(data.parent_username);
            clearInterval(polling);
            deleteUser(username);
        }

        if (data.is_active) {
            clearInterval(polling);
            toggleSpinner(false);
            telegramLoginButton.textContent = 'Выйти';
            updateWelcomeText(data.first_name);
        }
    }

    function deleteUser(username) {
        return fetch(`/api/v1/user/${username}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            }
        }).then(response => {
            if (!response.ok) {
                throw new Error('User deletion failed');
            }
        });
    }

    telegramLoginButton.addEventListener('click', function() {
        const username = telegramLoginButton.getAttribute('data-username');

        if (telegramLoginButton.textContent === 'Войти через Telegram') {
            toggleSpinner(true);
            handleUserFetch(username)
                .then(data => {
                    if (data) {
                        toggleSpinner(false);
                        telegramLoginButton.textContent = 'Выйти';
                        updateWelcomeText(data.first_name);
                    } else {
                        return createUser(username);
                    }
                })
                .then(data => {
                    if (data) {
                        console.log('Success:', data);
                        window.open(telegramLoginUrl, '_blank');
                        startPolling(username);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showErrorMessage('An error occurred. Please try again');
                    toggleSpinner(false);
                });
        } else if (telegramLoginButton.textContent === 'Выйти') {
            updateWelcomeText('друг');
            telegramLoginButton.textContent = 'Войти через Telegram';
        }
    });
});
