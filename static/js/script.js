// ==========================================================
// CodeCraft Academy - Main Site JavaScript
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {

    // ---------- Navbar toggle (mobile) ----------
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");

    if (navToggle && navLinks) {
        navToggle.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });

        document.querySelectorAll(".nav-links a").forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("active");
            });
        });
    }

    // ---------- Auto-hide flash messages ----------
    document.querySelectorAll(".alert").forEach(function (alertEl) {
        setTimeout(function () {
            alertEl.style.transition = "opacity 0.5s ease";
            alertEl.style.opacity = "0";
            setTimeout(function () { alertEl.remove(); }, 500);
        }, 5000);
    });

    // ---------- Scroll reveal animation (desktop only to prevent mobile blank screens) ----------
    const revealItems = document.querySelectorAll(".card, .course-card, .testimonial-card, .tutor-card");
    if ("IntersectionObserver" in window && window.innerWidth > 768) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = "1";
                    entry.target.style.transform = "translateY(0)";
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.05 });

        revealItems.forEach(function (item) {
            item.style.opacity = "0";
            item.style.transform = "translateY(24px)";
            item.style.transition = "opacity 0.6s ease, transform 0.6s ease";
            observer.observe(item);
        });
    } else {
        revealItems.forEach(function (item) {
            item.style.opacity = "1";
            item.style.transform = "none";
        });
    }

    // ---------- Image preview (course/tutor/testimonial forms) ----------
    document.querySelectorAll("input[type='file']").forEach(function (input) {
        input.addEventListener("change", function () {
            const previewId = input.getAttribute("data-preview");
            if (!previewId) return;
            const preview = document.getElementById(previewId);
            const file = input.files[0];

            if (file) {
                const validTypes = ["image/png", "image/jpeg", "image/jpg"];
                if (!validTypes.includes(file.type)) {
                    alert("Only PNG, JPG, JPEG images are allowed.");
                    input.value = "";
                    return;
                }
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.style.display = "flex";
                    preview.innerHTML = "<img src='" + e.target.result + "' alt='preview'>";
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // ---------- Contact form validation ----------
    const contactForm = document.getElementById("contactForm");
    if (contactForm) {
        contactForm.addEventListener("submit", function (e) {
            let valid = true;
            valid = validateField("name", v => v.trim().length >= 2, "Please enter your full name.") && valid;
            valid = validateField("email", v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), "Please enter a valid email address.") && valid;
            valid = validateField("message", v => v.trim().length >= 10, "Message must be at least 10 characters.") && valid;

            if (!valid) e.preventDefault();
        });
    }

    // ---------- Booking form validation ----------
    const bookingForm = document.getElementById("bookingForm");
    if (bookingForm) {
        bookingForm.addEventListener("submit", function (e) {
            let valid = true;
            valid = validateField("student_name", v => v.trim().length >= 2, "Please enter your full name.") && valid;
            valid = validateField("email", v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), "Please enter a valid email address.") && valid;
            if (!valid) e.preventDefault();
        });
    }

    // ---------- Login form validation ----------
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            let valid = true;
            valid = validateField("email", v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), "Please enter a valid email address.") && valid;
            valid = validateField("password", v => v.length >= 4, "Password must be at least 4 characters.") && valid;
            if (!valid) e.preventDefault();
        });
    }

    function validateField(name, testFn, errorMsg) {
        const field = document.querySelector(`[name="${name}"]`);
        if (!field) return true;
        const errorEl = document.getElementById(name + "Error");
        const ok = testFn(field.value);

        if (!ok) {
            field.style.borderColor = "#dc2626";
            if (errorEl) { errorEl.textContent = errorMsg; errorEl.style.display = "block"; }
        } else {
            field.style.borderColor = "#e2e8f0";
            if (errorEl) errorEl.style.display = "none";
        }
        return ok;
    }

    // ---------- Rating stars display on public pages ----------
    document.querySelectorAll(".rating-input").forEach(function (input) {
        input.addEventListener("input", function () {
            const label = document.getElementById(input.id + "Label");
            if (label) label.textContent = "★".repeat(input.value) + "☆".repeat(5 - input.value);
        });
    });
});
