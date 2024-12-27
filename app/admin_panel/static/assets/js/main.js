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


function clickHandler(event) {
    if (!event.target.closest('.checkbox-cell')) {
        window.location.href = event.currentTarget.getAttribute('data-link');
    }
}