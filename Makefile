# ==========================
# Makefile pour docker-compose
# situé à la racine du repo
# docker-compose.yml est dans /deploy
# ==========================

# Cible par défaut
.DEFAULT_GOAL := help

# Variables
COMPOSE_FILE := deploy/docker-compose.yml
DOCKER_COMPOSE := docker-compose -f $(COMPOSE_FILE)

# Liste des services
SERVICES := db auth_service profile_service matching_service chat_service notification_service frontend nginx

# Éviter les conflits avec des fichiers du même nom
.PHONY: help build up down restart logs clean prune re du test

# Aide
help:
	@echo "Commandes générales :"
	@echo "  make build        : Construire toutes les images Docker"
	@echo "  make up           : Démarrer tous les services en arrière-plan"
	@echo "  make down         : Arrêter et supprimer tous les services"
	@echo "  make restart      : Redémarrer tous les services"
	@echo "  make logs         : Afficher les logs de tous les services (suivi en direct)"
	@echo "  make clean        : Arrêter et supprimer tous les services + volumes"
	@echo "  make prune        : Nettoyage complet (images, volumes, orphelins...)"
	@echo "  make re           : (prune + build + up) Nettoyer et tout reconstruire"
	@echo "  make du           : down + up --build (recréer l'environnement)"
	@echo ""
	@echo "Commandes par service :"
	@echo "  make <service>-up        : Démarrer un service (ex: make auth_service-up)"
	@echo "  make <service>-down      : Arrêter un service"
	@echo "  make <service>-restart   : Redémarrer un service"
	@echo "  make <service>-logs      : Afficher les logs d'un service"
	@echo "  make build-<service>     : Construire l'image d'un service"
	@echo "  make recreate-<service>  : Recréer le conteneur d'un service (--force-recreate)"
	@echo ""
	@echo "Tests :"
	@echo "  make test : Exécuter les tests (ex: fait un 'docker-compose exec ...' ou un script)."
	@echo ""
	@echo "Exemples :"
	@echo "  make auth_service-up"
	@echo "  make profile_service-logs"
	@echo "  make build-matching_service"
	@echo ""
	@echo "Astuce : Voir la liste complète avec 'make help'."

# ==========================
# Commandes générales
# ==========================

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

logs:
	$(DOCKER_COMPOSE) logs -f

clean:
	$(DOCKER_COMPOSE) down -v

prune:
	@echo "Nettoyage complet de l'environnement Docker..."
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	docker system prune -f
	docker volume prune -f

re: prune build up

du:
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d --build

# ==========================
# Commandes par service
# ==========================
# Génération automatique de cibles pour chaque service :
#  - <service>-up
#  - <service>-down
#  - <service>-restart
#  - <service>-logs
#  - build-<service>
#  - recreate-<service>
# A adapter si vous souhaitez d’autres noms.

$(foreach service,$(SERVICES),$(eval \
$(service)-up: ; \
	$(DOCKER_COMPOSE) up -d $(service) ; \
\
$(service)-down: ; \
	$(DOCKER_COMPOSE) stop $(service) ; \
\
$(service)-restart: ; \
	$(DOCKER_COMPOSE) restart $(service) ; \
\
$(service)-logs: ; \
	$(DOCKER_COMPOSE) logs -f $(service) ; \
\
build-$(service): ; \
	$(DOCKER_COMPOSE) build $(service) ; \
\
recreate-$(service): ; \
	$(DOCKER_COMPOSE) up -d --force-recreate $(service) ; \
))

# ==========================
# Tests
# ==========================
# Exécution globale des tests.
# A adapter si vous avez un conteneur 'tests'
# ou si vous faites 'exec auth_service pytest' etc.

test:
	@echo "Exécution globale des tests..."
	# Option 1: Si vous avez un conteneur 'tests':
	# $(DOCKER_COMPOSE) run --rm tests

	# Option 2: Exécuter un script Python qui fait tout
	# python services/exec_all_tests.py

	# Option 3: Docker-compose exec sur chaque microservice
	# ex:
	# $(DOCKER_COMPOSE) exec auth_service pytest
	# $(DOCKER_COMPOSE) exec profile_service pytest
	# etc.

	# Mettez la logique qui vous convient, par exemple :
	$(DOCKER_COMPOSE) exec auth_service pytest
	$(DOCKER_COMPOSE) exec profile_service pytest
	$(DOCKER_COMPOSE) exec matching_service pytest
	$(DOCKER_COMPOSE) exec chat_service pytest
	$(DOCKER_COMPOSE) exec notification_service pytest

	@echo "Tous les tests se sont terminés (sans erreur)."
