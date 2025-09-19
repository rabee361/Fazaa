class VideoUploader {
    constructor(container) {
        this.container = container;
        this.fileInput = container.querySelector('input[type="file"]');
        this.uploadContent = container.querySelector('.video-upload-content');
        this.progressContainer = container.querySelector('.upload-progress');
        this.progressFill = container.querySelector('.progress-fill');
        this.progressText = container.querySelector('.progress-text');
        this.previewContainer = container.querySelector('.video-preview');
        
        this.init();
    }

    init() {
        // Set up event listeners
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.container.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.container.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.container.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Check if there's an existing video (for update forms)
        this.checkExistingVideo();
    }

    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        this.container.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        this.container.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        this.container.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    processFile(file) {
        // Validate file type
        if (!this.isValidVideoFile(file)) {
            this.showError('يرجى اختيار ملف فيديو صالح (MP4, AVI, MOV, WMV)');
            return;
        }

        // Validate file size (50MB limit)
        if (file.size > 50 * 1024 * 1024) {
            this.showError('حجم الملف كبير جداً. يرجى اختيار ملف أصغر من 50 ميجابايت');
            return;
        }

        this.clearError();
        this.hideUploadContent();
        this.simulateUpload(file);
    }

    isValidVideoFile(file) {
        const validTypes = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-msvideo', 'video/x-ms-wmv'];
        return validTypes.includes(file.type) || /\.(mp4|avi|mov|wmv)$/i.test(file.name);
    }

    simulateUpload(file) {
        this.showProgress();
        this.container.classList.add('loading');
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                setTimeout(() => {
                    this.uploadComplete(file);
                }, 500);
            }
            this.updateProgress(progress);
        }, 200);
    }

    uploadComplete(file) {
        this.hideProgress();
        this.container.classList.remove('loading');
        this.showVideoPreview(file);
    }

    showVideoPreview(file) {
        const videoUrl = URL.createObjectURL(file);
        
        this.previewContainer.innerHTML = `
            <div class="video-preview-container">
                <video controls preload="metadata">
                    <source src="${videoUrl}" type="${file.type}">
                    المتصفح لا يدعم تشغيل الفيديو
                </video>
            </div>
            <div class="video-info">
                <div class="video-name">${file.name}</div>
                <div class="video-size">${this.formatFileSize(file.size)}</div>
            </div>
            <div class="video-actions">
                <button type="button" class="video-action-btn" onclick="this.closest('.video-uploader').videoUploader.changeVideo()">تغيير</button>
                <button type="button" class="video-action-btn remove" onclick="this.closest('.video-uploader').videoUploader.removeVideo()">حذف</button>
            </div>
        `;
        
        this.showPreview();
        this.container.classList.add('video-uploader-active');
    }

    checkExistingVideo() {
        // Check if there's a value in the file input (for update forms)
        const existingVideoUrl = this.fileInput.getAttribute('data-current-video');
        const existingVideoName = this.fileInput.getAttribute('data-current-name');
        if (existingVideoUrl) {
            this.showExistingVideo(existingVideoUrl, existingVideoName);
        }
    }

    showExistingVideo(videoUrl, videoName = null) {
        const fileName = videoName || videoUrl.split('/').pop() || 'فيديو حالي';
        
        this.previewContainer.innerHTML = `
            <div class="video-preview-container">
                <video controls preload="metadata">
                    <source src="${videoUrl}" type="video/mp4">
                    المتصفح لا يدعم تشغيل الفيديو
                </video>
            </div>
            <div class="video-info">
                <div class="video-name">${fileName}</div>
                <div class="video-size">ملف محفوظ</div>
            </div>
            <div class="video-actions">
                <button type="button" class="video-action-btn" onclick="this.closest('.video-uploader').videoUploader.changeVideo()">تغيير</button>
                <button type="button" class="video-action-btn remove" onclick="this.closest('.video-uploader').videoUploader.removeVideo()">حذف</button>
            </div>
        `;
        
        this.showPreview();
        this.hideUploadContent();
        this.container.classList.add('video-uploader-active');
    }

    changeVideo() {
        this.fileInput.click();
    }

    removeVideo() {
        this.fileInput.value = '';
        this.hidePreview();
        this.showUploadContent();
        this.container.classList.remove('video-uploader-active');
        this.clearError();
    }

    showProgress() {
        this.progressContainer.style.display = 'block';
    }

    hideProgress() {
        this.progressContainer.style.display = 'none';
    }

    updateProgress(percentage) {
        this.progressFill.style.width = percentage + '%';
        this.progressText.textContent = `جاري الرفع... ${Math.round(percentage)}%`;
    }

    showPreview() {
        this.previewContainer.style.display = 'block';
    }

    hidePreview() {
        this.previewContainer.style.display = 'none';
    }

    showUploadContent() {
        this.uploadContent.style.display = 'block';
    }

    hideUploadContent() {
        this.uploadContent.style.display = 'none';
    }

    showError(message) {
        this.container.classList.add('error');
        let errorDiv = this.container.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            this.container.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }

    clearError() {
        this.container.classList.remove('error');
        const errorDiv = this.container.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 بايت';
        
        const k = 1024;
        const sizes = ['بايت', 'كيلوبايت', 'ميجابايت', 'جيجابايت'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Initialize video uploaders when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const videoUploaders = document.querySelectorAll('.video-uploader');
    videoUploaders.forEach(container => {
        container.videoUploader = new VideoUploader(container);
    });
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VideoUploader;
}