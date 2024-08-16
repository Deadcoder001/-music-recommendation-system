document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const query = document.getElementById('query').value;
    fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ 'query': query })
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';
        
        if (data.error) {
            resultsDiv.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        const song = data.song;
        resultsDiv.innerHTML += `
            <div class="song">
                <h2>${song.name}</h2>
                <p>Artist: ${song.artist}</p>
                <img src="${song.album_image}" alt="${song.name} album art" style="width: 200px;">
                <a href="${song.spotify_url}" target="_blank">Listen on Spotify</a>
            </div>
        `;

        resultsDiv.innerHTML += '<h3>Recommended Songs:</h3>';
        data.recommendations.forEach(rec => {
            resultsDiv.innerHTML += `
                <div class="song">
                    <h4>${rec.name}</h4>
                    <p>Artist: ${rec.artist}</p>
                    <img src="${rec.album_image}" alt="${rec.name} album art" style="width: 150px;">
                    <a href="${rec.spotify_url}" target="_blank">Listen on Spotify</a>
                </div>
            `;
        });
    });
});
