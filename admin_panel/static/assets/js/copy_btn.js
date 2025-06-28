
// Add this function to initialize copy buttons
function initializeCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(button => {
        // Remove existing event listener to prevent duplicates
        button.removeEventListener('click', copyButtonHandler);
        // Add new event listener
        button.addEventListener('click', copyButtonHandler);
    });
}

// Separate the handler function
async function copyButtonHandler(e) {
    e.stopPropagation(); // Prevent row click event
    const url = this.getAttribute('data-url');
    
    try {
        // Try modern clipboard API first
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(url);
            showToast('تم نسخ الرابط بنجاح');
        } else {
            // Fallback for older browsers and non-HTTPS contexts
            const textArea = document.createElement('textarea');
            textArea.value = url;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            try {
                document.execCommand('copy');
                textArea.remove();
                showToast('تم نسخ الرابط بنجاح');
            } catch (err) {
                textArea.remove();
                showToast('حدث خطأ أثناء نسخ الرابط - الرجاء النسخ يدوياً');
                showSelectableUrl(url);
            }
        }
    } catch (err) {
        showToast('حدث خطأ أثناء نسخ الرابط - الرجاء النسخ يدوياً');
        showSelectableUrl(url);
    }
}

// Call initializeCopyButtons when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeCopyButtons();
});

function clickHandler(event) {
    if (!event.target.closest('.checkbox-cell')) {
        window.location.href = event.currentTarget.getAttribute('data-link');
    }
}
