self.onmessage = (event) => {
  const { imageBitmap, width, height } = event.data;

  try {
    // Now we CAN use canvas in worker via OffscreenCanvas
    const offscreen = new OffscreenCanvas(width, height);
    const ctx = offscreen.getContext('2d');

    ctx.drawImage(imageBitmap, 0, 0);
    const imageData = ctx.getImageData(0, 0, width, height);

    self.postMessage(
      { success: true, imageData },
      [imageData.data.buffer]
    );
  } catch (err) {
    self.postMessage({ success: false, error: err.message });
  }
};