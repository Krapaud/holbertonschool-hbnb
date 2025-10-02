# 🏠 HBnB - Holberton School Project

> **Project Status**: 🚧 **Under Development** 🚧

## 📋 Overview

HBnB is a "bed and breakfast" type accommodation rental application developed as part of the Holberton School curriculum. The project aims to create a complete platform for managing accommodations, reservations, and users.

## 🎯 Project Objectives

This project aims to develop a complete web application following software development best practices:

- **Layered Architecture**: Clear separation between presentation, business logic, and data
- **REST API**: Standardized programming interface
- **UML Modeling**: Complete technical documentation with diagrams
- **Design Patterns**: Use of patterns like Repository, Facade, etc.

## 🏗️ Project Architecture

The project follows a well-defined layered architecture:

```
📁 HBnB Application
├── 🌐 Presentation Layer (REST API)
├── 🧠 Business Logic Layer (Domain)
├── 💾 Data Access Layer (Repository)
└── 🗄️ Persistence Layer (Database)
```

## 📁 Current Project Structure

```
holbertonschool-hbnb/
├── README.md                                    # This file
├── HBnB_Document_Technique_Architecture.md     # Complete technical documentation
└── part1/                                      # Phase 1 - Design and modeling
    ├── README.md                              # Part 1 documentation
    ├── high-level_package_diagram.mmd        # High-level package diagram
    ├── business_logic_layer_diagram.mmd      # Business Logic layer diagram
    ├── sequence_api_call_user.mmd            # Sequence diagram - Users
    ├── sequence_api_call_place.mmd           # Sequence diagram - Places
    ├── sequence_api_call_review.mmd          # Sequence diagram - Reviews
    └── sequence_api_call_request_list.mmd    # Sequence diagram - Lists
```

## 🚀 Planned Features

### 👥 User Management
- Registration and authentication
- User profiles (hosts and travelers)
- Rights and permissions management

### 🏡 Accommodation Management
- Creation and modification of listings
- Availability management
- Photo upload and management
- Geolocation

### 📅 Reservation System
- Accommodation search
- Online booking
- Calendar management
- Payment system

### ⭐ Review System
- Reviews and ratings
- Bidirectional comments
- Content moderation

## 📊 Current Phase - Part 1: Design and Modeling

### ✅ Delivered Elements

1. **Complete Technical Documentation**
   - Detailed architecture document
   - Functional requirements analysis

2. **UML Diagrams**
   - High-level package diagram
   - Business Logic class diagram
   - API call sequence diagrams

3. **Flow Modeling**
   - User interaction flows
   - Accommodation management flows
   - Review system flows
   - List request flows

### 🔄 Next Steps

- [ ] **Part 2**: Business Logic layer implementation
- [ ] **Part 3**: REST API development
- [ ] **Part 4**: Web user interface
- [ ] **Part 5**: Testing and deployment

## 📚 Documentation

- **[Complete Technical Documentation](./HBnB_Document_Technique_Architecture.md)** - Detailed architecture blueprint
- **[Part 1 Documentation](./part1/README.md)** - Design and modeling phase

## 🛠️ Planned Technologies

- **Backend**: Python/Flask or FastAPI
- **Database**: SQLite/PostgreSQL
- **Frontend**: HTML/CSS/JavaScript
- **Documentation**: Mermaid for UML diagrams

## 👨‍💻 Developers

Project developed as part of the **Holberton School** curriculum.

## 📄 License

This project is developed for educational purposes as part of the Holberton School program.

---

**Note**: This project is currently in the design phase. Code implementation will follow in the upcoming parts of the project.
