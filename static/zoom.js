let scale = 1;
window.addEventListener("wheel", function (event) {
  // Prevent the default scroll behavior
  if (event.ctrlKey) {
    event.preventDefault();

    // Zoom in or out based on the scroll direction
    if (event.deltaY < 0) {
      scale *= 1.1; // Zoom in
    } else {
      scale /= 1.1; // Zoom out
    }

    // Apply the scaling transformation
    document.body.style.transform = "scale(" + scale + ")";
    document.body.style.transformOrigin = "0 0"; // 设置缩放基准点为左上角
  }
});
