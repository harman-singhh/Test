// ==========================================================
// CodeCraft Academy - Dashboard JavaScript
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {

    // ---------- Sidebar toggle (mobile) ----------
    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", function () {
            sidebar.classList.toggle("active");
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

    // ---------- Delete confirmation ----------
    document.querySelectorAll(".confirm-delete").forEach(function (link) {
        link.addEventListener("click", function (e) {
            const label = link.getAttribute("data-label") || "this item";
            if (!confirm("Are you sure you want to delete " + label + "? This cannot be undone.")) {
                e.preventDefault();
            }
        });
    });

    // ---------- Auto-submit booking status change ----------
    document.querySelectorAll(".status-select").forEach(function (select) {
        select.addEventListener("change", function () {
            select.closest("form").submit();
        });
    });

    // ---------- Image preview on add/edit forms ----------
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

    // ---------- Simple required-field validation for dashboard forms ----------
    document.querySelectorAll("form[data-validate='true']").forEach(function (form) {
        form.addEventListener("submit", function (e) {
            let valid = true;
            form.querySelectorAll("[required]").forEach(function (field) {
                if (!field.value || !field.value.trim()) {
                    valid = false;
                    field.style.borderColor = "#dc2626";
                } else {
                    field.style.borderColor = "#e2e8f0";
                }
            });
            if (!valid) {
                e.preventDefault();
                alert("Please fill in all required fields.");
            }
        });
    });
});
