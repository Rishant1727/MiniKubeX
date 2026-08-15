import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [workers, setWorkers] = useState([]);
  const [deployments, setDeployments] = useState([]);
  const [connected, setConnected] = useState(false);

  const [name, setName] = useState("");
  const [image, setImage] = useState("nginx");
  const [replicas, setReplicas] = useState(1);

  // ==========================================
  // FETCH WORKERS + DEPLOYMENTS
  // ==========================================

  const fetchClusterData = async () => {
    // Workers
    try {
      const workersResponse = await fetch(
        `${API_URL}/cluster/workers`
      );

      if (!workersResponse.ok) {
        throw new Error(
          `Workers API returned ${workersResponse.status}`
        );
      }

      const workersData = await workersResponse.json();

      console.log("WORKER DATA:", workersData);

      setWorkers(
        Array.isArray(workersData)
          ? workersData
          : []
      );

      setConnected(true);
    } catch (error) {
      console.error(
        "Failed to load workers:",
        error
      );

      setWorkers([]);
      setConnected(false);
    }

    // Deployments
    try {
      const deploymentsResponse = await fetch(
        `${API_URL}/deployments`
      );

      if (!deploymentsResponse.ok) {
        throw new Error(
          `Deployments API returned ${deploymentsResponse.status}`
        );
      }

      const deploymentsData =
        await deploymentsResponse.json();

      console.log(
        "DEPLOYMENT DATA:",
        deploymentsData
      );

      setDeployments(
        Array.isArray(deploymentsData)
          ? deploymentsData
          : []
      );
    } catch (error) {
      console.error(
        "Failed to load deployments:",
        error
      );

      setDeployments([]);
    }
  };

  // ==========================================
  // INITIAL LOAD + AUTO REFRESH
  // ==========================================

  useEffect(() => {
    fetchClusterData();

    const interval = setInterval(
      fetchClusterData,
      5000
    );

    return () => {
      clearInterval(interval);
    };
  }, []);

  // ==========================================
  // CREATE DEPLOYMENT
  // ==========================================

  const createDeployment = async () => {
    if (!name.trim()) {
      alert("Please enter a deployment name.");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/deployments`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            name: name.trim(),
            image: image.trim(),
            replicas: Number(replicas),
            cpu_request: 1,
            memory_request: 1
          })
        }
      );

      if (!response.ok) {
        const errorText =
          await response.text();

        throw new Error(errorText);
      }

      console.log(
        "Deployment created successfully."
      );

      setName("");
      setImage("nginx");
      setReplicas(1);

      await fetchClusterData();

    } catch (error) {
      console.error(
        "Deployment creation failed:",
        error
      );

      alert(
        "Failed to create deployment. Check the FastAPI terminal."
      );
    }
  };

  // ==========================================
  // UPDATE DEPLOYMENT
  // ==========================================

  const updateDeployment = async (
  deploymentName,
  currentReplicas
) => {
  const newImage = image.trim();

  if (!newImage) {
    alert("Please enter a Docker image in the image field.");
    return;
  }

  try {
    const response = await fetch(
      `${API_URL}/deployments/${deploymentName}/update`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: deploymentName,
          image: newImage,
          replicas: currentReplicas,
          cpu_request: 1,
          memory_request: 1
        })
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText);
    }

    console.log("Deployment updated successfully.");

    await fetchClusterData();

  } catch (error) {
    console.error("Update failed:", error);
    alert("Failed to update deployment.");
  }
};
  
  // ==========================================
  // UI
  // ==========================================

  return (
    <div className="dashboard">

      {/* HEADER */}

      <header className="header">

        <div>
          <h1>MiniKubeX</h1>

          <p>
            Container Orchestration Dashboard
          </p>
        </div>

        <div>

          <div className="cluster-status">
            {connected
              ? "● Cluster Online"
              : "● Cluster Offline"}
          </div>

          <button
            type="button"
            onClick={fetchClusterData}
          >
            Refresh
          </button>

        </div>

      </header>

      <main>

        {/* STATISTICS */}

        <section className="stats">

          <div className="stat-card">

            <h3>
              Workers
            </h3>

            <strong>
              {workers.length}
            </strong>

          </div>

          <div className="stat-card">

            <h3>
              Deployments
            </h3>

            <strong>
              {deployments.length}
            </strong>

          </div>

          <div className="stat-card">

            <h3>
              Healthy Workers
            </h3>

            <strong>
              {
                workers.filter(
                  (worker) =>
                    worker.healthy === true
                ).length
              }
            </strong>

          </div>

        </section>

        {/* CREATE DEPLOYMENT */}

        <section className="panel">

          <h2>
            Create Deployment
          </h2>

          <div className="deployment-form">

            <input
              type="text"
              placeholder="Deployment name"
              value={name}
              onChange={(event) =>
                setName(event.target.value)
              }
            />

            <input
              type="text"
              placeholder="Docker image"
              value={image}
              onChange={(event) =>
                setImage(event.target.value)
              }
            />

            <input
              type="number"
              min="1"
              value={replicas}
              onChange={(event) =>
                setReplicas(
                  event.target.value
                )
              }
            />

            <button
              type="button"
              onClick={createDeployment}
            >
              Deploy
            </button>

          </div>

        </section>

        {/* WORKERS */}

        <section className="panel">

          <h2>
            Workers
          </h2>

          {workers.length === 0 ? (

            <p>
              No workers registered.
            </p>

          ) : (

            <div className="worker-grid">

              {workers.map(
                (worker) => (

                  <div
                    className="worker-card"
                    key={worker.worker_id}
                  >

                    <div className="worker-header">

                      <strong>
                        {worker.worker_id}
                      </strong>

                      <span
                        className={
                          worker.healthy
                            ? "healthy"
                            : "unhealthy"
                        }
                      >
                        ●
                      </span>

                    </div>

                    <p>
                      CPU:{" "}
                      {worker.cpu_capacity}
                    </p>

                    <p>
                      Memory:{" "}
                      {worker.memory_capacity} GB
                    </p>

                    <p>
                      Host:{" "}
                      {worker.host}
                    </p>

                    <p>
                      Port:{" "}
                      {worker.port}
                    </p>

                    <p>
                      Status:{" "}
                      {worker.healthy
                        ? "Healthy"
                        : "Unhealthy"}
                    </p>

                  </div>

                )
              )}

            </div>

          )}

        </section>

        {/* DEPLOYMENTS */}

        <section className="panel">

          <h2>
            Deployments
          </h2>

          {deployments.length === 0 ? (

            <p>
              No deployments found.
            </p>

          ) : (

            <table>

              <thead>

                <tr>

                  <th>
                    Name
                  </th>

                  <th>
                    Image
                  </th>

                  <th>
                    Replicas
                  </th>

                  <th>
                    Version
                  </th>

                  <th>
                    Status
                  </th>

                  <th>
                    Actions
                  </th>

                </tr>

              </thead>

              <tbody>

                {deployments.map(
                  (deployment) => (

                    <tr
                      key={
                        deployment.name
                      }
                    >

                      <td>
                        {deployment.name}
                      </td>

                      <td>
                        {deployment.image}
                      </td>

                      <td>
                        {
                          deployment.available_replicas ??
                          0
                        }
                        /
                        {
                          deployment.replicas ??
                          0
                        }
                      </td>

                      <td>
                        v
                        {
                          deployment.version ??
                          1
                        }
                      </td>

                      <td>
                        {
                          deployment.status ??
                          "unknown"
                        }
                      </td>

                      <td>

                        <button
                          type="button"
                          onClick={() =>
                           updateDeployment(
                            deployment.name,
                            deployment.replicas
                           )
                          }
                        >
                          Update
                        </button>

                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          )}

        </section>

      </main>

    </div>
  );
}

export default App;