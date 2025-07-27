# QuadtreeVision

**QuadtreeVision** is a Python-based image compression and edge detection tool that uses quadtree decomposition to efficiently analyze and simplify images. Built with OpenCV and NumPy, this project demonstrates spatial segmentation, color averaging, and adaptive pruning based on color variance and heuristics.

---

## Features

- **Quadtree Decomposition**: Recursively splits image regions based on size and color variance.
- **Adaptive Compression**: Simplifies regions with minimal color variation by averaging them.
- **Edge Detection**: Highlights boundaries where significant color differences exist.
- **Minimal Dependencies**: Requires only OpenCV and NumPy.
- **Supports Any Image** format readable by OpenCV.

---

## 🛠️ Installation

Make sure you have Python installed (3.7+ recommended). Then:

```bash
pip install opencv-python numpy
```
## Authors

- [Deishaun Colins](https://github.com/shaundcm)
- [M Deshna Shree](https://github.com/dsdeshna)
