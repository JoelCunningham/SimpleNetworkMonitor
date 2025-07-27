export function initSelect(select, options, onChange, placeholder) {
  const text = select.querySelector(".select-text");
  const dropdown = select.querySelector(".select-dropdown");

  text.textContent = placeholder;
  dropdown.innerHTML = ""; // Remove existing options

  if (!options || options.length === 0) {
    select.classList.add("disabled");
    select.setAttribute("aria-disabled", "true");
    select.addEventListener("click", (e) => {
      e.stopPropagation();
      e.preventDefault();
    });
    return;
  }
  select.classList.remove("disabled");
  select.removeAttribute("aria-disabled");

  options.forEach((option) => {
    console.log("Adding option:", option);
    const div = document.createElement("div");
    div.className = "select-option";
    div.textContent = option.label;
    div.dataset.value = option.value;
    dropdown.appendChild(div);

    div.addEventListener("click", () => {
      currentValue = option.value;
      text.textContent = option.label;
      select.classList.remove("open");
      dropdown
        .querySelectorAll(".select-option")
        .forEach((o) => o.classList.remove("selected"));
      div.classList.add("selected");
      if (onChange) onChange(option.value);
    });
  });

  // Open/close logic
  select.addEventListener("click", (e) => {
    if (select.classList.contains("disabled")) return;
    select.classList.toggle("open");
  });
  // Keyboard navigation
  select.addEventListener("keydown", (e) => {
    if (select.classList.contains("disabled")) return;
    if (e.key === "Enter" || e.key === " ") {
      select.classList.toggle("open");
      e.preventDefault();
    } else if (e.key === "Escape") {
      select.classList.remove("open");
    }
  });
  // Close on outside click
  document.addEventListener("click", (e) => {
    if (!select.contains(e.target)) {
      select.classList.remove("open");
    }
  });
}

export function cleanSelect(select) {
  const parent = select.parentNode;
  const clone = select.cloneNode(true);
  parent.replaceChild(clone, select);
}
