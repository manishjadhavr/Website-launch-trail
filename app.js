lucide.createIcons();

document.addEventListener("DOMContentLoaded", () => {
    const reveals = document.querySelectorAll(".reveal");

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
                revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    });

    reveals.forEach(reveal => {
        revealObserver.observe(reveal);
    });

    const navbar = document.getElementById("navbar");
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            navbar.classList.add("shadow-sm");
        } else {
            navbar.classList.remove("shadow-sm");
        }
    });

    const form = document.getElementById("rfq-form");
    const successMsg = document.getElementById("form-success");

    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            btn.textContent = "Submitting...";
            btn.disabled = true;

            setTimeout(() => {
                btn.textContent = "Submit RFQ";
                btn.disabled = false;
                form.reset();
                successMsg.classList.remove("hidden");
                setTimeout(() => {
                    successMsg.classList.add("hidden");
                }, 5000);
            }, 1000);
        });
    }
});
