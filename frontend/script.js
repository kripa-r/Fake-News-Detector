document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analyze-form');
    const urlInput = document.getElementById('url-input');
    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');
    const errorContainer = document.getElementById('error-container');
    const historyList = document.getElementById('history-list');
    const clearHistoryBtn = document.getElementById('clear-history');

    // API endpoint
    const API_URL = 'http://127.0.0.1:8000/api/analyze';

    // Load history from localStorage on page load
    loadHistory();

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = urlInput.value.trim();
        if (!url) return;

        // Show loader and hide previous results/errors
        loader.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            displayResults(data);
            saveToHistory(data);
            loadHistory();

        } catch (error) {
            console.error('Error:', error);
            showError();
        } finally {
            loader.classList.add('hidden');
            form.reset();
        }
    });

    clearHistoryBtn.addEventListener('click', () => {
        localStorage.removeItem('analysisHistory');
        loadHistory();
    });

    function displayResults(data) {
        if (data.classification === "Error") {
            showError();
            return;
        }

        const classificationEl = document.getElementById('result-classification');
        const confidenceBar = document.getElementById('confidence-bar');
        const confidenceScoreEl = document.getElementById('confidence-score');
        const checkedUrlEl = document.getElementById('checked-url');
        const resultCard = document.getElementById('result-card');

        // Set classification text and color
        classificationEl.textContent = data.classification;
        if (data.classification === 'Real News') {
            classificationEl.className = 'real-text';
            resultCard.className = 'real';
            confidenceBar.style.backgroundColor = 'var(--real-color)';
        } else {
            classificationEl.className = 'fake-text';
            resultCard.className = 'fake';
            confidenceBar.style.backgroundColor = 'var(--fake-color)';
        }

        // Set confidence score
        const confidencePercent = (data.confidence_score * 100).toFixed(2);
        confidenceScoreEl.textContent = `${confidencePercent}%`;
        confidenceBar.style.width = `${confidencePercent}%`;

        // Set URL
        checkedUrlEl.textContent = data.url;
        checkedUrlEl.href = data.url;

        resultsContainer.classList.remove('hidden');
    }

    function showError() {
        errorContainer.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
    }

    function saveToHistory(data) {
        if (data.classification === "Error") return;
        let history = JSON.parse(localStorage.getItem('analysisHistory')) || [];
        // Add new item to the beginning of the array
        history.unshift(data);
        // Keep history to a reasonable size (e.g., 10 items)
        if (history.length > 10) {
            history.pop();
        }
        localStorage.setItem('analysisHistory', JSON.stringify(history));
    }

    function loadHistory() {
        let history = JSON.parse(localStorage.getItem('analysisHistory')) || [];
        historyList.innerHTML = ''; // Clear current list

        if (history.length === 0) {
            historyList.innerHTML = '<p>Your recent analyses will appear here.</p>';
            clearHistoryBtn.classList.add('hidden');
            return;
        }

        clearHistoryBtn.classList.remove('hidden');
        history.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            const resultClass = item.classification === 'Real News' ? 'real-text' : 'fake-text';
            
            historyItem.innerHTML = `
                <div class="url"><a href="${item.url}" target="_blank" rel="noopener noreferrer">${item.url}</a></div>
                <div class="result ${resultClass}">${item.classification}</div>
            `;
            historyList.appendChild(historyItem);
        });
    }
});