# 🌍 Kazakhstan Tourism Platform

[![Angular](https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white)](https://angular.io/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-FF1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)](https://jwt.io/)

> Discover the beauty of Kazakhstan through our interactive tourism platform! 🏞️✨

## 📖 Description

Welcome to the **Kazakhstan Tourism Platform** – a full-stack web application designed to showcase and explore the stunning landscapes, cultural heritage, and hidden gems of Kazakhstan. Whether you're a local traveler or an international visitor, our platform offers a seamless experience to discover locations, read reviews, manage favorites, and connect with fellow explorers.

### 🎯 Key Features
- **🔐 Secure Authentication**: JWT-based login and registration system
- **📍 Location Management**: Browse, create, update, and delete tourist locations
- **⭐ Reviews & Ratings**: Share your experiences and read authentic reviews
- **❤️ Favorites**: Save your favorite spots for quick access
- **📱 Responsive Design**: Optimized for desktop and mobile devices
- **🔄 Real-time Updates**: Dynamic content loading with Angular
- **🛡️ CORS Enabled**: Smooth frontend-backend communication

## 🛠️ Tech Stack

### Frontend
- **Angular 17+** – Modern web framework for building SPAs
- **TypeScript** – Strongly typed programming language
- **CSS3** – Stylish and responsive UI components
- **RxJS** – Reactive programming for async operations

### Backend
- **Django** – High-level Python web framework
- **Django REST Framework** – Powerful API toolkit
- **SQLite** – Lightweight database for development
- **JWT Authentication** – Secure token-based auth
- **CORS Headers** – Cross-origin resource sharing

### Tools & Testing
- **Postman** – API testing and documentation
- **Git** – Version control
- **VS Code** – Development environment

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v18+) and **npm** for Angular
- **Python** (v3.8+) and **pip** for Django
- **Git** for cloning the repository

### Installation & Setup

1. **Clone the Repository** 📥
   ```bash
   git clone https://github.com/your-username/kazakhstan-tourism-platform.git
   cd kazakhstan-tourism-platform
   ```

2. **Backend Setup** 🐍
   ```bash
   cd back/project
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend Setup** ⚛️
   ```bash
   cd ../../angular-frontend
   npm install
   ng serve
   ```

4. **Access the Application** 🌐
   - Frontend: [http://localhost:4200](http://localhost:4200)
   - Backend API: [http://localhost:8000](http://localhost:8000)

### 🆕 Tips for First-Time Users

- **🔑 Register an Account**: Start by creating a user account to unlock full features like adding reviews and managing favorites.
- **🏞️ Explore Locations**: Browse the homepage to discover featured locations. Click on any location for detailed information.
- **💬 Leave Reviews**: Share your experiences! After visiting a location, add a review to help other travelers.
- **❤️ Save Favorites**: Use the heart icon to bookmark locations you want to visit later.
- **📱 Mobile Friendly**: The app is fully responsive – try it on your phone for the best experience.
- **🧪 Test with Postman**: Import the provided Postman collection (`postman/`) to test API endpoints directly.
- **🔧 Development Mode**: Both frontend and backend run in development mode with hot-reloading for easy coding.

### 📚 API Documentation
Check out our Postman collection for detailed API endpoints:
- Authentication (Login/Register/Logout)
- Locations (CRUD operations)
- Reviews (Create/Read/Delete)
- Favorites (Add/Remove/Get)

## 👥 Contributors

This project was lovingly crafted by:

<table>
  <tr>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/12345678?v=4" width="100px;" alt="Niyazbekova Elza"/><br />
      <sub><b>Niyazbekova Elza</b></sub><br />
      <sub>Backend Developer</sub>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/87654321?v=4" width="100px;" alt="Altynbek Amina"/><br />
      <sub><b>Altynbek Amina</b></sub><br />
      <sub>Frontend Developer</sub>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/11223344?v=4" width="100px;" alt="Nursultan Dastan"/><br />
      <sub><b>Nursultan Dastan</b></sub><br />
      <sub>Full-Stack Developer</sub>
    </td>
  </tr>
</table>

## 📄 Project Structure

```
kazakhstan-tourism-platform/
├── angular-frontend/          # Angular application
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/    # UI components
│   │   │   ├── services/      # API services
│   │   │   ├── guards/        # Route guards
│   │   │   └── models/        # TypeScript interfaces
│   │   └── styles.css
│   └── angular.json
├── back/                      # Django backend
│   └── project/
│       ├── api/               # Django REST API
│       │   ├── models.py      # Database models
│       │   ├── views.py       # API views
│       │   ├── serializers.py # Data serializers
│       │   └── urls.py        # API routes
│       ├── project/
│       │   ├── settings.py    # Django settings
│       │   ├── urls.py        # Main URLs
│       │   └── wsgi.py
│       ├── db.sqlite3         # SQLite database
│       └── manage.py
├── postman/                   # API testing collections
└── README.md                  # This file
```

## 🎉 Acknowledgments

- Special thanks to the beautiful landscapes of Kazakhstan for inspiration! 🇰🇿
- Built with ❤️ using open-source technologies
- Inspired by the need to showcase Kazakhstan's tourism potential

## 📞 Support

If you encounter any issues or have suggestions:
- Open an issue on GitHub
- Contact the contributors
- Check the Postman collection for API examples

---

*Made with passion for Kazakhstan's tourism industry* 🌟