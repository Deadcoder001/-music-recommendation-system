document.getElementById('search-form').onsubmit = async function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<p>Searching...</p>';
    
    try {
        let response = await fetch('/search', {
            method: 'POST',
            body: formData
        });
        let data = await response.json();
        
        resultsDiv.innerHTML = '';
        if (data.error) {
            resultsDiv.textContent = data.error;
        } else if (data.songs) {
            resultsDiv.innerHTML = `<h2>Select your song</h2><ul class="song-list">` +
                data.songs.map(song => `
                    <li class="song-item">
                        <img src="${song.album_image}" alt="Art">
                        <div class="song-info">
                            <strong>${song.name}</strong><br>
                            <span>${song.artist}</span>
                        </div>
                        <button class="select-btn" onclick='getRecommendations(${JSON.stringify(song)})'>Pick this</button>
                    </li>
                `).join('') + `</ul>`;
        }
    } catch (error) {
        resultsDiv.textContent = 'An error occurred. Please try again.';
    }
};

async function getRecommendations(song) {
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<p>Getting recommendations...</p>';
    
    try {
        let response = await fetch('/recommend', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ song_id: song.id })
        });
        let data = await response.json();
        
        if (data.error) {
            resultsDiv.textContent = data.error;
        } else {
            resultsDiv.innerHTML = `
                <div class="song-block main-song">
                    <h2>Selected Song</h2>
                    <img src="${song.album_image}" alt="Art">
                    <h3>${song.name}</h3>
                    <p>${song.artist}</p>
                    <a href="${song.spotify_url}" target="_blank" class="spotify-link">Listen on Spotify</a>
                </div>
                <div class="recommendations-section">
                    <h3>Recommended Songs</h3>
                    <ul class="song-list">
                        ${data.recommendations.map(rec => `
                            <li class="song-item">
                                <img src="${rec.album_image}" alt="Art">
                                <div class="song-info">
                                    <strong>${rec.name}</strong><br>
                                    <span>${rec.artist}</span>
                                </div>
                                <a href="${rec.spotify_url}" target="_blank" class="spotify-btn">Open</a>
                            </li>
                        `).join('')}
                    </ul>
                    <button onclick="location.reload()" class="reset-btn">Search Again</button>
                </div>
            `;
        }
    } catch (error) {
        resultsDiv.textContent = 'An error occurred fetching recommendations.';
    }
}
