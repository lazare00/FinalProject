let searchTerm = document.getElementById("searchInput");
let searchButton = document.querySelector(".search-bar button");

searchButton.addEventListener("click", () => {
    window.location.href = "/search/" + searchTerm.value;
});
