// Add smooth scrolling and animations
document.addEventListener('DOMContentLoaded', function() {
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

    const track = document.getElementById('offersTrack');
    const indicatorsContainer = document.getElementById('indicators');
    
    if (track) {
        let currentIndex = 0;
        let cards = Array.from(track.children);
        let cardCount = cards.length;
        let cardWidth = cards[0]?.offsetWidth + 32 || 352; // 32px for gap
        let visibleCards = Math.floor(track.parentElement.offsetWidth / cardWidth);
        let maxIndex = cardCount - visibleCards;
        let startX = 0;
        let startY = 0;
        let isDragging = false;
        let startTime = 0;
        
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
            const translateX = -(currentIndex * cardWidth);
            track.style.transform = `translateX(${translateX}px)`;
            
            updateIndicators();
        }
        
        // Touch and drag events
        track.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isDragging = true;
            startTime = new Date().getTime();
            track.style.transition = 'none';
        });
        
        track.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            
            const currentX = e.touches[0].clientX;
            const currentY = e.touches[0].clientY;
            const diffX = currentX - startX;
            const diffY = currentY - startY;
            
            // Check if horizontal or vertical scrolling
            if (Math.abs(diffX) > Math.abs(diffY)) {
                e.preventDefault();
                const translateX = -(currentIndex * cardWidth) + diffX;
                track.style.transform = `translateX(${translateX}px)`;
            }
        });
        
        track.addEventListener('touchend', (e) => {
            if (!isDragging) return;
            
            isDragging = false;
            track.style.transition = 'transform 0.5s ease-in-out';
            
            const endX = e.changedTouches[0].clientX;
            const diffX = endX - startX;
            const deltaTime = new Date().getTime() - startTime;
            
            // Determine if it's a swipe or just a tap
            if (Math.abs(diffX) > 50 || (Math.abs(diffX) > 10 && deltaTime < 300)) {
                if (diffX > 0 && currentIndex > 0) {
                    moveToSlide(currentIndex - 1);
                } else if (diffX < 0 && currentIndex < maxIndex) {
                    moveToSlide(currentIndex + 1);
                } else {
                    moveToSlide(currentIndex);
                }
            } else {
                moveToSlide(currentIndex);
            }
        });
        
        // Auto slide functionality
        function autoSlideOffers() {
            if (isOverflowing()) {
                currentIndex = (currentIndex + 1) % (maxIndex + 1);
                moveToSlide(currentIndex);
            }
        }
        
        // Start auto sliding
        let autoSlideInterval = setInterval(autoSlideOffers, 4000);
        
        // Pause auto sliding when user interacts
        track.addEventListener('touchstart', () => {
            clearInterval(autoSlideInterval);
        });
        
        track.addEventListener('touchend', () => {
            autoSlideInterval = setInterval(autoSlideOffers, 4000);
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            cardWidth = cards[0]?.offsetWidth + 32 || 352;
            visibleCards = Math.floor(track.parentElement.offsetWidth / cardWidth);
            maxIndex = Math.max(0, cardCount - visibleCards);
            currentIndex = Math.min(currentIndex, maxIndex);
            moveToSlide(currentIndex);
        });
        
        // Initialize carousel
        moveToSlide(0);
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

// Add carousel functionality to profile.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize carousel
    const carouselTrack = document.querySelector('.carousel-track');
    const carouselItems = document.querySelectorAll('.carousel-item');
    const indicatorsContainer = document.querySelector('.carousel-indicators');
    
    if (carouselTrack && carouselItems.length > 0) {
        let currentIndex = 0;
        const totalItems = carouselItems.length;
        let autoSlideInterval;
        
        // Create indicators
        function createIndicators() {
            if (!indicatorsContainer) return;
            
            for (let i = 0; i < totalItems; i++) {
                const indicator = document.createElement('div');
                indicator.classList.add('carousel-indicator');
                if (i === 0) indicator.classList.add('active');
                indicator.addEventListener('click', () => goToSlide(i));
                indicatorsContainer.appendChild(indicator);
            }
        }
        
        // Update indicators
        function updateIndicators() {
            if (!indicatorsContainer) return;
            
            const indicators = indicatorsContainer.querySelectorAll('.carousel-indicator');
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentIndex);
            });
        }
        
        // Go to specific slide
        function goToSlide(index) {
            if (index < 0 || index >= totalItems) return;
            
            currentIndex = index;
            const offset = currentIndex * 100;
            carouselTrack.style.transform = `translateX(${offset}%)`;
            
            updateIndicators();
            resetAutoSlide();
        }
        
        // Next slide
        function nextSlide() {
            currentIndex = (currentIndex + 1) % totalItems;
            goToSlide(currentIndex);
        }
        
        // Previous slide
        function prevSlide() {
            currentIndex = (currentIndex - 1 + totalItems) % totalItems;
            goToSlide(currentIndex);
        }
        
        // Start auto slide
        function startAutoSlide() {
            if (totalItems > 1) {
                autoSlideInterval = setInterval(nextSlide, 4000);
            }
        }
        
        // Reset auto slide
        function resetAutoSlide() {
            clearInterval(autoSlideInterval);
            startAutoSlide();
        }
        
        // Initialize carousel
        function initCarousel() {
            // Set initial position
            carouselTrack.style.transform = `translateX(0%)`;
            
            // Add event listeners to controls
            document.querySelector('.carousel-next')?.addEventListener('click', nextSlide);
            document.querySelector('.carousel-prev')?.addEventListener('click', prevSlide);
            
            // Create indicators
            createIndicators();
            
            // Start auto slide
            startAutoSlide();
        }
        
        // Initialize the carousel
        initCarousel();
    }
    
});








// Add this function to initialize copy buttons
function initializeCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(button => {
        // Remove existing event listener to prevent duplicates
        button.removeEventListener('click', copyButtonHandler);
        // Add new event listener
        button.addEventListener('click', copyButtonHandler);
    });
}

// Separate the handler function
async function copyButtonHandler(e) {
    e.stopPropagation(); // Prevent row click event
    const url = this.getAttribute('data-url');
    
    try {
        // Try modern clipboard API first
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(url);
            showToast('تم نسخ الرابط بنجاح');
        } else {
            // Fallback for older browsers and non-HTTPS contexts
            const textArea = document.createElement('textarea');
            textArea.value = url;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            try {
                document.execCommand('copy');
                textArea.remove();
                showToast('تم نسخ الرابط بنجاح');
            } catch (err) {
                textArea.remove();
                showToast('حدث خطأ أثناء نسخ الرابط - الرجاء النسخ يدوياً');
                showSelectableUrl(url);
            }
        }
    } catch (err) {
        showToast('حدث خطأ أثناء نسخ الرابط - الرجاء النسخ يدوياً');
        showSelectableUrl(url);
    }
}

// Call initializeCopyButtons when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeCopyButtons();
});

