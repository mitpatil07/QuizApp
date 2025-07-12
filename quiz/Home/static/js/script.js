const questionCards = document.querySelectorAll('.question-card');
const navButtons = document.querySelectorAll('.question-number');
const timerElement = document.getElementById('time');

let current = 0;
const total = questionCards.length;

function showQuestion(index) {
    questionCards.forEach(q => q.classList.remove('active'));
    navButtons.forEach(btn => btn.classList.remove('active'));
    questionCards[index].classList.add('active');
    navButtons[index].classList.add('active');
    current = index;
    document.querySelector('.right-panel').scrollTo({ top: 0, behavior: 'smooth' });
}

function nextQuestion() {
    if (current < total - 1) showQuestion(current + 1);
}

function prevQuestion() {
    if (current > 0) showQuestion(current - 1);
}

navButtons.forEach((btn, index) => {
    btn.addEventListener('click', () => showQuestion(index));
});

document.querySelectorAll('input[type="radio"]').forEach(input => {
    input.addEventListener('change', function () {
        const index = Array.from(questionCards).findIndex(card => card.contains(this));
        navButtons[index].classList.add('answered');
    });
});

// Timer
let totalSeconds = 5 * 60;
function updateTimer() {
    const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, '0');
    const seconds = String(totalSeconds % 60).padStart(2, '0');
    timerElement.textContent = `${minutes}:${seconds}`;
    if (totalSeconds === 0) {
        document.getElementById("quiz-form").submit();
    } else {
        totalSeconds--;
        setTimeout(updateTimer, 1000);
    }
}

updateTimer();
showQuestion(0);

// Tab/Window Restriction
let warningCount = 0;
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        warningCount++;
        alert("Tab switching is not allowed!");
        if (warningCount >= 3) document.getElementById("quiz-form").submit();
    }
});

// window.addEventListener('blur', () => {
//     warningCount++;
//     alert("Window focus lost!");
//     if (warningCount >= 3) document.getElementById("quiz-form").submit();
// });

// Optional: Disable right-click & F12
document.addEventListener("contextmenu", e => e.preventDefault());
document.onkeydown = function (e) {
    if (e.key === "F12" || (e.ctrlKey && e.shiftKey && e.key === "I")) {
        alert("Developer tools are disabled.");
        return false;
    }
};

function enterFullScreen() {
    const docEl = document.documentElement;
    if (docEl.requestFullscreen) {
        docEl.requestFullscreen();
    } else if (docEl.mozRequestFullScreen) {
        docEl.mozRequestFullScreen(); // Firefox
    } else if (docEl.webkitRequestFullscreen) {
        docEl.webkitRequestFullscreen(); // Chrome, Safari and Opera
    } else if (docEl.msRequestFullscreen) {
        docEl.msRequestFullscreen(); // IE/Edge
    }
}

// Call it on load
window.addEventListener('load', () => {
    enterFullScreen();
});

// Strong check: detect page reloads using Navigation API
window.addEventListener('load', function () {
    if (performance.navigation.type === performance.navigation.TYPE_RELOAD) {
      alert("Page reload is not allowed during the quiz!");
      window.location.href = "/"; // or any fallback redirect
    }
  });
  
  // Modern browsers use this for reload detection (fallback)
  window.addEventListener("pageshow", function (event) {
    if (event.persisted) {
      alert("Back/Reload not allowed!");
      window.location.href = "/";
    }
  });

  document.querySelectorAll('input[type="radio"]').forEach(input => {
    input.addEventListener('change', function () {
      localStorage.setItem(this.name, this.value);
    });
  });

  
  window.addEventListener('load', () => {
    for (let key in localStorage) {
      if (document.getElementsByName(key).length > 0) {
        let val = localStorage.getItem(key);
        let radio = document.querySelector(`input[name="${key}"][value="${val}"]`);
        if (radio) radio.checked = true;
      }
    }
  });
  