# Proactive Financial Guardian

Un agente de IA autónomo diseñado para ser tu guardián financiero personal. Se conecta a tus cuentas, entiende tus metas financieras y te ayuda de forma proactiva a tomar mejores decisiones a través de recordatorios y análisis inteligentes.

## Arquitectura

El sistema utiliza una arquitectura de microservicios desacoplada, orquestada por un sistema de tareas en segundo plano.

  * **Backend API:** `FastAPI` (Python)
  * **Base de Datos:** `PostgreSQL` (gestionada con Docker)
  * **Cola de Tareas:** `Redis` (gestionada con Docker)
  * **Worker Asíncrono:** `RQ (Redis Queue)`
  * **Integraciones Externas:**
      * Google APIs (OAuth, Docs, Calendar, Gemini)
      * Bank of Anthos (aplicación web de ejemplo)


## Prerrequisitos

Antes de empezar, asegúrate de tener instalado lo siguiente:

  * **WSL 2 (Windows Subsystem for Linux):** El entorno de desarrollo recomendado para evitar incompatibilidades.
  * **Docker Desktop:** Para gestionar los servicios de base de datos y la cola.
  * **Python 3.10+:** Asegúrate de que esté disponible en tu entorno WSL.
  * **Git:** Para clonar el repositorio.

## 🚀 Guía de Instalación y Puesta en Marcha

Sigue estos pasos para configurar tu entorno de desarrollo local desde cero.

### 1\. Clonar el Repositorio

Abre tu terminal de WSL, navega a la carpeta donde guardas tus proyectos y clona el repositorio:

```bash
git clone <URL_DE_TU_REPOSITORIO>
cd proactive-financial-guardian
```

### 2\. Configurar los Secretos

La aplicación necesita claves de API y credenciales para funcionar. Nunca las subas al repositorio.

