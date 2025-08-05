

````markdown
# SmartLINK - AI-Powered Recommendation Engine

This is an AI-based recommendation engine that matches people based on shared institutions (e.g., schools, companies), activities, and social graphs using **Qdrant** for semantic search and **Neo4j** for graph database management.

## 🚀 Project Setup

Follow these instructions to set up and run the project locally.

### Prerequisites

- **Docker** (for running Qdrant and Neo4j containers)
- **Python 3.11+** (preferably inside a virtual environment)
- **pip** (for installing Python packages)

### Step 1: Clone the Repository

Clone the repository to your local machine.

```bash
git clone https://github.com/your-username/SmartLINK.git
cd SmartLINK
````

### Step 2: Set Up Docker Containers

This project uses **Docker** to run **Qdrant** and **Neo4j**.

#### 2.1 Install Docker

If you don't have Docker installed, follow the [official Docker installation guide](https://docs.docker.com/get-docker/) to set it up.

#### 2.2 Pull and Run Qdrant

Run the following command to start the Qdrant container (vector search engine):

```bash
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant
```

Confirm Qdrant is running by visiting `http://localhost:6333/collections`. You should see an empty collection.

#### 2.3 Pull and Run Neo4j

Neo4j is used for storing and visualizing graph relationships between users.

```bash
docker run -d -p 7474:7474 -p 7687:7687 --name neo4j -e NEO4J_AUTH=neo4j/test123 neo4j:5.14
```

Login using:

* **Username**: `neo4j`
* **Password**: `test123`

Check if Neo4j is running by visiting `http://localhost:7474`.

---

### Step 3: Set Up Python Environment

#### 3.1 Create a Virtual Environment

Create and activate a virtual environment for the project.

```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
```

#### 3.2 Install Dependencies

Install required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

---

### Step 4: Prepare Data

The `users.csv` file contains user data. Place it inside the `data/` folder:

```csv
user_id,name,email,school,company,role,location
u001,Raj Purohith,raj@example.com,TAMU,OpenAI,Data Scientist,College Station
u002,Alice Smith,alice@example.com,MIT,Google,Software Engineer,Boston
...
```

### Step 5: Run the Code

#### 5.1 Load User Profiles into DuckDB

```bash
python ingest/load_profiles.py
```

#### 5.2 Parse Bios from PDFs to JSONL

```bash
python ingest/parse_bios.py
```

#### 5.3 Embed Bios and Upload to Qdrant

```bash
python recommenders/semantic_indexer.py
```

#### 5.4 Test Semantic Search

Test the recommendation engine by searching for similar bios.

```bash
python recommenders/semantic_search.py
```

---

### 📝 How it Works

1. **Data Ingestion**:

   * Load user data from a CSV file.
   * Parse bios from LinkedIn, resumes, or other sources into structured text.

2. **Semantic Search**:

   * Create embeddings of bios using a **Sentence Transformer** model.
   * Store and index the embeddings in **Qdrant** for efficient similarity search.

3. **Graph Relationships**:

   * Build relationships between users based on shared institutions (schools, companies).
   * Store the relationships in **Neo4j** for visualization and advanced querying.

---

### 🛠️ Docker Commands

* **Start Qdrant**:

  ```bash
  docker start qdrant
  ```

* **Start Neo4j**:

  ```bash
  docker start neo4j
  ```

* **Stop All Containers**:

  ```bash
  docker stop $(docker ps -aq)
  ```

* **Remove All Containers**:

  ```bash
  docker rm $(docker ps -aq)
  ```

---

### 🐳 Docker Compose (Optional)

For easier management, you can use Docker Compose by creating a `docker-compose.yml` file.

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant
    container_name: qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    restart: always

  neo4j:
    image: neo4j:5.14
    container_name: neo4j
    environment:
      - NEO4J_AUTH=neo4j/test123
    ports:
      - "7474:7474"
      - "7687:7687"
    restart: always
```

Run everything at once:

```bash
docker-compose up -d
```

---

### 🚧 Troubleshooting

* **Qdrant connection issue**:

  * Ensure the container is running by checking Docker logs or restarting Qdrant.
  * Ensure that ports `6333` and `6334` are not being blocked by a firewall.

* **Neo4j authentication failure**:

  * Recreate the Neo4j container with correct authentication:

    ```bash
    docker stop neo4j
    docker rm neo4j
    docker run -d -p 7474:7474 -p 7687:7687 --name neo4j -e NEO4J_AUTH=neo4j/test123 neo4j:5.14
    ```

---

### 🚀 Future Enhancements

* Integrate **LinkedIn API** for real-time bio parsing.
* Implement **Confidence scoring** for recommendations.
* Enable **mutual connection visualization** in Neo4j.

---

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

