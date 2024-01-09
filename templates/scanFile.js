document.addEventListener('DOMContentLoaded', function () {
    const takePictureButton = document.getElementById('takePictureButton');
    const cropperContainer = document.getElementById('cropperContainer');
    const cropButton = document.getElementById('cropButton');
    const imageContainer = document.getElementById('imageContainer');
    const cropperImage = document.getElementById('cropperImage');
    const croppedResult = document.getElementById('croppedResult');
    let cropper;

    takePictureButton.addEventListener('click', async function () {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            const video = document.createElement('video');
            cropperContainer.appendChild(video);
            video.srcObject = stream;
            video.play();

            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            video.addEventListener('loadedmetadata', function () {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
            });

            cropButton.style.display = 'block';

            cropButton.addEventListener('click', function () {
                const imageData = takeSnapshot(context, video, canvas);
                cropperContainer.removeChild(video);
                cropperImage.src = imageData;
                cropper = new Cropper(cropperImage, {
                    aspectRatio: 1 / 1, // Set aspect ratio as needed
                    crop(event) {
                        // Handle crop events if needed
                    },
                });
                cropperContainer.style.display = 'block';
            });
        } catch (err) {
            console.error('Error accessing camera:', err);
        }
    });

    function takeSnapshot(context, video, canvas) {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/png');
        return imageData;
    }

    // Example to get cropped result
    // You can use this on a button click or in any event handler where you need the cropped image
    // For example, you can trigger this function when a "Save" button is clicked
    function getCroppedResult() {
        const croppedImageData = cropper.getCroppedCanvas().toDataURL('image/png');
        croppedResult.src = croppedImageData;
        imageContainer.style.display = 'block';
    }
});