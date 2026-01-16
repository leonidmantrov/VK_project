//// Функции для голосования
//function voteQuestion(questionId, voteValue) {
//    if (!checkAuth()) return;  // ← Добавить проверку
//
//    $.ajax({
//        url: '/questions/ajax/vote/question/',
//        type: 'POST',
//        headers: {'X-CSRFToken': getCSRFToken()},
//        contentType: 'application/json',
//        data: JSON.stringify({
//            question_id: questionId,
//            vote_value: voteValue
//        }),
//        success: function(response) {
//            if (response.success) {
//                // Обновляем рейтинг на странице
//                $(`#question-${questionId}-rating`).text(response.rating);
//                $(`#question-${questionId}-total`).text(response.total_votes || 0);
//
//                // Обновляем активные кнопки
//                updateVoteButtons('.question-vote', questionId, response.user_vote);
//            }
//        },
//        error: function(xhr) {
//            console.error('Ошибка голосования:', xhr.responseJSON?.error);
//        }
//    });
//}
//
//function voteAnswer(answerId, voteValue) {
//    if (!checkAuth()) return;  // ← Добавить проверку
//
//    $.ajax({
//        url: '/questions/ajax/vote/answer/',
//        type: 'POST',
//        headers: {'X-CSRFToken': getCSRFToken()},
//        contentType: 'application/json',
//        data: JSON.stringify({
//            answer_id: answerId,
//            vote_value: voteValue
//        }),
//        success: function(response) {
//            if (response.success) {
//                // Обновляем рейтинг на странице
//                $(`#answer-${answerId}-rating`).text(response.rating);
//                $(`#answer-${answerId}-total`).text(response.total_votes || 0);
//
//                // Обновляем активные кнопки
//                updateVoteButtons('.answer-vote', answerId, response.user_vote);
//            }
//        },
//        error: function(xhr) {
//            console.error('Ошибка голосования:', xhr.responseJSON?.error);
//        }
//    });
//}

function voteQuestion(questionId, voteValue) {
    if (!checkAuth()) return;

    // Получаем CSRF токен
    const csrfToken = getCSRFToken();
    if (!csrfToken) {
        alert('Ошибка CSRF токена. Обновите страницу.');
        return;
    }

    // Блокируем кнопки на время запроса
    const buttons = document.querySelectorAll(`.question-vote[data-id="${questionId}"]`);
    buttons.forEach(btn => btn.disabled = true);

    $.ajax({
        url: '/questions/ajax/vote/question/',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'  // ← ДОБАВИТЬ ЭТО
        },
        contentType: 'application/json',
        data: JSON.stringify({
            question_id: questionId,
            vote_value: voteValue
        }),
        success: function(response) {
            if (response.success) {
                // Обновляем рейтинг на странице
                $(`#question-${questionId}-rating`).text(response.rating);
                $(`#question-${questionId}-total`).text(response.total_votes || 0);

                // Обновляем активные кнопки
                updateVoteButtons('.question-vote', questionId, response.user_vote);
            } else {
                alert('Ошибка: ' + (response.error || 'Неизвестная ошибка'));
            }
        },
        error: function(xhr) {
            console.error('Ошибка голосования:', xhr.responseJSON?.error);

            let errorMessage = 'Ошибка при голосовании';
            if (xhr.status === 403) {
                errorMessage = 'Ошибка CSRF. Попробуйте обновить страницу.';
            } else if (xhr.responseJSON?.error) {
                errorMessage = xhr.responseJSON.error;
            }

            alert(errorMessage);
        },
        complete: function() {
            // Разблокируем кнопки после запроса
            buttons.forEach(btn => btn.disabled = false);
        }
    });
}

function voteAnswer(answerId, voteValue) {
    if (!checkAuth()) return;

    // Получаем CSRF токен
    const csrfToken = getCSRFToken();
    if (!csrfToken) {
        alert('Ошибка CSRF токена. Обновите страницу.');
        return;
    }

    // Блокируем кнопки на время запроса
    const buttons = document.querySelectorAll(`.answer-vote[data-id="${answerId}"]`);
    buttons.forEach(btn => btn.disabled = true);

    $.ajax({
        url: '/questions/ajax/vote/answer/',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'  // ← ДОБАВИТЬ ЭТО
        },
        contentType: 'application/json',
        data: JSON.stringify({
            answer_id: answerId,
            vote_value: voteValue
        }),
        success: function(response) {
            if (response.success) {
                // Обновляем рейтинг на странице
                $(`#answer-${answerId}-rating`).text(response.rating);
                $(`#answer-${answerId}-total`).text(response.total_votes || 0);

                // Обновляем активные кнопки
                updateVoteButtons('.answer-vote', answerId, response.user_vote);
            } else {
                alert('Ошибка: ' + (response.error || 'Неизвестная ошибка'));
            }
        },
        error: function(xhr) {
            console.error('Ошибка голосования:', xhr.responseJSON?.error);

            let errorMessage = 'Ошибка при голосовании';
            if (xhr.status === 403) {
                errorMessage = 'Ошибка CSRF. Попробуйте обновить страницу.';
            } else if (xhr.responseJSON?.error) {
                errorMessage = xhr.responseJSON.error;
            }

            alert(errorMessage);
        },
        complete: function() {
            // Разблокируем кнопки после запроса
            buttons.forEach(btn => btn.disabled = false);
        }
    });
}

// Добавить функцию проверки аутентификации
function checkAuth() {
    // Проверяем по data-атрибуту body
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    if (!isAuthenticated) {
        alert('Для голосования необходимо войти в систему');
        return false;
    }
    return true;
}

// Вспомогательные функции
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.content || '';
}

// Универсальная функция для обновления кнопок
function updateVoteButtons(selector, id, userVote) {
    // Убираем активный класс со всех кнопок
    $(`${selector}[data-id="${id}"]`).removeClass('btn-primary').addClass('btn-outline-primary');

    // Добавляем активный класс нажатой кнопке
    if (userVote === 1) {
        $(`${selector}[data-id="${id}"][data-value="1"]`).removeClass('btn-outline-primary').addClass('btn-primary');
    } else if (userVote === -1) {
        $(`${selector}[data-id="${id}"][data-value="-1"]`).removeClass('btn-outline-primary').addClass('btn-primary');
    }
}