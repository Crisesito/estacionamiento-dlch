let availableSpaces = 100;

function updateCounter() {
    document.getElementById('counter').textContent = availableSpaces;
}

function occupySpace() {
    if (availableSpaces > 0) {
        availableSpaces--;
        updateCounter();
    } else {
        alert('No hay más estacionamientos disponibles.');
    }
}

function freeSpace() {
    if (availableSpaces < 100) {
        availableSpaces++;
        updateCounter();
    } else {
        alert('Todos los estacionamientos están libres.');
    }
}

// Resetear el contador a las 12:00 AM todos los días
function resetCounterAtMidnight() {
    const now = new Date();
    const midnight = new Date();
    midnight.setHours(24, 0, 0, 0);

    const timeUntilMidnight = midnight - now;

    setTimeout(function() {
        availableSpaces = 100;
        updateCounter();
        resetCounterAtMidnight(); // Volver a llamar la función para el próximo día
    }, timeUntilMidnight);
}

// Iniciar el contador y la función de reset
updateCounter();
resetCounterAtMidnight();
