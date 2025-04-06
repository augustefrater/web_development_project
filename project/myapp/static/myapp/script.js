document.addEventListener('DOMContentLoaded', function() {
    const header = document.getElementById('main-header');
    const menuToggle = document.getElementById('menu-toggle');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop) {
            // Downscroll code
            header.style.top = '-100px';  // Hide header
            menuToggle.classList.remove('hidden');
            menuToggle.classList.add('shown');
        } else {
            // Upscroll code
            header.style.top = '0';
            menuToggle.classList.remove('shown');
            menuToggle.classList.add('hidden');
        }
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
    }, false);

    menuToggle.addEventListener('click', function() {
        // Toggle menu visibility
        if (header.style.top === '-100px') {
            header.style.top = '0';
            this.classList.remove('shown');
            this.classList.add('hidden');
        } else {
            header.style.top = '-100px';
            this.classList.remove('hidden');
            this.classList.add('shown');
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    displayRecentlyViewed();
});

function viewBook(title, link, image) {
    const book = { title, link, image };
    let viewedBooks = JSON.parse(localStorage.getItem('recentBooks')) || [];

    // Remove duplicate entries
    viewedBooks = viewedBooks.filter(b => b.title !== title);

    // Add the new book to the start
    viewedBooks.unshift(book);

    // Limit to 5 recent books
    viewedBooks = viewedBooks.slice(0, 5);

    // Save to localStorage
    localStorage.setItem('recentBooks', JSON.stringify(viewedBooks));

    // Redirect to book page
    window.location.href = link;
}

function displayRecentlyViewed() {
    const recentList = document.getElementById('recent-list');
    const noRecentImage = document.getElementById('no-recent-image');
    const viewedBooks = JSON.parse(localStorage.getItem('recentBooks')) || [];

    recentList.innerHTML = '';

    if (viewedBooks.length === 0) {
        noRecentImage.style.display = 'block';
        return;
    } else {
        noRecentImage.style.display = 'none';
    }

    viewedBooks.forEach(book => {
        const bookDiv = document.createElement('div');
        bookDiv.classList.add('slide');
        bookDiv.innerHTML = `
            <a href="${book.link}">
                <img src="${book.image}" alt="${book.title}">
            </a>
        `;
        recentList.appendChild(bookDiv);
    });
}
