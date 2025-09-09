fetch("/api/hello")
  .then(response => response.json())
  .then(data => {
    document.getElementById("backend-message").innerText = data.message;
  })
  .catch(err => {
    document.getElementById("backend-message").innerText = "Backend not reachable 😢";
  });
