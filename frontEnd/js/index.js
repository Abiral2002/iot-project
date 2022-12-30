(() => {
  const image = document.querySelector(".image");
  const app_screen= document.querySelector(".app")
  const lock_screen= document.querySelector(".login")
  const notification = document.querySelector(".notification");
  const status = document.querySelector(".status");
  const password = document.querySelector(".password");
  const styles = getComputedStyle(document.documentElement);
  document
    .querySelector(".password-submit")
    .addEventListener("click", onPasswordSubmit);
  document.querySelector(".open-button").addEventListener("click", onOpen);
  document.querySelector(".close-button").addEventListener("click", onClose);

  function onPasswordSubmit(e) {
    e.preventDefault()
    fetch("http://127.0.0.1:8000/login", {
      method: "post",
      credentials:true,
      body:JSON.stringify({password:password.value}),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
      .then(async (res) => {
        const resp = await res.json();
        if (resp.msg == "success") {
          lock_screen.style.display="none"
          app_screen.style.display="flex"
          notification.style.transform = "scaleY(1)";
          notification.innerText = "Logged In";
          setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
          status.innerText = "Open";
          status.style.borderColor = styles.getPropertyValue("--open");
          status.style.color = styles.getPropertyValue("--open");
        }
      })
      .catch(console.log);
  }

  function onOpen() {
    fetch("http://127.0.0.1:8000/open-lock", { method: "get" })
      .then(async (res) => {
        const resp = await res.json();
        if (resp.msg == "Lock was closed") {
          notification.style.transform = "scaleY(1)";
          notification.innerText = "Door unlocked";
          setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
          status.innerText = "Open";
          status.style.borderColor = styles.getPropertyValue("--open");
          status.style.color = styles.getPropertyValue("--open");
        }
      })
      .catch(console.log);
  }

  function onClose() {
    fetch("http://127.0.0.1:8000/close-lock", { method: "get" }).then(
      async (res) => {
        const resp = await res.json();
        if (resp.msg == "Lock was closed")
          notification.style.transform = "scaleY(1)";
        notification.innerText = "Door locked";
        setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
        status.innerText = "Locked";
        status.style.borderColor = styles.getPropertyValue("--close");
        status.style.color = styles.getPropertyValue("--close");
      }
    );
  }

  function getting_data() {
    const socket = new WebSocket("ws://127.0.0.1:8000/camera");

    socket.onopen = function () {
      notification.innerText = "Connection established";
      notification.style.backgroundColor = styles.getPropertyValue("--open");
      notification.style.transform = "scaleY(1)";

      setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
    };

    socket.onmessage = async function (event) {
      const arrayData = event.data;
      const blob = new Blob([arrayData]);
      const url = URL.createObjectURL(blob);
      image.src = url;
    };

    socket.onclose = function () {
      notification.innerText = "Connection closed";
      status.innerText = "X";
      status.style.borderColor = styles.getPropertyValue("--close");
      status.style.color = styles.getPropertyValue("--close");
      notification.style.backgroundColor = styles.getPropertyValue("--close");
      notification.style.transform = "scaleY(1)";
      setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
    };

    socket.onerror = function (error) {
      notification.innerText = "Error occured closed";
      notification.style.transform = "scaleY(1)";
      setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
    };

    socket.send("Hello");
  }
  getting_data();
})();