1.  **Credenciales de Google:**

      * Ve a la [Consola de Google Cloud](https://console.cloud.google.com/).
      * Crea un nuevo proyecto y activa las APIs de **Google Docs, Google Calendar y Vertex AI (para Gemini)**.
      * Ve a "Credenciales", crea una "ID de cliente de OAuth 2.0" de tipo "Aplicación web".
      * Añade `http://localhost:8000/callback` como URI de redireccionamiento autorizado.
      * Descarga el fichero JSON de credenciales y renómbralo a `client_secret.json` en la raíz del proyecto.

2.  **Variables de Entorno:**

      * Crea un fichero llamado `.env` en la raíz del proyecto. Este fichero está ignorado por Git para proteger tus secretos.
      * Copia y pega el siguiente contenido en tu fichero `.env` y rellénalo con tus propios valores:

    <!-- end list -->

    ```env
    # Fichero .env

    # URL de conexión a la base de datos PostgreSQL que corre en Docker
    DATABASE_URL="postgresql://postgres:mysecretpassword@localhost/postgres"

    # Clave de API de Google AI Studio para el modelo Gemini
    GOOGLE_API_KEY="aqui_va_tu_api_key_de_gemini"

    # Clave secreta para la sesión de FastAPI (puedes generar una con `openssl rand -hex 32`)
    SESSION_SECRET_KEY="tu_clave_secreta_aqui"
    ```

### 3\. Iniciar la Infraestructura (Docker)

Abre Docker Desktop y asegúrate de que está corriendo. Luego, desde tu terminal de WSL, ejecuta estos comandos para lanzar los contenedores de PostgreSQL y Redis:

```bash
# Iniciar PostgreSQL
docker run -d --name postgres-pfg -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=postgres postgres:latest

# Iniciar Redis
docker run -d --name redis-pfg -p 6379:6379 redis:latest
```

### 4\. Configurar el Entorno de Python

```bash
# Crea un entorno virtual
python3 -m venv venv

# Actívalo
source venv/bin/activate

# Instala todas las dependencias
pip install -r requirements.txt
```

### 5\. Inicializar la Base de Datos

Este comando leerá tus modelos de SQLAlchemy y creará las tablas necesarias en la base de datos de PostgreSQL.

```bash
python create_tables.py
```

## ▶️ Ejecutar la Aplicación

Necesitarás **dos terminales de WSL** (ambas con el entorno virtual activado `source venv/bin/activate`).

  * **Terminal 1: Iniciar el Servidor API**

    ```bash
    uvicorn app.main:app --reload --port 8000
    ```

  * **Terminal 2: Iniciar el Worker**

    ```bash
    python run_worker.py
    ```

¡La aplicación ya está corriendo! La API está disponible en `http://localhost:8000`.

## 🧪 Cómo Probarlo

1.  **Autenticación Inicial:**

      * Abre tu navegador y ve a `http://localhost:8000/`.
      * Haz clic en el enlace para iniciar sesión con Google.
      * Completa el flujo de OAuth. Esto creará una entrada para tu usuario en la base de datos.

2.  **Configuración de Datos para la Prueba:**

      * Para probar la funcionalidad de IA, tu usuario necesita tener una URL de Google Doc asignada. Como aún no hay interfaz para esto, puedes usar el script `temp_set_doc_url.py` (si lo tienes) o modificar la base de datos manualmente.

3.  **Lanzar una Tarea:**

      * Ve a la documentación interactiva de la API en `http://localhost:8000/docs`.
      * Busca el endpoint `POST /tasks/trigger/payment-prediction/{user_id}`.
      * Haz clic en "Try it out", introduce el `id` de tu usuario (normalmente `1` si es el primero) y haz clic en "Execute".

4.  **Verificar el Resultado:**

      * Observa la salida en la **Terminal 2 (Worker)**. Verás los logs del procesamiento: lectura del Doc, llamada a Gemini y creación del evento en Calendar.
      * Revisa tu Google Calendar para ver el evento creado.

## Deployment to Google Kubernetes Engine (GKE)

This guide outlines the steps to deploy the Proactive Financial Guardian to a GKE cluster.

1. **Prerequisites**

      * A Google Cloud Platform (GCP) project with billing enabled.
      * gcloud CLI installed and authenticated.
      * kubectl installed.
      * A registered domain name.
      * Docker Desktop installed and running.

2. **GCP Setup**

      * Enable APIs: In your GCP project, enable the following APIs:
      * Kubernetes Engine API
      * Artifact Registry API
      * Vertex AI API
      * Google Docs API
      * Google Calendar API
      * Create GKE Cluster & Artifact Registry: (You can add your gcloud commands here for cluster and repository creation).
      * Configure kubectl: gcloud container clusters get-credentials ...
      * Reserve a Static IP: gcloud compute addresses create guardian-static-ip --global
      * Configure DNS: Create an A record for your subdomain (e.g., guardian.your-domain.com) pointing to the reserved static IP.
      * Grant Permissions: Grant the GKE nodes permission to pull from Artifact Registry.

      ```bash
      gcloud projects add-iam-policy-binding ...
      ```
3. **Building and Pushing Images**

      For each deployment, build and push the versioned Docker images to avoid caching issues:

      ```bash
      # Example for v2
      docker build -t us-central1-docker.pkg.dev/your-project/your-repo/api:v2 -f Dockerfile.api .
      docker push us-central1-docker.pkg.dev/your-project/your-repo/api:v2
      ```
4. **Kubernetes Deployment Steps**

      Apply the Kubernetes manifests in the following order:

      * PostgreSQL: kubectl apply -f kubernetes/01-postgres.yaml
      * Redis: kubectl apply -f kubernetes/02-redis.yaml
      * Application Secrets: Create kubernetes/03-app-secrets.yaml with the necessary base64-encoded keys and apply it.
      * Deployments: kubectl apply -f kubernetes/04-deployment.yaml (Ensure the image tag is updated to the latest version).
      * Service & Ingress: Apply the 05-api-service.yaml, 06-certificate.yaml, 07-ingress.yaml, and 08-backend-config.yaml files to configure networking and SSL.
      * Database Migration: Run the one-time database table creation job: kubectl apply -f kubernetes/09-create-tables-job.yaml