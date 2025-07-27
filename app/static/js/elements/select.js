export function initSelect(select, options, onChange, placeholder, action) {
  const text = select.querySelector(".select-text");
  const dropdown = select.querySelector(".select-dropdown");

  dropdown.innerHTML = ""; // Remove existing options

  if (placeholder) {
    text.textContent = placeholder;
  }

  console.log(options, onChange, placeholder, action);

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

  // Add options
  options.forEach((option) => {
    const div = document.createElement("div");
    div.className = "select-option";
    div.textContent = option.label;
    div.dataset.value = option.value;
    dropdown.appendChild(div);

    div.addEventListener("click", () => {
      currentValue = option.value;
      text.textContent = option.label;
      select.classList.add("closed");
      dropdown
        .querySelectorAll(".select-option")
        .forEach((o) => o.classList.remove("selected"));
      div.classList.add("selected");
      if (onChange) onChange(option.value);
    });
  });

  // Add action
  if (action) {
    const div = document.createElement("div");
    div.className = "select-option";
    div.textContent = action.label;
    div.dataset.value = 0;
    dropdown.appendChild(div);

    div.addEventListener("click", () => {
      currentValue = 0;
      select.classList.add("closed");
      dropdown
        .querySelectorAll(".select-option")
        .forEach((o) => o.classList.remove("selected"));
      action.run();
    });
  }

  dropdown.style.maxHeight = `${options.length * 39}px`;
  if (action) {
    dropdown.classList.add("actionable");
    dropdown.style.maxHeight = `${(options.length + 1) * 39 + 2}px`;
  }

  // Open/close logic
  select.addEventListener("click", (e) => {
    if (select.classList.contains("disabled")) return;
    select.classList.toggle("closed");
  });
  // Keyboard navigation
  select.addEventListener("keydown", (e) => {
    if (select.classList.contains("disabled")) return;
    if (e.key === "Enter" || e.key === " ") {
      select.classList.toggle("closed");
      e.preventDefault();
    } else if (e.key === "Escape") {
      select.classList.add("closed");
    }
  });
  // Close on outside click
  document.addEventListener("click", (e) => {
    if (!select.contains(e.target)) {
      select.classList.add("closed");
    }
  });
}

export function cleanSelect(select) {
  const parent = select.parentNode;
  const clone = select.cloneNode(true);
  parent.replaceChild(clone, select);
}
