function toggleMenu() {
  const menu = document.querySelector(".menu-links");
  const icon = document.querySelector(".hamburger-icon");
  menu.classList.toggle("open");
  icon.classList.toggle("open");
}

document.getElementById("sendButton").addEventListener("click", function () {
  // Text aus der Textarea abrufen
  var userInput = document.getElementById("userInput").value;

  // Überprüfen, ob der Benutzer Text eingegeben hat
  if (userInput.trim() === "") {
    alert("Bitte geben Sie einen Text ein, bevor Sie ihn senden.");
    return;
  }

  // JSON-Daten für die Anfrage vorbereiten
  var data = JSON.stringify({ user_text: userInput });

  // AJAX-Anfrage an das Backend senden
  var xhr = new XMLHttpRequest();
  xhr.open(
    "POST",
    "https://rkpgmizti5.execute-api.eu-central-1.amazonaws.com/st/text",
    true
  );
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status == 200) {
        // Erfolgreiche Antwort vom Backend
        alert("Ihre Nachricht wurde erfolgreich gesendet!");
        // Optional: Hier könntest du weitere Aktionen ausführen, z.B. die Eingabebox leeren
        document.getElementById("userInput").value = "";
      } else {
        // Fehler beim Senden der Nachricht
        alert(
          "Es gab ein Problem beim Senden Ihrer Nachricht. Bitte versuchen Sie es später erneut."
        );
      }
    }
  };

  // Anfrage senden
  xhr.send(data);
});
