// Add interactive effects
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');
    const panelBtns = document.querySelectorAll('.panel-btn');

    // Search input focus effect
    searchInput.addEventListener('focus', function() {
        this.style.transform = 'translateY(-3px)';
    });

    searchInput.addEventListener('blur', function() {
        this.style.transform = 'translateY(0)';
    });

    // Panel button click effects
    panelBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            this.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.style.transform = 'scale(1.1)';
            }, 100);
        });
    });

    // Typing effect for quote
    const quoteText = document.querySelector('.quote-text');
    const originalText = quoteText.textContent;
    quoteText.textContent = '';

    let i = 0;

    function typeWriter() {
        if (i < originalText.length) {
            quoteText.textContent += originalText.charAt(i);
            i++;
            setTimeout(typeWriter, 50);
        }
    }

    setTimeout(typeWriter, 1000);

    // Create more floating particles
    function createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.width = (Math.random() * 4 + 2) + 'px';
        particle.style.height = particle.style.width;
        particle.style.animationDelay = Math.random() * 6 + 's';
        document.body.appendChild(particle);

        setTimeout(() => {
            particle.remove();
        }, 6000);
    }

    // Create particles periodically
    setInterval(createParticle, 2000);
});