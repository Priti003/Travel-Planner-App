document.addEventListener('DOMContentLoaded', () => {
    // Select elements
    let searchBtn = document.querySelector('#search-btn');
    let searchBar = document.querySelector('.search-bar-container');
    let formBtn = document.querySelector('#login-btn');
    let loginForm = document.querySelector('.login-form-container');
    let formClose = document.querySelector('#form-close');
    let menu = document.querySelector('#menu-bar');
    let navbar = document.querySelector('.navbar');
    let videoBtn = document.querySelectorAll('.vid-btn');
    let videoSlider = document.querySelector('#video-slider');

    // Add Plan Tour Link functionality
    let planTourLink = document.querySelector('a[href="#plan-tour-section"]');
    let planTourSection = document.querySelector('#plan-tour-section');

    // Scroll behavior for Plan Tour link
    if (planTourLink && planTourSection) {
        planTourLink.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent default link behavior
            planTourSection.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Window scroll behavior
    window.onscroll = () => {
        if (searchBtn) searchBtn.classList.remove('fa-times');
        if (searchBar) searchBar.classList.remove('active');
        if (menu) menu.classList.remove('fa-times');
        if (navbar) navbar.classList.remove('active');
        if (loginForm) loginForm.classList.remove('active');
    };

    // Menu toggle functionality
    if (menu) {
        menu.addEventListener('click', () => {
            menu.classList.toggle('fa-times');
            navbar.classList.toggle('active');
        });
    }

    // Search bar toggle functionality
    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            searchBtn.classList.toggle('fa-times');
            searchBar.classList.toggle('active');
        });
    }

    // Login form functionality
    if (formBtn) {
        formBtn.addEventListener('click', () => {
            loginForm.classList.add('active');
        });
    }

    if (formClose) {
        formClose.addEventListener('click', () => {
            loginForm.classList.remove('active');
        });
    }

    // Video control functionality
    if (videoBtn) {
        videoBtn.forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelector('.controls .active').classList.remove('active');
                btn.classList.add('active');
                let src = btn.getAttribute('data-src');
                if (videoSlider) {
                    videoSlider.src = src;
                    videoSlider.play(); // Ensure the video plays after swapping
                }
            });
        });
    }

    // Swiper sliders initialization

    // Review Swiper Slider
    var reviewSwiper = new Swiper(".review-slider", {
        spaceBetween: 20,
        loop: true,
        autoplay: {
            delay: 2500,
            disableOnInteraction: false,
        },
        breakpoints: {
            640: {
                slidesPerView: 1,
            },
            768: {
                slidesPerView: 2,
            },
            1024: {
                slidesPerView: 3,
            },
        },
    });

    // Brand Swiper Slider with updated configuration
    var brandSwiper = new Swiper('.brand-slider', {
        slidesPerView: 3,  // Number of slides visible at once
        spaceBetween: 30,  // Space between slides
        loop: true,  // Enable looping
        autoplay: {
            delay: 2500,  // Time between transitions
            disableOnInteraction: false,  // Continue autoplay after interaction
        },
        pagination: {
            el: '.swiper-pagination',  // Add pagination element
            clickable: true,  // Allow pagination to be clickable
        },
        navigation: {
            nextEl: '.swiper-button-next',  // Add next button
            prevEl: '.swiper-button-prev',  // Add previous button
        },
        breakpoints: {
            450: {
                slidesPerView: 2,
            },
            768: {
                slidesPerView: 3,
            },
            991: {
                slidesPerView: 4,
            },
            1200: {
                slidesPerView: 5,
            },
        },
    });
});
