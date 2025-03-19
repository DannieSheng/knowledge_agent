document.addEventListener("DOMContentLoaded", function() {
    fetchNews();
});

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
                    <p><strong>Summary:</strong> ${news.summary || "No summary available"}</p>
                    <small>Published on: ${news.published}</small>
                    <hr>
                `;
                newsContainer.appendChild(item);
            });
        })
        .catch(error => console.error("Error fetching news:", error));
}