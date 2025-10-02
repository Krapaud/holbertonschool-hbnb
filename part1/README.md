# HBnB — Document technique : Blueprint d'architecture

---

## 1. Objet du document

Ce document regroupe et explique les diagrammes et notes produits lors des tâches précédentes (diagramme de packages haut niveau, diagramme de classes détaillé pour la couche Business Logic, diagrammes de séquence pour les appels API). Il sert de référence technique pour l'implémentation et la maintenance du projet HBnB.

**Public visé** : développeurs backend, architectes, chefs de projet, QA.

**Périmètre** : architecture applicative, conception de la Business Logic, flux d'interaction API. Ne couvre pas les choix d'infrastructure détaillés (déploiement CI/CD, infra cloud) sauf mention explicite.

---

## 2. Table des matières

1. [Objet du document](#1-objet-du-document)
2. [Table des matières](#2-table-des-matières)
3. [Vue d'ensemble du projet](#3-vue-densemble-du-projet)
4. [Architecture globale](#4-architecture-globale)
5. [Couche Business Logic (Domain)](#5-couche-business-logic-domain)
6. [Flux d'interaction API](#6-flux-dinteraction-api)
7. [Décisions de conception et justifications](#7-décisions-de-conception-et-justifications)
8. [Contrats API (résumé)](#8-contrats-api-résumé)
9. [Non-fonctionnel et contraintes](#9-non-fonctionnel-et-contraintes)
10. [Checklist de relecture / livraison](#10-checklist-de-relecture--livraison)
11. [Annexes](#11-annexes)

---

## 3. Vue d'ensemble du projet

HBnB est une application de location (similaire conceptuellement à « hôte & bed and breakfast ») qui permet :

- **gestion des hébergements** (création, modification, suppression),
- **recherche et réservation**,
- **gestion des disponibilités et calendriers**,
- **facturation et gestion des paiements**,
- **gestion des utilisateurs** (hôtes, voyageurs, admins).

Le système adopte une architecture en couches : présentation (API REST), service / business logic, couche d'accès aux données (repository / DAL), et persistance (base de données). Une façade (Facade) ou API service expose des points d'entrée simplifiés à la couche supérieure.

---

## 4. Architecture globale

### 4.1 Diagramme de packages (HAUT NIVEAU)

```mermaid
classDiagram
    class PresentationLayer {
        +UserAPI
        +PlaceAPI
        +ReviewAPI
        +AmenityAPI
    }
    class BusinessLogicLayer {
        +HBnBFacade
        +User
        +Place
        +Review
        +Amenity
    }
    class PersistenceLayer {
        +UserRepository
        +PlaceRepository
        +ReviewRepository
        +AmenityRepository
        +Database
    }
    PresentationLayer ..> BusinessLogicLayer : "Facade Pattern"
    BusinessLogicLayer ..> PersistenceLayer : "Database Operations"
```

**Objectif du diagramme** : montrer les principaux modules/packages et leurs dépendances (API, Controllers, Services, Domain, Repositories, Models/DTOs, Infrastructure, Auth).

### 4.2 Composants clés

- **Presentation Layer (API)** : contrôleurs REST, validation des requêtes, mapping DTO → Domain
- **Business Logic Layer** : logique métier, orchestration, transactions
- **Persistence Layer** : abstractions d'accès aux données, implémentations (SQL/NoSQL)
- **Infrastructure** : intégrations externes (paiements, email, storage)
- **Security** : gestion JWT / OAuth, politiques d'accès

### 4.3 Décisions de conception

> **Decision** : Séparation claire entre domain (logique pure) et service (orchestration) pour faciliter tests unitaires et réutilisabilité.

> **Decision** : Dépendances dirigées vers l'intérieur (outer layers dépendent des abstractions du domain).

> **Decision** : Pattern façade pour fournir une interface stable aux contrôleurs et masquer la complexité des opérations transactionnelles.

### 4.4 Pattern façade et raisons

Le pattern Façade simplifie l'interface entre la couche de présentation et la logique métier en :
- Centralisant les points d'entrée de l'API
- Gérant les transactions de manière cohérente
- Masquant la complexité interne des interactions entre services
- Facilitant les tests et la maintenance

---

## 5. Couche Business Logic (Domain)

### 5.1 Diagramme de classes détaillé

```mermaid
classDiagram
    class BaseModel {
        +UUID4 id
        +datetime created_at
        +datetime updated_at
    }
    class PlaceModel {
        +string name
        +string description
        +float price
        +float latitude
        +float longitude
        +update_place(place)
        +add_amenity(amenity)
        +create_place()
        +delete_place(place)
    }
    class AmenityModel {
        +string name
        +string description
        +update_amenity(amenity)
        +list_amenity()
        +create_amenity()
        +delete_amenity(amenity)
    }
    class UserModel {
        +string first_name
        +string last_name
        +string email
        -string password
        +bool admin
        +authenticate(email, password)
        +create_profile()
        +update_profile(user)
        +delete_profile(user)
    }
    class ReviewModel {
        +string text
        +int rating
        +update_review(review)
        +create_review()
        +delete_review(review)
    }

    BaseModel <|-- PlaceModel
    BaseModel <|-- UserModel
    BaseModel <|-- AmenityModel
    BaseModel <|-- ReviewModel
    UserModel "1" --> "*" PlaceModel
    UserModel "1" --> "*" ReviewModel
    ReviewModel "*" --> "1" PlaceModel
    PlaceModel "*" -- "*" AmenityModel
```

**But** : représenter les entités, agrégats, repos, services de domaine et leurs relations.

### 5.2 Principales entités (extrait)

#### User (hôte / voyageur)
- **attributs** : id, email, hashedPassword, role, profile
- **méthodes** : authenticate(), canCreateListing(), isHost()

#### Place (hébergement)
- **attributs** : id, ownerId, title, description, location, amenities, basePrice
- **méthodes** : calculatePrice(dateRange), isAvailable(dateRange)

#### Review (avis)
- **attributs** : id, placeId, guestId, text, rating, createdAt
- **méthodes** : validate(), update(), delete()

#### Amenity (équipement)
- **attributs** : id, name, description
- **méthodes** : create(), update(), delete(), list()

### 5.3 Description des entités et relations

- **BaseModel** : classe abstraite fournissant les propriétés communes (ID, timestamps)
- **UserModel** : représente les utilisateurs du système (hôtes et voyageurs)
- **PlaceModel** : représente les logements disponibles à la location
- **ReviewModel** : représente les avis laissés par les voyageurs
- **AmenityModel** : représente les équipements et services disponibles

### 5.4 Règles métier importantes

1. **Authentification** : seuls les utilisateurs authentifiés peuvent créer des places et des reviews
2. **Propriété** : un utilisateur ne peut modifier que ses propres places
3. **Reviews** : un utilisateur ne peut laisser qu'un seul avis par place
4. **Validation des données** : tous les champs obligatoires doivent être validés côté serveur

### 5.5 Services et objets de domaine

- **PlaceService** : orchestration de la gestion des places
- **UserService** : gestion de l'authentification et des profils
- **ReviewService** : validation des avis et gestion des conflits
- **AmenityService** : gestion des équipements

### 5.6 Repositories (interfaces)

- **IUserRepository**, **IPlaceRepository**, **IReviewRepository**, **IAmenityRepository**
- **implémentations** : SqlUserRepository, MongoPlaceRepository (exemples selon DB choisie)

> **Raisons** : interfaces permettent substitution pour tests et choix de persistance variable.

---

## 6. Flux d'interaction API

### 6.1 Diagrammes de séquence inclus

Les diagrammes suivants illustrent les principaux flux d'interaction :
- Création d'un utilisateur
- Création d'une place
- Recherche de places
- Création d'un avis

### 6.2 Séquence : Création d'un utilisateur

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant UserModel
    participant Database

    Client->>API: POST /users (signup request)
    API->>UserModel: validate_data(email, password, names)
    alt invalid data
        UserModel-->>API: error (400 Bad Request)
        API-->>Client: 400 Bad Request
    else valid data
        UserModel->>Database: check if email exists
        alt email already exists
            Database-->>UserModel: email found
            UserModel-->>API: error (409 Conflict)
            API-->>Client: 409 Conflict (Email already used)
        else email not found
            Database-->>UserModel: no match
            UserModel->>Database: INSERT new user
            Database-->>UserModel: success (user_id)
            UserModel-->>API: return new user object
            API-->>Client: 201 Created (user_id, info, token)
        end
    end
```

**Acteurs** : Client (frontend/mobile), API Controller, UserModel, Database

**Étapes clefs** :
1. Frontend POST /users avec données d'inscription
2. API valide les données via UserModel
3. Vérification de l'unicité de l'email
4. Création du compte utilisateur
5. Retour du token d'authentification

### 6.3 Séquence : Création d'une place

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant UserModel
    participant PlaceModel
    participant Database

    Client->>API: POST /places (place data)
    API->>UserModel: verify authentication (token)
    alt invalid or expired token
        UserModel-->>API: error (401 Unauthorized)
        API-->>Client: 401 Unauthorized
    else user valid
        UserModel-->>API: user verified
        API->>PlaceModel: validate place data
        alt invalid data
            PlaceModel-->>API: error (400 Bad Request)
            API-->>Client: 400 Bad Request
        else valid data
            PlaceModel->>Database: INSERT new place
            Database-->>PlaceModel: success (place_id)
            PlaceModel-->>API: return place object
            API-->>Client: 201 Created (place_id, info)
        end
    end
```

**Points d'attention** : 
- Vérification de l'authentification obligatoire
- Validation complète des données de la place
- Gestion des erreurs d'autorisation et de validation

### 6.4 Séquence : Recherche de places

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant PlaceModel
    participant Database

    Client->>API: GET /places?city=X&price<Y
    API->>PlaceModel: validate search filters
    alt invalid filters
        PlaceModel-->>API: error (400 Bad Request)
        API-->>Client: 400 Invalid Query Parameters
    else valid filters
        PlaceModel->>Database: SELECT places WHERE filters
        alt no results found
            Database-->>PlaceModel: empty list
            PlaceModel-->>API: return []
            API-->>Client: 200 OK (empty list)
        else results found
            Database-->>PlaceModel: list of places
            PlaceModel-->>API: return place objects
            API-->>Client: 200 OK (list of places)
        end
    end
```

**Résumé** : frontend → PlaceController.search() → PlaceService applique filtres, appelle PlaceRepository.search() → mapper DTOs vers frontend. Pagination, cache (Redis) recommandé.

### 6.5 Séquence : Création d'un avis

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant UserModel
    participant PlaceModel
    participant ReviewModel
    participant Database

    Client->>API: POST /reviews (review data)
    API->>UserModel: verify authentication
    alt invalid token
        UserModel-->>API: error (401 Unauthorized)
        API-->>Client: 401 Unauthorized
    else user valid
        UserModel-->>API: user verified
        API->>PlaceModel: verify place exists
        PlaceModel->>Database: SELECT place by id
        alt place not found
            Database-->>PlaceModel: no match
            PlaceModel-->>API: error (404 Not Found)
            API-->>Client: 404 Place Not Found
        else place exists
            Database-->>PlaceModel: place found
            API->>ReviewModel: validate review data
            alt invalid review data
                ReviewModel-->>API: error (400 Bad Request)
                API-->>Client: 400 Bad Request
            else valid review
                ReviewModel->>Database: INSERT new review
                Database-->>ReviewModel: success (review_id)
                ReviewModel-->>API: return review object
                API-->>Client: 201 Created (review_id, info)
            end
        end
    end
```

**Étapes critiques** :
1. Authentification de l'utilisateur
2. Vérification de l'existence de la place
3. Validation des données de l'avis
4. Persistance de l'avis

---

## 7. Décisions de conception et justifications

### 7.1 Architecture en couches
- **Facilite tests** : chaque couche peut être testée indépendamment
- **Remplaçabilité** : les implémentations peuvent être changées sans impact
- **Séparation de responsabilités** : chaque couche a un rôle bien défini

### 7.2 Façade/API Service
- **Simplifie controllers** : interface unifiée pour les opérations complexes
- **Centralise transactions** : gestion cohérente des rollbacks

### 7.3 Repositories + Interfaces
- **Inversion de dépendance** : facilite les tests unitaires
- **Migrations DB futures** : changement de base de données simplifié

### 7.4 Sécurité
- **JWT pour API stateless** : scalabilité horizontale
- **RBAC pour endpoints sensibles** : contrôle d'accès granulaire
- **Validation côté serveur** : sécurité renforcée

---

## 8. Contrats API (résumé)

### 8.1 Endpoints principaux

#### POST /users (Création d'utilisateur)
- **Request body** : `{ first_name, last_name, email, password }`
- **Response 201** : `{ user_id, email, token }`
- **Response 409** : Conflit si email déjà utilisé
- **Response 400** : Données invalides

#### POST /places (Création de place)
- **Headers requis** : `Authorization: Bearer <token>`
- **Request body** : `{ name, description, price, latitude, longitude }`
- **Response 201** : `{ place_id, name, price }`
- **Response 401** : Token invalide ou expiré
- **Response 400** : Données invalides

#### GET /places (Recherche de places)
- **Query params** : `city, price_min, price_max`
- **Response 200** : `[{ place_id, name, price, location }]`
- **Response 400** : Paramètres de recherche invalides

#### POST /reviews (Création d'avis)
- **Headers requis** : `Authorization: Bearer <token>`
- **Request body** : `{ place_id, text, rating }`
- **Response 201** : `{ review_id, text, rating }`
- **Response 404** : Place non trouvée
- **Response 401** : Non authentifié

---

## 9. Non-fonctionnel et contraintes

### 9.1 Performance
- **Temps de réponse** : recherche et pages listes < 300ms sous charge normale
- **Optimisations** : index DB et cache Redis recommandés

### 9.2 Scalabilité
- **Architecture stateless** : JWT pour faciliter la montée en charge
- **Cache distribué** : Redis pour les requêtes fréquentes

### 9.3 Résilience
- **Gestion d'erreur** : retry/backoff sur intégrations externes
- **Circuit-breaker** : protection contre les cascades de pannes

### 9.4 Observabilité
- **Logs structurés** : format JSON pour faciliter l'analyse
- **Traces distribuées** : OpenTelemetry recommandé
- **Métriques** : Prometheus pour le monitoring

### 9.5 Sécurité
- **Chiffrement** : données sensibles chiffrées en base
- **Validation** : sanitisation de toutes les entrées utilisateur
- **Rate limiting** : protection contre les abus

---

## 10. Checklist de relecture / livraison

- [ ] Diagrammes intégrés et à jour
- [ ] Contrats API documentés
- [ ] Tests unitaires couvrant les règles métier
- [ ] Documentation de déploiement
- [ ] Configuration de sécurité validée
- [ ] Monitoring et alertes configurés
- [ ] Performance testée sous charge
- [ ] Relecture par un pair architecture
- [ ] Relecture orthographe et style

---
