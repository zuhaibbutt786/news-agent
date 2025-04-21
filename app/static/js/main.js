document.addEventListener('DOMContentLoaded', function() {
    // Language switcher
    const languageLinks = document.querySelectorAll('[data-lang]');
    languageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            switchLanguage(lang);
            
            // Save language preference in localStorage
            localStorage.setItem('preferredLanguage', lang);
        });
    });
    
    // Check for saved language preference
    const savedLanguage = localStorage.getItem('preferredLanguage');
    if (savedLanguage) {
        switchLanguage(savedLanguage);
    }
    
    function switchLanguage(lang) {
        const englishElements = document.querySelectorAll('.english-text');
        const urduElements = document.querySelectorAll('.urdu-text');
        
        if (lang === 'ur') {
            englishElements.forEach(el => el.style.display = 'none');
            urduElements.forEach(el => el.style.display = 'block');
            document.body.style.direction = 'rtl';
            
            // Update dropdown button text
            const languageDropdown = document.getElementById('languageDropdown');
            if (languageDropdown) {
                languageDropdown.textContent = 'Urdu';
            }
        } else {
            englishElements.forEach(el => el.style.display = 'block');
            urduElements.forEach(el => el.style.display = 'none');
            document.body.style.direction = 'ltr';
            
            // Update dropdown button text
            const languageDropdown = document.getElementById('languageDropdown');
            if (languageDropdown) {
                languageDropdown.textContent = 'English';
            }
        }
    }
    
    // Lazy loading images
    if ('loading' in HTMLImageElement.prototype) {
        // Browser supports native lazy loading
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // Fallback for browsers that don't support lazy loading
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
        document.body.appendChild(script);
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add current date to the footer
    const footerYear = document.querySelector('footer .text-center p');
    if (footerYear) {
        const currentYear = new Date().getFullYear();
        footerYear.innerHTML = footerYear.innerHTML.replace(/\d{4}/, currentYear);
    }
    
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});