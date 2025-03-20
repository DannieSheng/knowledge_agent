document.addEventListener("DOMContentLoaded", function() {
    // Fetch and update the homepage news
    if (document.getElementById("news-list")) {
        fetchNews();
    }
    
    // Fetch and update the archive page news
    if (document.getElementById("archive-list")) {
        fetchArchiveNews();
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
                    <p><strong>Summary:</strong> ${news.summary_zh || "暂无摘要"}</p>
                    <small>Published on: ${news.published}</small>
                    <hr>
                `;
                newsContainer.appendChild(item);
            });
        })
        .catch(error => console.error("Error fetching news:", error));
}

// Fetch archived news for the archive page
function fetchArchiveNews() {
    fetch('/api/archive')
        .then(response => response.json())
        .then(data => {
            let archiveContainer = document.getElementById("archive-list");
            archiveContainer.innerHTML = "";  // Clear any existing content
            if (data.length === 0) {
                archiveContainer.innerHTML = "<p>No archived news available.</p>";
            }
            data.forEach(news => {
                let item = document.createElement("div");
                item.classList.add("news-item");
                item.innerHTML = `
                    <h2><a href="${news.link}" target="_blank">${news.title}</a></h2>
                    <p><strong>Categories:</strong> ${news.categories ? news.categories.join(", ") : "N/A"}</p>
                    <p><strong>Summary:</strong> ${news.summary_en || "No summary available"}</p>
                    <p><strong>Summary:</strong> ${news.summary_zh || "暂无摘要"}</p>
                    <small>Published on: ${news.published}</small>
                    <hr>
                `;
                archiveContainer.appendChild(item);
            });
        })
        .catch(error => console.error("Error fetching archive news:", error));
}