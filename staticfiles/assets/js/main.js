document.addEventListener('DOMContentLoaded', function() {
    const selectAllCheckbox = document.getElementById('selectAll');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    const deleteForm = document.getElementById('deleteForm');
    const deleteBtn = document.getElementById('deleteBtn');
    const selectedIdsInput = document.getElementById('selectedIds');

    selectAllCheckbox.addEventListener('change', function() {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const allChecked = Array.from(rowCheckboxes).every(cb => cb.checked);
            selectAllCheckbox.checked = allChecked;
        });
    });

    deleteForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
        
        if (selectedCheckboxes.length === 0) {
            alert('الرجاء تحديد عنصر واحد على الأقل للحذف');
            return;
        }

        if (confirm('هل أنت متأكد من حذف العناصر المحددة؟')) {
            const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
            selectedIdsInput.value = JSON.stringify(selectedIds);
            this.submit();
        }
    });
});

// Sidebar toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');

    function toggleSidebar() {
        sidebar.classList.toggle('hidden');
        overlay.classList.toggle('show');
    }

    function closeSidebar() {
        sidebar.classList.add('hidden');
        overlay.classList.remove('show');
    }

    // Toggle sidebar when clicking the hamburger button
    sidebarToggle?.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleSidebar();
    });

    // Close sidebar when clicking overlay
    overlay?.addEventListener('click', function() {
        closeSidebar();
    });

    // Close sidebar when clicking outside
    document.addEventListener('click', function(e) {
        if (!sidebar.contains(e.target) && 
            !sidebarToggle.contains(e.target) && 
            !sidebar.classList.contains('hidden')) {
            closeSidebar();
        }
    });

    // Prevent clicks inside sidebar from closing it
    sidebar?.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});

function clickHandler(event) {
    if (!event.target.closest('.checkbox-cell')) {
        window.location.href = event.currentTarget.getAttribute('data-link');
    }
}