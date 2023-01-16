(() => {
  const image = document.querySelector(".image");
  const app_screen = document.querySelector(".app");
  const lock_screen = document.querySelector(".login");
  const notification = document.querySelector(".notification");
  const status = document.querySelector(".status");
  const password = document.querySelector(".password");
  const styles = getComputedStyle(document.documentElement);
  const open = document.querySelector(".open-button");
  const close = document.querySelector(".close-button");
  document
    .querySelector(".password-submit")
    .addEventListener("click", onPasswordSubmit);
  open.addEventListener("click", onOpen);
  close.addEventListener("click", onClose);

  function screen_apper() {
    lock_screen.style.display = "none";
    app_screen.style.display = "flex";
    notification.style.transform = "scaleY(1)";
    notification.innerText = "Logged In";
    setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
    status.innerText = "Open";
    status.style.borderColor = styles.getPropertyValue("--open");
    status.style.color = styles.getPropertyValue("--open");
    fetch("/status", { method: "get" }).then(async (req) => {
      let requ = await req.json();
      if (requ.msg == "Open") {
        status.innerText = "Open";

        status.style.borderColor = styles.getPropertyValue("--open");
        status.style.color = styles.getPropertyValue("--open");
      } else {
        status.innerText = "Locked";
        status.style.borderColor = styles.getPropertyValue("--close");
        status.style.color = styles.getPropertyValue("--close");
      }
    });
    getting_data();
  }

  function onPasswordSubmit(e) {
    e.preventDefault();
    fetch("/login", {
      method: "post",
      body: JSON.stringify({ password: password.value }),
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(async (res) => {
        const resp = await res.json();
        if (resp.msg == "success") {
          screen_apper();
        }
      })
      .catch(console.log);
  }

  function onOpen() {
    open.disabled = true;
    fetch("/open-lock", { method: "get" })
      .then(async (res) => {
        const resp = await res.json();
        notification.innerText = "Door unlocked";
        open.disabled = false;
        if (resp.msg == "Lock opened") {
          notification.style.transform = "scaleY(1)";
          setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
          status.innerText = "Open";
          status.style.borderColor = styles.getPropertyValue("--open");
          status.style.color = styles.getPropertyValue("--open");
        }
      })
      .catch(() => {
        open.disabled = false;
      });
  }

  function onClose() {
    close.disabled = true;
    fetch("/close-lock", { method: "get" })
      .then(async (res) => {
        const resp = await res.json();
        close.disabled = false;
        if (resp.msg == "Lock closed")
          notification.style.transform = "scaleY(1)";
        notification.innerText = "Door locked";
        setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
        status.innerText = "Locked";
        status.style.borderColor = styles.getPropertyValue("--close");
        status.style.color = styles.getPropertyValue("--close");
      })
      .catch(() => {
        close.disabled = false;
      });
  }

  function getting_data() {
    const socket = new WebSocket("ws://192.168.1.74:8000/camera");

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
})();
