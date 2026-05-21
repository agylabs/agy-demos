document.addEventListener("DOMContentLoaded", () => {
    const shortenForm = document.getElementById("shorten-form");
    const originalUrlInput = document.getElementById("original_url");
    const customAliasInput = document.getElementById("custom_alias");
    const expiresInSelect = document.getElementById("expires_in_minutes");
    const submitBtn = document.getElementById("submit-btn");
    const btnText = submitBtn.querySelector(".btn-text");
    const btnLoader = submitBtn.querySelector(".btn-loader");
    const linksTbody = document.getElementById("links-tbody");
    const refreshBtn = document.getElementById("refresh-btn");

    // Modal elements
    const qrModal = document.getElementById("qr-modal");
    const qrUrlDisplay = document.getElementById("qr-url-display");
    const qrCloseBtn = document.getElementById("close-modal-btn");
    const downloadQrBtn = document.getElementById("download-qr-btn");

    // Load initial listings
    fetchUrls();

    // Event listener for Refresh
    refreshBtn.addEventListener("click", fetchUrls);

    // Event listener for shortening form submission
    shortenForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const originalUrl = originalUrlInput.value.trim();
        const customAlias = customAliasInput.value.trim() || null;
        const expiresInMinutes = expiresInSelect.value ? parseInt(expiresInSelect.value) : null;

        // Set Loading state
        submitBtn.disabled = true;
        btnText.textContent = "Shortening...";
        btnLoader.classList.remove("hidden");

        try {
            const response = await fetch("/api/shorten", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    original_url: originalUrl,
                    custom_alias: customAlias,
                    expires_in_minutes: expiresInMinutes
                })
            });

            const data = await response.json();

            if (!response.ok) {
                // If it's a validation error, extract detail
                const errMsg = data.detail || "Failed to shorten URL.";
                showToast(errMsg, "error");
            } else {
                showToast("Link shortened successfully!", "success");
                
                // Clear input fields
                originalUrlInput.value = "";
                customAliasInput.value = "";
                expiresInSelect.value = "";

                // Refresh URL table
                await fetchUrls();
            }
        } catch (error) {
            console.error("Error creating short URL:", error);
            showToast("Network error. Please try again.", "error");
        } finally {
            // Restore Loading state
            submitBtn.disabled = false;
            btnText.textContent = "Shorten Link";
            btnLoader.classList.add("hidden");
        }
    });

    // Event listeners to close QR modal
    qrCloseBtn.addEventListener("click", () => {
        qrModal.classList.remove("active");
    });
    qrModal.querySelector(".modal-backdrop").addEventListener("click", () => {
        qrModal.classList.remove("active");
    });

    // Download QR Code Action
    downloadQrBtn.addEventListener("click", () => {
        const img = document.querySelector("#qrcode img");
        const canvas = document.querySelector("#qrcode canvas");
        let url = "";

        if (img && img.src) {
            url = img.src;
        } else if (canvas) {
            url = canvas.toDataURL("image/png");
        }

        if (url) {
            const a = document.createElement("a");
            a.href = url;
            a.download = "ziplink_qrcode.png";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            showToast("QR code downloaded!", "success");
        } else {
            showToast("Could not export QR code image.", "error");
        }
    });

    // Fetch and populate links table
    async function fetchUrls() {
        try {
            const response = await fetch("/api/urls");
            if (!response.ok) throw new Error("Could not retrieve links.");
            const urls = await response.json();

            linksTbody.innerHTML = "";

            if (urls.length === 0) {
                linksTbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="table-empty">No active shortened links. Enter a URL above to create your first link!</td>
                    </tr>
                `;
                return;
            }

            urls.forEach((url) => {
                const tr = document.createElement("tr");

                // Short link column
                const shortUrlCell = document.createElement("td");
                const shortLink = document.createElement("a");
                shortLink.href = url.short_url;
                shortLink.target = "_blank";
                shortLink.className = "short-url-link";
                shortLink.textContent = url.short_url;
                shortUrlCell.appendChild(shortLink);

                // Destination column
                const destCell = document.createElement("td");
                destCell.className = "dest-url-cell";
                destCell.title = url.original_url;
                destCell.textContent = url.original_url;

                // Clicks column
                const clicksCell = document.createElement("td");
                const clicksBadge = document.createElement("span");
                clicksBadge.className = "clicks-badge";
                clicksBadge.textContent = url.clicks;
                clicksCell.appendChild(clicksBadge);

                // Last Accessed column
                const lastCell = document.createElement("td");
                lastCell.className = "time-cell";
                lastCell.textContent = url.last_clicked_at 
                    ? formatTimestamp(url.last_clicked_at) 
                    : "Never";

                // Expiration column
                const expiryCell = document.createElement("td");
                const expiryBadge = document.createElement("span");
                
                if (url.expires_at) {
                    const expiryDate = new Date(url.expires_at);
                    const now = new Date();
                    if (now > expiryDate) {
                        expiryBadge.className = "expiry-badge expiry-expired";
                        expiryBadge.textContent = "Expired";
                    } else {
                        expiryBadge.className = "expiry-badge expiry-active";
                        expiryBadge.textContent = formatTimestamp(url.expires_at);
                    }
                } else {
                    expiryBadge.className = "expiry-badge expiry-never";
                    expiryBadge.textContent = "Never";
                }
                expiryCell.appendChild(expiryBadge);

                // Actions column
                const actionsCell = document.createElement("td");
                actionsCell.className = "row-actions";

                // Copy button
                const copyBtn = document.createElement("button");
                copyBtn.className = "btn-row-action";
                copyBtn.title = "Copy short URL";
                copyBtn.innerHTML = "📋";
                copyBtn.addEventListener("click", () => {
                    navigator.clipboard.writeText(url.short_url);
                    showToast("Link copied to clipboard!", "success");
                });

                // QR button
                const qrBtn = document.createElement("button");
                qrBtn.className = "btn-row-action";
                qrBtn.title = "Show QR code";
                qrBtn.innerHTML = "📱";
                qrBtn.addEventListener("click", () => {
                    openQRModal(url.short_url);
                });

                // Delete button
                const deleteBtn = document.createElement("button");
                deleteBtn.className = "btn-row-action btn-row-action-delete";
                deleteBtn.title = "Delete short URL";
                deleteBtn.innerHTML = "🗑️";
                deleteBtn.addEventListener("click", async () => {
                    if (confirm(`Are you sure you want to delete /${url.short_code}?`)) {
                        try {
                            const delResponse = await fetch(`/api/urls/${url.short_code}`, {
                                method: "DELETE"
                            });
                            if (delResponse.ok) {
                                showToast("Link deleted successfully.", "success");
                                fetchUrls();
                            } else {
                                showToast("Failed to delete link.", "error");
                            }
                        } catch (err) {
                            showToast("Error deleting link.", "error");
                        }
                    }
                });

                actionsCell.appendChild(copyBtn);
                actionsCell.appendChild(qrBtn);
                actionsCell.appendChild(deleteBtn);

                tr.appendChild(shortUrlCell);
                tr.appendChild(destCell);
                tr.appendChild(clicksCell);
                tr.appendChild(lastCell);
                tr.appendChild(expiryCell);
                tr.appendChild(actionsCell);

                linksTbody.appendChild(tr);
            });
        } catch (error) {
            console.error("Error fetching URL directory:", error);
            linksTbody.innerHTML = `
                <tr>
                    <td colspan="6" class="table-empty text-danger">⚠️ Error loading links. Please make sure the backend is active.</td>
                </tr>
            `;
        }
    }

    // Function to launch the QR code modal
    function openQRModal(url) {
        qrUrlDisplay.textContent = url;
        const qrcodeDiv = document.getElementById("qrcode");
        qrcodeDiv.innerHTML = ""; // Clean previous canvases

        // Instantiate David Shim's QRCode Generator (client-side)
        new QRCode(qrcodeDiv, {
            text: url,
            width: 180,
            height: 180,
            colorDark: "#070a13",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H
        });

        qrModal.classList.add("active");
    }

    // Modern toast notification system
    function showToast(message, type = "success") {
        const toastContainer = document.getElementById("toast-container");
        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;

        const icon = document.createElement("span");
        icon.className = "toast-icon";
        icon.textContent = type === "success" ? "✨" : "⚠️";

        const msgSpan = document.createElement("span");
        msgSpan.className = "toast-message";
        msgSpan.textContent = message;

        toast.appendChild(icon);
        toast.appendChild(msgSpan);
        toastContainer.appendChild(toast);

        // Slide away and delete toast after 4s
        setTimeout(() => {
            toast.style.animation = "slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1) reverse forwards";
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3700);
    }

    // Formatter for ISO timestamps
    function formatTimestamp(isoString) {
        if (!isoString) return "Never";
        // Parse ISO UTC string manually or directly via Date
        const d = new Date(isoString);
        return d.toLocaleString(undefined, {
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        });
    }
});
