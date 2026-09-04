// ========================================
// COMPETENCYIQ - INTERACTIONS
// ========================================

// Start Assessment
function startAssessment() {
    alert(
        "Welcome to CompetencyIQ! 🧠\n\nYour assessment module is ready to be connected."
    );
}


// Explore Platform
function learnMore() {
    document
        .getElementById("features")
        .scrollIntoView({
            behavior: "smooth"
        });
}


// Navigation links
document.querySelectorAll(".nav-links a").forEach(function (link) {

    link.addEventListener("click", function (event) {

        const target = document.querySelector(
            link.getAttribute("href")
        );

        if (target) {

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth"
            });
        }

    });

});