let processingVote = false; // Флаг для предотвращения множественных кликов

function voteQuestion(questionId, voteValue) {
    if (processingVote) return;
    if (!checkAuth()) return;

    const csrfToken = getCSRFToken();
    if (!csrfToken) {
        alert('Ошибка CSRF токена. Обновите страницу.');
        return;
    }

    // Проверяем текущее состояние кнопки
    const currentBtn = document.querySelector(`.question_text-vote[data-id="${questionId}"][data-value="${voteValue}"]`);
    const isActive = currentBtn.classList.contains('btn-primary');

    // Блокируем кнопки
    processingVote = true;
    const buttons = document.querySelectorAll(`.question_text-vote[data-id="${questionId}"]`);
    buttons.forEach(btn => btn.disabled = true);

    $.ajax({
        url: '/ajax/vote/question_text/',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        contentType: 'application/json',
        data: JSON.stringify({
            question_id: questionId,
            vote_value: voteValue
        }),
        success: function(response) {
            if (response.success) {
                // Обновляем рейтинг
                $(`#question_text-${questionId}-rating`).text(response.rating);
                if ($(`#question_text-${questionId}-total`).length) {
                    $(`#question_text-${questionId}-total`).text(response.total_votes || 0);
                }

                let displayVote = response.user_vote;
                if (isActive && response.user_vote === voteValue) {displayVote = 0;}

                updateVoteButtons('.question_text-vote', questionId, displayVote);
            } else {
                alert('Ошибка: ' + (response.error || 'Неизвестная ошибка'));
            }
        },
        error: function(xhr) {
            console.error('Ошибка голосования:', xhr.responseJSON?.error);
            alert(xhr.responseJSON?.error || 'Ошибка при голосовании');
        },
        complete: function() {
            buttons.forEach(btn => btn.disabled = false);
            processingVote = false;
        }
    });
}

function voteAnswer(answerId, voteValue) {
    if (processingVote) return;
    if (!checkAuth()) return;

    const csrfToken = getCSRFToken();
    if (!csrfToken) {
        alert('Ошибка CSRF токена. Обновите страницу.');
        return;
    }

    const currentBtn = document.querySelector(`.answer-vote[data-id="${answerId}"][data-value="${voteValue}"]`);
    const isActive = currentBtn.classList.contains('btn-primary');

    processingVote = true;
    const buttons = document.querySelectorAll(`.answer-vote[data-id="${answerId}"]`);
    buttons.forEach(btn => btn.disabled = true);

    $.ajax({
        url: '/ajax/vote/answer/',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        contentType: 'application/json',
        data: JSON.stringify({
            answer_id: answerId,
            vote_value: voteValue
        }),
        success: function(response) {
            if (response.success) {
                $(`#answer-${answerId}-rating`).text(response.rating);
                if ($(`#answer-${answerId}-total`).length) {
                    $(`#answer-${answerId}-total`).text(response.total_votes || 0);
                }

                let displayVote = response.user_vote;
                if (isActive && response.user_vote === voteValue) {
                    displayVote = 0;
                }

                updateVoteButtons('.answer-vote', answerId, displayVote);
            } else {
                alert('Ошибка: ' + (response.error || 'Неизвестная ошибка'));
            }
        },
        error: function(xhr) {
            console.error('Ошибка голосования:', xhr.responseJSON?.error);
            alert(xhr.responseJSON?.error || 'Ошибка при голосовании');
        },
        complete: function() {
            buttons.forEach(btn => btn.disabled = false);
            processingVote = false;
        }
    });
}

function markCorrectAnswer(questionId, answerId) {
    if (processingVote) return;
    if (!checkAuth()) return;

    const csrfToken = getCSRFToken();
    if (!csrfToken) {
        alert('Ошибка CSRF токена. Обновите страницу.');
        return;
    }

    const button = document.getElementById(`mark-correct-${answerId}`);
    if (button) button.disabled = true;
    processingVote = true;

    $.ajax({
        url: '/ajax/mark-correct/',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        contentType: 'application/json',
        data: JSON.stringify({
            question_id: questionId,
            answer_id: answerId
        }),
        success: function(response) {
            if (response.success) {
                const answerElement = document.getElementById(`answer-${answerId}`);
                const allAnswers = document.querySelectorAll('.card__answers');

                if (response.is_correct) {
                    answerElement.classList.add('border-success', 'bg-light');

                    let badge = answerElement.querySelector('.correct-badge');
                    if (!badge) {
                        badge = document.createElement('span');
                        badge.className = 'badge bg-success correct-badge ms-2';
                        badge.textContent = '✅ Правильный ответ';

                        const buttonContainer = answerElement.querySelector('.question__footer > div:first-child');
                        if (buttonContainer) {
                            buttonContainer.innerHTML = '';
                            buttonContainer.appendChild(badge);
                        }
                    }

                    const button = document.getElementById(`mark-correct-${answerId}`);
                    if (button) button.style.display = 'none';

                    allAnswers.forEach(el => {
                        if (el.id !== `answer-${answerId}`) {
                            el.classList.remove('border-success', 'bg-light');
                            const otherBadge = el.querySelector('.correct-badge');
                            if (otherBadge) otherBadge.remove();

                            const otherButton = el.querySelector(`[id^="mark-correct-"]`);
                            if (otherButton) otherButton.style.display = 'inline-block';
                        }
                    });
                } else {
                    answerElement.classList.remove('border-success', 'bg-light');
                    const badge = answerElement.querySelector('.correct-badge');
                    if (badge) badge.remove();

                    const button = document.getElementById(`mark-correct-${answerId}`);
                    if (button) button.style.display = 'inline-block';
                }
            } else {
                alert('Ошибка: ' + (response.error || 'Неизвестная ошибка'));
            }
        },
        error: function(xhr) {
            console.error('Ошибка отметки правильного ответа:', xhr.responseJSON?.error);
            alert(xhr.responseJSON?.error || 'Ошибка при отметке правильного ответа');
        },
        complete: function() {
            if (button) button.disabled = false;
            processingVote = false;
        }
    });
}

function checkAuth() {
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    if (!isAuthenticated) {
        alert('Для голосования необходимо войти в систему');
        return false;
    }
    return true;
}

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.content || '';
}

function updateVoteButtons(selector, id, userVote) {
    $(`${selector}[data-id="${id}"]`).removeClass('btn-primary').addClass('btn-outline-primary');

    if (userVote === 1) {
        $(`${selector}[data-id="${id}"][data-value="1"]`).removeClass('btn-outline-primary').addClass('btn-primary');
    } else if (userVote === -1) {
        $(`${selector}[data-id="${id}"][data-value="-1"]`).removeClass('btn-outline-primary').addClass('btn-primary');
    }
}