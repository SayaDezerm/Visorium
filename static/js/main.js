document.addEventListener('click', function(e) {
    const btn = e.target.closest('.btn-fav');
    if (!btn) return;

    const url = btn.dataset.url;
    const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.is_favorite) {
            btn.classList.add('active');
            btn.title = 'Elimină din favorite';
        } else {
            btn.classList.remove('active');
            btn.title = 'Adaugă la favorite';
            if (window.location.pathname.includes('watchlist')) {
                btn.closest('.movie-card').remove();
            }
        }
    });
});