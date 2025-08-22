// Add smooth scrolling and animations
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved theme preference or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const navbar = document.querySelector('.navbar');
    
    // Navbar scroll effect
    function handleScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    // Add scroll event listener
    window.addEventListener('scroll', handleScroll);
    
    // Initial check
    handleScroll();

    // Add fade-in animation to main elements
    const elements = document.querySelectorAll('.organization-details, .offer-info');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(el => {
        observer.observe(el);
    });

    // Add hover effects to info items
    const infoItems = document.querySelectorAll('.info-item');
    infoItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });

    // Add click effect to detail cards
    const detailCards = document.querySelectorAll('.detail-card');
    detailCards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Smooth scroll for navbar brand
    document.querySelector('.navbar-brand').addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Add copy functionality to copy buttons
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const textToCopy = this.getAttribute('data-clipboard-text') || this.href;
            navigator.clipboard.writeText(textToCopy).then(function() {
                // Show toast notification
                showToast('تم نسخ الرابط إلى الحافظة');
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        });
    });

    // Carousel functionality for cover images
    const coverTrack = document.querySelector('.cover-carousel-track');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const indicators = document.querySelectorAll('.indicator');
    
    if (coverTrack && prevBtn && nextBtn && indicators.length > 0) {
        let currentIndex = 0;
        const slideCount = indicators.length;
        const slideWidth = 100; // Each slide is 100% width
        
        // Update carousel position
        function updateCarousel() {
            coverTrack.style.transform = `translateX(${currentIndex * slideWidth}%)`;
            
            // Update indicators
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentIndex);
            });
        }
        
        // Next slide
        function nextSlide() {
            currentIndex = (currentIndex + 1) % slideCount;
            updateCarousel();
        }
        
        // Previous slide
        function prevSlide() {
            currentIndex = (currentIndex - 1 + slideCount) % slideCount;
            updateCarousel();
        }
        
        // Auto slide every 5 seconds
        let autoSlide = setInterval(nextSlide, 5000);
        
        // Event listeners for buttons
        nextBtn.addEventListener('click', () => {
            nextSlide();
            resetAutoSlide();
        });
        
        prevBtn.addEventListener('click', () => {
            prevSlide();
            resetAutoSlide();
        });
        
        // Event listeners for indicators
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                currentIndex = index;
                updateCarousel();
                resetAutoSlide();
            });
        });
        
        // Reset auto slide timer
        function resetAutoSlide() {
            clearInterval(autoSlide);
            autoSlide = setInterval(nextSlide, 5000);
        }
    }

    // Carousel functionality for offers slider
    const track = document.getElementById('offersTrack');
    const prevBtnOffers = document.getElementById('prevBtn');
    const nextBtnOffers = document.getElementById('nextBtn');
    const indicatorsContainer = document.getElementById('indicators');
    
    if (track && prevBtnOffers && nextBtnOffers) {
        let currentIndex = 0;
        let cards = Array.from(track.children);
        let cardCount = cards.length;
        let cardWidth = cards[0]?.offsetWidth + 32 || 352; // 32px for gap
        let visibleCards = Math.floor(track.parentElement.offsetWidth / cardWidth);
        let maxIndex = cardCount - visibleCards;
        
        // Create indicators
        if (indicatorsContainer) {
            for (let i = 0; i <= maxIndex; i++) {
                const indicator = document.createElement('div');
                indicator.classList.add('indicator');
                if (i === 0) indicator.classList.add('active');
                indicator.dataset.index = i;
                indicator.addEventListener('click', () => moveToSlide(i));
                indicatorsContainer.appendChild(indicator);
            }
        }
        
        const indicators = Array.from(indicatorsContainer?.children || []);
        
        // Check if carousel is needed (content overflows horizontally)
        function isOverflowing() {
            return track.scrollWidth > track.parentElement.offsetWidth;
        }
        
        // Update button states
        function updateButtons() {
            if (!isOverflowing()) {
                prevBtnOffers.disabled = true;
                nextBtnOffers.disabled = true;
                return;
            }
            
            prevBtnOffers.disabled = currentIndex === 0;
            nextBtnOffers.disabled = currentIndex === maxIndex;
        }
        
        // Update indicators
        function updateIndicators() {
            if (!indicatorsContainer) return;
            
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentIndex);
            });
        }
        
        // Move slider to specific index
        function moveToSlide(index) {
            if (!isOverflowing()) return;
            
            currentIndex = Math.max(0, Math.min(index, maxIndex));
            const translateX = currentIndex * cardWidth;
            track.style.transform = `translateX(${translateX}px)`;
            
            updateButtons();
            updateIndicators();
        }
        
        // Move slider by offset
        function moveSlider(offset) {
            moveToSlide(currentIndex + offset);
        }
        
        // Initialize carousel
        function initCarousel() {
            if (!isOverflowing()) {
                // Hide controls if not needed
                if (prevBtnOffers) prevBtnOffers.style.display = 'none';
                if (nextBtnOffers) nextBtnOffers.style.display = 'none';
                if (indicatorsContainer) indicatorsContainer.style.display = 'none';
                return;
            }
            
            updateButtons();
            updateIndicators();
        }
        
        // Event listeners for buttons
        prevBtnOffers.addEventListener('click', () => moveSlider(-1));
        nextBtnOffers.addEventListener('click', () => moveSlider(1));
        
        // Handle window resize
        window.addEventListener('resize', () => {
            cardWidth = cards[0]?.offsetWidth + 32 || 352;
            visibleCards = Math.floor(track.parentElement.offsetWidth / cardWidth);
            maxIndex = Math.max(0, cardCount - visibleCards);
            currentIndex = Math.min(currentIndex, maxIndex);
            initCarousel();
            moveToSlide(currentIndex);
        });
        
        // Initialize carousel
        initCarousel();
    }

    // Add theme toggle button functionality
    const themeToggleBtn = document.querySelector('.theme-toggle-btn');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', toggleTheme);
    }
});

// Show toast notification
function showToast(message) {
    // Remove any existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    
    // Add to document
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// Add loading animation
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Theme toggle functionality
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}