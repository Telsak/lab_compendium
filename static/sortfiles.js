document.getElementById('file-input').addEventListener('change', function(e) {
    var fileList = document.getElementById('file-list');
    fileList.innerHTML = '';
    for (var i = 0; i < this.files.length; i++) {
        var li = document.createElement('li');
        li.innerHTML = "<span class='order-number'></span> " + this.files[i].name;
        fileList.appendChild(li);
    }

    var sortable = new Sortable(fileList, {
        animation: 150,
        ghostClass: 'blue-background-class',
        onEnd: updateOrderNumbers
    });

    updateOrderNumbers(); // Initial numbering
});

function updateOrderNumbers() {
    var listItems = document.querySelectorAll('#file-list li');
    listItems.forEach(function(item, index) {
        var orderNumber = index + 1;
        item.querySelector('.order-number').textContent = orderNumber + '.';
    });
}

document.getElementById('reverse-order').addEventListener('click', function() {
    var fileList = document.getElementById('file-list');
    var items = Array.from(fileList.querySelectorAll('li'));
    for (var i = items.length - 1; i >= 0; i--) {
        fileList.appendChild(items[i]); // Re-append each item in reverse order
    }

    updateOrderNumbers(); // Update the order numbers after reversing
});

document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();

    var fileList = document.getElementById('file-list');
    var formData = new FormData();

    document.getElementById('spinner').style.display = 'block';

    fileList.querySelectorAll('li').forEach(function(item, index) {
        var orderNumber = (index + 1).toString().padStart(3, '0'); // Create a 3-digit order number
        var originalFileName = item.textContent.split('.').slice(1).join('.').trim();
        var fileExtension = originalFileName.split('.').pop();
        var newFileName = orderNumber + '_' + originalFileName;

        // Find the file in the original FileList and append it with the new name
        Array.from(document.getElementById('file-input').files).forEach(function(file) {
            if (file.name === originalFileName) {
                formData.append('files', file, newFileName);
            }
        });
    });

    // Send the FormData with AJAX
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.success_url) {
            document.getElementById('spinner').style.display = 'none';
            window.location.href = data.success_url;
        }
    })
    .catch(error => console.error('Error:', error));
});
