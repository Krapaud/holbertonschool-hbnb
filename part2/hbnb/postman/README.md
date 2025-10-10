# Configuration Postman pour l'API HBNB

## Installation et Configuration

### 1. Extension Postman VS Code
L'extension Postman officielle est déjà installée dans votre VS Code.

### 2. Importation des fichiers Postman

#### Importer la Collection
1. Dans VS Code, ouvrez la palette de commandes (`Ctrl+Shift+P`)
2. Tapez "Postman" et sélectionnez "Postman: Open Postman"
3. Cliquez sur "Import"
4. Sélectionnez le fichier `postman/HBNB_API_Collection.json`

#### Importer l'Environnement
1. Dans Postman, cliquez sur l'icône "Environment" (engrenage) en haut à droite
2. Cliquez sur "Import"
3. Sélectionnez le fichier `postman/HBNB_Development_Environment.json`
4. Sélectionnez l'environnement "HBNB Development" dans le dropdown

## Structure de la Collection

### 📁 Users
- **Create User** : POST `/api/v1/users/`
  - Teste la création d'un nouvel utilisateur
  - Sauvegarde automatiquement l'ID utilisateur pour les autres requêtes
  - Tests automatiques inclus

- **Get User by ID** : GET `/api/v1/users/{{user_id}}`
  - Récupère les détails d'un utilisateur
  - Utilise l'ID sauvegardé de la requête précédente

- **Create User - Duplicate Email** : POST `/api/v1/users/`
  - Teste la validation d'email dupliqué
  - Vérifie que l'API retourne une erreur 400

- **Get User - Not Found** : GET `/api/v1/users/non-existing-id`
  - Teste le cas d'utilisateur introuvable
  - Vérifie que l'API retourne une erreur 404

### 📁 Places (À implémenter)
- Templates prêts pour les endpoints Places
- Sera fonctionnel une fois les endpoints implémentés

### 📁 Amenities (À implémenter)
- Templates prêts pour les endpoints Amenities
- Sera fonctionnel une fois les endpoints implémentés

### 📁 Reviews (À implémenter)
- Templates prêts pour les endpoints Reviews
- Sera fonctionnel une fois les endpoints implémentés

## Variables d'Environnement

### Variables de Collection
- `user_id` : ID de l'utilisateur créé (défini automatiquement)
- `place_id` : ID du lieu créé (à définir manuellement si nécessaire)
- `base_url` : http://localhost:5000

### Variables d'Environnement (HBNB Development)
- `base_url` : http://localhost:5000
- `api_version` : v1
- `content_type` : application/json

## Tests Automatiques

Chaque requête importante inclut des tests automatiques qui vérifient :
- Les codes de statut HTTP
- La structure des réponses JSON
- La présence des champs requis
- Les messages d'erreur appropriés

### Exécution des Tests
1. Sélectionnez la collection "HBNB API Collection"
2. Cliquez sur "Run" pour exécuter tous les tests
3. Ou exécutez les requêtes individuellement

## Utilisation Recommandée

### Workflow de Test Complet
1. **Démarrer l'API** : `python run.py` dans le terminal
2. **Exécuter la Collection** : Lance tous les tests automatiquement
3. **Vérifier les Résultats** : Consulter le rapport de tests

### Test Manuel
1. Exécuter "Create User" en premier pour créer un utilisateur de test
2. L'ID utilisateur sera automatiquement sauvegardé
3. Exécuter les autres requêtes qui utilisent cet ID

## Commandes Utiles

### Démarrer l'API
```bash
cd /home/krapaud/holbertonschool-hbnb/part2/hbnb
python run.py
```

### Vérifier que l'API fonctionne
```bash
curl http://localhost:5000/api/v1/users/
```

## Résolution de Problèmes

### API non disponible
- Vérifiez que `python run.py` fonctionne sans erreur
- Vérifiez que le port 5000 n'est pas utilisé par une autre application
- Utilisez `lsof -i :5000` pour vérifier

### Collection non importée
- Vérifiez le chemin des fichiers JSON
- Redémarrez VS Code si nécessaire
- Essayez d'importer directement via l'application Postman

### Variables non définies
- Vérifiez que l'environnement "HBNB Development" est sélectionné
- Exécutez d'abord "Create User" pour définir `user_id`

## Extension Alternatives

Si l'extension Postman pose problème, vous pouvez utiliser :
- **Thunder Client** : Extension légère et intuitive
- **REST Client** : Extension basée sur des fichiers .http
- **httpYac** : Client REST avancé avec support multi-protocoles

## Évolutions Futures

À mesure que vous implémentez les autres endpoints :
1. Ajoutez les nouveaux endpoints dans la collection
2. Mettez à jour les tests automatiques
3. Ajoutez de nouvelles variables si nécessaire
4. Documentez les nouveaux cas d'usage
