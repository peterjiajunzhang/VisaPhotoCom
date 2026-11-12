const filterButtons = document.querySelectorAll("[data-filter]");
const appCards = document.querySelectorAll(".app-card");
filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const selected = button.dataset.filter;
    filterButtons.forEach((item) =>
      item.setAttribute("aria-pressed", String(item === button)),
    );
    let visibleCount = 0;
    appCards.forEach((card) => {
      const visible =
        selected === "all" ||
        card.dataset.platform.split(" ").includes(selected);
      card.hidden = !visible;
      if (visible) visibleCount += 1;
    });
    document.querySelector("#filter-status").textContent =
      `${visibleCount} ${visibleCount === 1 ? "app" : "apps"} shown`;
  });
});
