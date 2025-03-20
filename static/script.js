let currentPage = 1;  // Default to the first page

document.addEventListener("DOMContentLoaded", function() {
    // Fetch and update the homepage news
    if (document.getElementById("news-list")) {
        fetchNews();
    }
    
    // Fetch and update the archive page news
    if (document.getElementById("archive-list")) {
        fetchArchiveNews(currentPage);
    }

    // Set today's date in the homepage
    if (document.getElementById("today-date")) {
        const today = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        document.getElementById("today-date").innerText = today;
    }
});

// Fetch current news for the homepage
function fetchNews() {
    fetch('/api/news')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched news:", data);  // ✅ Debugging line
            let newsContainer = document.getElementById("news-list");
            newsContainer.innerHTML = "";  // Clear old content

            data.forEach(news => {
                let item = document.createElement("div");
                item.classList.add("news-item");
                item.innerHTML = `
                    <h2><a href="${news.link}" target="_blank">${news.title}</a></h2>
                    <p><strong>Categories:</strong> ${news.categories ? news.categories.join(", ") : "N/A"}</p>
                    <p><strong>Summary:</strong> ${news.summary_en || "No summary available"}</p>
                    <p><strong>摘要:</strong> ${news.summary_zh || "暂无摘要"}</p>
                    <small>Published on: ${news.published}</small>
                    <div>
                        <button class="like-btn" onclick="likeNews(news.id)">👍</button>
                        <button class="dislike-btn" onclick="dislikeNews(news.id)">👎</button>
                    </div>
                    <hr>
                `;
                newsContainer.appendChild(item);
            });
        })
        .catch(error => console.error("Error fetching news:", error));
}

// Fetch archived news for the archive page
function fetchArchiveNews(page) {
    fetch(`/api/archive?page=${page}`)
        .then(response => response.json())
        .then(data => {
            let archiveContainer = document.getElementById("archive-list");
            archiveContainer.innerHTML = "";  // Clear any existing content
            if (data.length === 0) {
                archiveContainer.innerHTML = "<p>No archived news available.</p>";
                return;
            }
            data.forEach(news => {
                let item = document.createElement("div");
                item.classList.add("news-item");
                item.innerHTML = `
                    <h2><a href="${news.link}" target="_blank">${news.title}</a></h2>
                    <p><strong>Categories:</strong> ${news.categories ? news.categories.join(", ") : "N/A"}</p>
                    <p><strong>Summary:</strong> ${news.summary_en || "No summary available"}</p>
                    <p><strong>摘要:</strong> ${news.summary_zh || "暂无摘要"}</p>
                    <small>Published on: ${news.published}</small>
                    <hr>
                `;
                archiveContainer.appendChild(item);
            });
            // Update pagination controls based on the current page
            updatePaginationControls();
        })
        .catch(error => console.error("Error fetching archive news:", error));
}

function likeNews(newsId) {
    fetch(`/like/${newsId}`, { method: 'POST' });
}

function dislikeNews(newsId) {
    fetch(`/dislike/${newsId}`, { method: 'POST' });
}


// Change page when clicking "Previous" or "Next"
function changePage(direction) {
    if (direction === "next") {
        currentPage += 1;
    } else if (direction === "prev" && currentPage > 1) {
        currentPage -= 1;
    }

    fetchArchiveNews(currentPage);
}

// Update the visibility of pagination buttons based on current page
function updatePaginationControls() {
    // Disable "Previous" button on the first page
    document.getElementById("prev-page").disabled = currentPage === 1;

    // Disable "Next" button if there are no more pages (you can add logic here to check if more pages exist)
    // For now, we assume there are always more pages to go to, but you can enhance it
    document.getElementById("next-page").disabled = false;  // You can set this dynamically later
}