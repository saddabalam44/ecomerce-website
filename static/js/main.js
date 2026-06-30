// ShopSphere AJAX Scripts

document.addEventListener('DOMContentLoaded', () => {
    // CSRF Utility
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Add to Cart AJAX
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const url = form.getAttribute('action');
            const data = new FormData(form);

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                body: data
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update global cart badge
                    const cartBadges = document.querySelectorAll('.cart-badge');
                    cartBadges.forEach(badge => {
                        badge.textContent = data.total_items;
                    });
                    
                    // Trigger alert modal or message
                    alertMessage(data.message, 'success');
                } else {
                    alertMessage('Failed to add product to cart', 'danger');
                }
            })
            .catch(err => console.error(err));
        });
    });

    // Wishlist Toggle AJAX
    const wishlistToggles = document.querySelectorAll('.wishlist-toggle');
    wishlistToggles.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const url = btn.getAttribute('href');
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    const wishlistBadges = document.querySelectorAll('.wishlist-badge');
                    wishlistBadges.forEach(badge => {
                        badge.textContent = data.wishlist_count;
                    });
                    
                    if (data.action === 'added') {
                        btn.classList.add('active');
                        btn.innerHTML = '<i class="bi bi-heart-fill text-danger"></i>';
                    } else {
                        btn.classList.remove('active');
                        btn.innerHTML = '<i class="bi bi-heart"></i>';
                    }
                    alertMessage(data.message, 'success');
                } else {
                    alertMessage(data.message, 'danger');
                }
            })
            .catch(err => console.error(err));
        });
    });

    // Dismiss Notification AJAX
    const dismissBtns = document.querySelectorAll('.dismiss-notification');
    dismissBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const url = btn.getAttribute('href');
            const row = btn.closest('.notification-item');

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    row.style.opacity = '0';
                    setTimeout(() => {
                        row.remove();
                    }, 300);
                }
            })
            .catch(err => console.error(err));
        });
    });

    // Toast/Alert Generator
    function alertMessage(msg, type) {
        const container = document.getElementById('alert-container');
        if (!container) return;

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show border-0 shadow-sm`;
        alertDiv.innerHTML = `
            ${msg}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        container.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 3000);
    }
});
