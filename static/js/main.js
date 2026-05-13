// ── FAVORITE TOGGLE ──
document.addEventListener('click', function(e) {
    const btn = e.target.closest('.btn-fav');
    if (!btn) return;

    e.stopPropagation(); // nu deschide modalul la click pe inimă

    const url = btn.dataset.url;
    const csrfToken = getCsrf();

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(res => res.json())
    .then(data => {
        // update toate butoanele cu același movie-id (card + modal)
        document.querySelectorAll(`[data-movie-id="${data.movie_id}"]`).forEach(b => {
            if (data.is_favorite) {
                b.classList.add('active');
                b.title = 'Elimină din favorite';
                b.querySelector('span') && (b.querySelector('span').textContent = 'Elimină din favorite');
            } else {
                b.classList.remove('active');
                b.title = 'Adaugă la favorite';
                b.querySelector('span') && (b.querySelector('span').textContent = 'Adaugă la favorite');
                if (window.location.pathname.includes('watchlist')) {
                    const card = b.closest('.movie-card');
                    if (card) card.remove();
                }
            }
        });
    });
});

// ── MODAL ──
const modal        = document.getElementById('movieModal');
const modalClose   = document.getElementById('modalClose');
const modalTitle   = document.getElementById('modalTitle');
const modalGenre   = document.getElementById('modalGenre');
const modalYear    = document.getElementById('modalYear');
const modalDuration     = document.getElementById('modalDuration');
const modalDurationText = document.getElementById('modalDurationText');
const modalDescription  = document.getElementById('modalDescription');
const modalFavBtn       = document.getElementById('modalFavBtn');

// Deschide modal la click pe card
document.addEventListener('click', function(e) {
    const card = e.target.closest('.movie-card');
    if (!card) return;
    if (e.target.closest('.btn-fav')) return;

    const { title, year, genre, duration, description} = card.dataset;

    // Info
    modalTitle.textContent       = title;
    modalGenre.textContent       = genre;
    modalYear.textContent        = year;
    modalDescription.textContent = description;

    if (duration) {
        modalDurationText.textContent = duration + ' min';
        modalDuration.style.display   = 'flex';
    } else {
        modalDuration.style.display   = 'none';
    }

    const cardFavBtn = card.querySelector('.btn-fav');
    if (cardFavBtn) {
        modalFavBtn.style.display = 'flex';
        modalFavBtn.dataset.movieId = cardFavBtn.dataset.movieId;
        modalFavBtn.dataset.url     = cardFavBtn.dataset.url;
        syncFavBtn(modalFavBtn, cardFavBtn.classList.contains('active'));
    } else {
        modalFavBtn.style.display = 'none';
    }

    // Deschide
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
});

// Închide modal
function closeModal() {
    modal.classList.remove('open');
    document.body.style.overflow = '';
}

modalClose.addEventListener('click', closeModal);

// Click pe overlay închide
modal.addEventListener('click', function(e) {
    if (e.target === modal) closeModal();
});

// ESC închide
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
});

// Buton favorit din modal
modalFavBtn.addEventListener('click', function() {
    const csrfToken = getCsrf();
    fetch(modalFavBtn.dataset.url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(res => res.json())
    .then(data => {
        const isNowFav = data.is_favorite;
        syncFavBtn(modalFavBtn, isNowFav);

        // sincronizează și butonul de pe card
        const cardFavBtn = document.querySelector(`.btn-fav[data-movie-id="${data.movie_id}"]`);
        if (cardFavBtn) {
            isNowFav ? cardFavBtn.classList.add('active') : cardFavBtn.classList.remove('active');
        }
    });
});

// ── HELPERS ──
function syncFavBtn(btn, isActive) {
    const span = btn.querySelector('span');
    if (isActive) {
        btn.classList.add('active');
        if (span) span.textContent = 'Elimină din favorite';
    } else {
        btn.classList.remove('active');
        if (span) span.textContent = 'Adaugă la favorite';
    }
}

function getCsrf() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}