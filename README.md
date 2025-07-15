# 🌌 AstroGPT

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white" alt="Selenium">
  <br>
  <img src="https://img.shields.io/github/license/TheBheta/AstroGPT?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/TheBheta/AstroGPT?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/forks/TheBheta/AstroGPT?style=flat-square" alt="Forks">
</div>

> **An intelligent astronomical image search engine that uses computer vision to find similar deep space objects based on uploaded images, originally developed to help our team practice for the 2024 Science Olympiad Astronomy competition.**

## ✨ Features

- 🔍 **Image-based Search**: Upload any astronomical image of  and find similar deep space objects
- 🎯 **Computer Vision Matching**: Uses ORB (Oriented FAST and Rotated BRIEF) feature detection for accurate image matching
- 📊 **Comprehensive Database**: Includes images of nebulae, exoplanets, star systems, and other celestial objects
- 🌐 **Web Interface**: Beautiful, responsive Flask web application
- 📄 **Research Papers**: Automated scraping and storage of scientific papers related to astronomical objects
- 📈 **Visual Analytics**: Graph generation and analysis tools for astronomical data

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Chrome browser (for web scraping functionality)
- ChromeDriver (included in the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/TheBheta/AstroGPT.git
   cd AstroGPT
   ```

2. **Install dependencies**
   ```bash
   pip install flask opencv-python numpy matplotlib selenium beautifulsoup4 requests spire.pdf
   ```

3. **Run the application**
   ```bash
   python server.py
   ```

4. **Access the web interface**
   Open your browser and navigate to `http://localhost:5000`

## 🔧 How It Works

### Image Matching Algorithm

AstroGPT uses advanced computer vision techniques to match uploaded images with its database:

1. **Feature Detection**: Uses ORB (Oriented FAST and Rotated BRIEF) to detect keypoints and descriptors
2. **Feature Matching**: Employs Brute Force Matcher with Hamming distance for descriptor matching
3. **Ranking**: Sorts matches by distance to find the most similar images
4. **Results**: Returns top 10 most similar astronomical objects

### Database Structure

The system organizes astronomical data into categories:

- **Images**: High-quality images of deep space objects
- **Papers**: Scientific research papers related to each object
- **Graphs**: Generated visualizations and analysis charts
- **Pages**: HTML pages with detailed information about each object

### Supported Astronomical Objects

- **Nebulae**: Carina Nebula, NGC 1333, HH 7-11
- **Exoplanets**: WASP-18b, WASP-39b, WASP-43b, V830 Tau b, V 1298 Tau b
- **Star Systems**: HR 8799, Beta Pictoris, TW Hya, AB Aurigae, HD 169142
- **Brown Dwarfs**: 2M 1207, Luhman 16
- **Star-Forming Regions**: TRAPPIST-1

**Complete List of Objects**:
Carina Nebula, NGC 1333, TW Hya, HH 7-11, AB Aurigae, HD 169142, Luhman 16, V830 Tau b, V 1298 Tau b, WASP-18b, WASP-39b, WASP-43b, HR 8799, Beta Pictoris, 2M 1207, TRAPPIST-1

## 📁 Project Structure

```
AstroGPT/
├── 📄 server.py              # Flask web application
├── 🔍 findImage.py           # Image matching algorithm
├── 🌐 imageScraper.py        # Web scraping for images
├── 📊 paperScraper.py        # Research paper scraping
├── 🗄️ dbsetup.py            # Database initialization
├── 🎨 templates/             # HTML templates
├── 📁 static/               # Static assets
│   ├── 🖼️ images/           # Astronomical object images
│   ├── 📄 papers/           # Research papers
│   ├── 📊 graphs/           # Generated visualizations
│   └── 🔍 queryimages/      # User uploaded images
└── 📊 mydb.sqlite           # SQLite database
```

## 🎯 Usage

1. **Upload an Image**: Visit the web interface and upload an astronomical image
2. **Wait for Processing**: The system will analyze your image using computer vision
3. **View Results**: Browse through similar objects found in the database
4. **Explore Details**: Click on results to view research papers and additional information

## 🔬 Technical Details

### Computer Vision Pipeline

```python
# Feature detection and matching
orb = cv.ORB_create()
kp1, des1 = orb.detectAndCompute(query_image, None)
kp2, des2 = orb.detectAndCompute(database_image, None)

# Brute force matching
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# Sort by distance for best matches
matches = sorted(matches, key=lambda x: x.distance)
```

### Web Scraping

The system automatically scrapes:
- High-resolution images from Google Images
- Scientific papers from academic databases
- Metadata and descriptions for each object

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Areas for Contribution

- 🔍 Improve image matching algorithms
- 🎨 Enhance the web interface
- 📊 Add more astronomical objects to the database
- 🐛 Fix bugs and optimize performance
- 📖 Improve documentation
- 🏆 **Science Olympiad Features**: Add study modes, practice quizzes, or competition-specific tools

**Special call to Science Olympiad community**: Share your feedback, suggest new features that would help with Astronomy event preparation, or contribute additional astronomical objects that are commonly tested!

## 📊 Performance

- **Database Size**: 15+ categories of astronomical objects
- **Image Processing**: Sub-second matching for most queries
- **Accuracy**: High precision matching using ORB features
- **Scalability**: Easily extendable database structure

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Author**: TheBheta
- **Repository**: [AstroGPT](https://github.com/TheBheta/AstroGPT)
- **Issues**: [Report a Bug](https://github.com/TheBheta/AstroGPT/issues)

---

<div align="center">
  <p><strong>🌟 Star this repository if you find it helpful! 🌟</strong></p>
  <p>Made with ❤️ for the astronomy community</p>
</div>
