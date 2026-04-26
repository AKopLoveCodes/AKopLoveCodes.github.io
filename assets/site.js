const progress = document.getElementById("progress");
const glow = document.getElementById("cursorGlow");

function updateProgress() {
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const height = document.documentElement.scrollHeight - window.innerHeight;
  const pct = height > 0 ? (scrollTop / height) * 100 : 0;
  progress.style.width = `${pct}%`;
}

window.addEventListener("scroll", updateProgress, { passive: true });
updateProgress();

window.addEventListener(
  "pointermove",
  (event) => {
    if (!glow) {
      return;
    }

    glow.style.left = `${event.clientX}px`;
    glow.style.top = `${event.clientY}px`;
  },
  { passive: true },
);

document.querySelectorAll(".card").forEach((card) => {
  card.addEventListener("pointermove", (event) => {
    const rect = card.getBoundingClientRect();
    card.style.setProperty("--mx", `${event.clientX - rect.left}px`);
    card.style.setProperty("--my", `${event.clientY - rect.top}px`);
  });
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.16 },
);

document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));
