// Add interactive effects
document.addEventListener('DOMContentLoaded', function() {


    // Get elements
    const searchInput = document.querySelector('.search-input');
    const panelBtns = document.querySelectorAll('.panel-btn');
    const searchBtn = document.querySelector('.search-btn');
    const quoteSection = document.querySelector('.quote-section');
    let resultsSection = document.querySelector('.results-section');
    const header = document.querySelector('.header');
    const mainSection = document.querySelector('.main-content');
    const resultsList = document.querySelector('.results-list');
    const deleteBtn = document.querySelector('.delete-btn');
    const rankingRange = document.getElementById('ranking-range');
    const rankingValue = document.getElementById('ranking-value');
    const rankingValueResult = document.querySelector('.ranking-value');


    rankingRange.addEventListener('input', function() {
        rankingValue.textContent = rankingRange.value;
    });

    // Alert box elements
    function showCustomAlert(message) {
        const alertBox = document.getElementById('custom-alert');
        const alertMsg = document.getElementById('custom-alert-message');
        const alertClose = document.getElementById('custom-alert-close');
        alertMsg.textContent = message;
        alertBox.style.display = 'flex';
        alertClose.onclick = function() {
            alertBox.style.display = 'none';
        };
    }

    // Sửa hàm handleSearch
    async function handleSearch() {
        // Check if search input is empty
        if (searchInput.value.trim() === '') {
            showCustomAlert('Vui lòng nhập từ khóa tìm kiếm.');
            return;
        }

        // Show loading state
        resultsList.innerHTML = '<div class="loading">Đang tìm kiếm...</div>';

        quoteSection.style.display = 'none';
        resultsSection.style.display = 'block';
        header.classList.add('move-right');
        mainSection.classList.add('move-up');
        resultsSection.style.animation = 'fadeIn 0.5s ease-in-out';
        resultsSection.style.display = 'flex';
        resultsSection.style.justifyContent = 'center';

        // Sửa: Sử dụng giá trị thực từ input
        const searchData = {
            "query": searchInput.value.trim(),
            "model": getSelectedModel(), // Hàm để lấy model được chọn
            "top_n": parseInt(rankingRange.value)
        };

        try {
            // Sửa: Sử dụng await thay vì .then()
            const results = await searchNewsWithJSON(searchData);

            console.log('Search results:', results);

            // Clear loading
            resultsList.innerHTML = '';

            if (results && results.length > 0) {
                results.forEach(item => {
                    const resultItem = document.createElement('div');
                    resultItem.className = 'result-item';
                    resultItem.innerHTML = `
                    <h3>${item.title}</h3>
                    <p class="description">${item.description}</p>
                    <p class="content">${item.content.split(' ').slice(0, 50).join(' ')}...</p>
                    <div class="result-meta">
                        <span class="score">Score: ${item.score.toFixed(4)}</span>
                        <a href="${item.link}" target="_blank" class="read-more">Đọc thêm</a>
                    </div>
                `;
                    resultsList.appendChild(resultItem);
                });
            } else {
                resultsList.innerHTML = '<div class="no-results">Không tìm thấy kết quả nào.</div>';
            }

            rankingValueResult.textContent = rankingRange.value;

        } catch (error) {
            console.error('Search failed:', error);
            resultsList.innerHTML = '<div class="error">Có lỗi xảy ra khi tìm kiếm. Vui lòng thử lại.</div>';
            showCustomAlert('Có lỗi xảy ra khi tìm kiếm: ' + error.message);
        }
    }

    // Handle search button click
    searchBtn.addEventListener('click', function(e) {
        e.preventDefault();
        handleSearch();
    });

    // Handle Enter key press in search input
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // Prevent form submission
            handleSearch();
        }
    });

    // Handle delete button click
    deleteBtn.addEventListener('click', function(e) {
        e.preventDefault();
        searchInput.value = '';
        resultsSection.style.display = 'none';
        quoteSection.style.display = 'block';
        header.classList.remove('move-right');
        mainSection.classList.remove('move-up');

        // Example: Show all data on page load (or call this after search)
        renderResults(data);
    });




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

// Sửa lỗi trong hàm searchNewsWithJSON
async function searchNewsWithJSON(jsonData) {
    try {
        const response = await fetch('http://34.30.185.80:8386/api/v1/search/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData)
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }

        // Sửa lỗi: return await response.json() thay vì response.data
        return await response.json();
    } catch (error) {
        console.error('Search error:', error);
        throw error;
    }
}

// Hàm để lấy model được chọn từ UI
function getSelectedModel() {
    const selectedBtn = document.querySelector('.panel-btn.active');
    if (selectedBtn) {
        return selectedBtn.dataset.model || 'tf-idf';
    }
    return 'tf-idf'; // default
}

// // Thêm event listener cho panel buttons
// panelBtns.forEach(btn => {
//     btn.addEventListener('click', function() {
//         // Remove active class from all buttons
//         panelBtns.forEach(b => b.classList.remove('active'));
//         // Add active class to clicked button
//         this.classList.add('active');

//         this.style.transform = 'scale(0.9)';
//         setTimeout(() => {
//             this.style.transform = 'scale(1.1)';
//         }, 100);
//     });
// });