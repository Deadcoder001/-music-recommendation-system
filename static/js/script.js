document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        let html = '';
        if (data.song) {
            html += `
                <div class="card mb-4">
                    <div class="card-body text-center">
                        <img src="${data.song.album_image}" alt="Album Image" class="album-image mb-3">
                        <div>
                            <h5 class="card-title">${data.song.name}</h5>
                            <p class="card-text">${data.song.artist}</p>
                        </div>
                        <div class="d-flex justify-content-start mt-6">
                            <a href="${data.song.spotify_url}" class="btn btn-primary mt-2" target="_blank">Listen on Spotify</a>
                        </div>
                    </div>
                </div>
            `;
            if (data.recommendations.length) {
                html += '<div class="recommendations"><h5>Recommendations</h5><div class="row">';
                data.recommendations.forEach(rec => {
                    html += `
                        <div class="col-12 col-sm-6 col-md-4 mb-4">
                            <div class="card">
                                <div class="card-body">
                                    <img src="${rec.album_image}" alt="Album Image" class="album-image">
                                    <div>
                                        <h6 class="card-title">${rec.name}</h6>
                                        <p class="card-text">${rec.artist}</p>
                                        <a href="${rec.spotify_url}" class="btn btn-secondary" target="_blank">Listen on Spotify</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                });
                html += '</div></div>';
            }
        } else {
            html = '<div class="alert alert-danger" role="alert">No song found</div>';
        }
        document.getElementById('results').innerHTML = html;
    });
});
