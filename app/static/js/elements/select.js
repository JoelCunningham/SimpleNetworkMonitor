import { getElement } from "../services/common.js";

class Select {
  constructor(element) {
    this.element = element;
    this.initialised = false;
    this.value = null;

    this.text = getElement(".select-text", element);
    this.dropdown = getElement(".select-dropdown", element);
    this.placeholder = this.text.textContent;

    this.elementOnClick = () => {
      if (this.getState() === SelectState.OPEN) {
        this.setState(SelectState.CLOSED);
      } else {
        this.setState(SelectState.OPEN);
      }
    };
    this.elementOnKeyDown = event => {
      if (event.key === "Enter" || event.key === " ") {
        if (this.getState() === SelectState.OPEN) {
          this.setState(SelectState.CLOSED);
        } else {
          this.setState(SelectState.OPEN);
        }
      } else if (event.key === "Escape") {
        if (this.getState() === SelectState.OPEN) {
          this.setState(SelectState.CLOSED);
        }
      }
      event.preventDefault();
    };
    this.documentOnClick = event => {
      if (!this.element.contains(event.target)) {
        if (this.getState() === SelectState.OPEN) {
          this.setState(SelectState.CLOSED);
        }
      }
    };
  }

  /* Construction methods --------------------------------------------------- */

  init(options, action, onChange = null) {
    this.clean();

    if (!options || options.length === 0) {
      this.setState(SelectState.DISABLED);
      return;
    }

    options.forEach(option => {
      this.addOption(option.value, option.label, onChange);
    });
    if (action) {
      this.addAction(action.label, action.run, action.icon);
    }

    this.dropdown.style.maxHeight = `${options.length * 39}px`;
    if (action) {
      this.dropdown.classList.add("actionable");
      this.dropdown.style.maxHeight = `${(options.length + 1) * 39 + 2}px`;
    }

    this.element.addEventListener("click", this.elementOnClick);
    this.element.addEventListener("keydown", this.elementOnKeyDown);
    document.addEventListener("click", this.documentOnClick);
  }

  addOption(value, label, onChange) {
    const option = document.createElement("div");
    option.className = "select-option";
    option.textContent = label;
    this.dropdown.appendChild(option);

    option.addEventListener("click", () => {
      this.setValue(value, label, option);
      this.setState(SelectState.CLOSED);
      if (onChange) onChange(value);
    });
  }

  addAction(label, runAction, icon) {
    const action = document.createElement("div");
    action.className = "select-option action";
    action.textContent = label;
    action.style.backgroundImage = icon ? `url(${icon})` : "";
    this.dropdown.appendChild(action);

    action.addEventListener("click", () => {
      this.unsetValue();
      this.setState(SelectState.CLOSED);
      runAction();
    });
  }

  /* Value management methods ----------------------------------------------- */

  getValue() {
    return this.value;
  }

  setValue(value, label, option) {
    this.value = value;
    this.text.textContent = label;

    const selected = getElement(".selected", this.dropdown);
    if (selected) selected.classList.remove("selected");
    if (option) option.classList.add("selected");
  }

  unsetValue() {
    this.value = null;
    this.text.textContent = this.placeholder;

    const selected = getElement(".selected", this.dropdown);
    if (selected) selected.classList.remove("selected");
  }

  /* State management methods ----------------------------------------------- */

  setState(state) {
    if (this.getState() === state) return;
    this.clearState();

    switch (state) {
      case SelectState.ERROR:
        this.element.classList.add("error");
      case SelectState.CLOSED:
        this.element.classList.add("closed");
        break;
      case SelectState.DISABLED:
        this.element.classList.add("disabled");
        this.element.setAttribute("disabled", "true");
        this.element.setAttribute("aria-disabled", "true");
        break;
    }
  }

  getState() {
    const classes = this.element.classList;
    if (classes.contains("error")) return SelectState.ERROR;
    if (classes.contains("closed")) return SelectState.CLOSED;
    if (classes.contains("disabled")) return SelectState.DISABLED;
    return SelectState.OPEN;
  }

  clearState() {
    this.element.classList.remove("closed", "disabled", "error");
    this.element.removeAttribute("disabled");
    this.element.removeAttribute("aria-disabled");
  }

  /* Cleanup methods -------------------------------------------------------- */

  isInitialised() {
    return this.initialised;
  }

  clean() {
    this.element.classList.add("closed");
    this.element.classList.remove("error");

    this.element.classList.remove("disabled");
    this.element.removeAttribute("aria-disabled");

    this.text.textContent = this.placeholder;

    // Clean the dropdown and remove event listeners
    this.dropdown.innerHTML = "";

    this.element.removeEventListener("click", this.elementOnClick);
    this.element.removeEventListener("keydown", this.elementOnKeyDown);
    document.removeEventListener("click", this.documentOnClick);

    this.initialised = false;
  }
}

const SelectState = {
  OPEN: "OPEN",
  CLOSED: "CLOSED",
  DISABLED: "DISABLED",
  ERROR: "ERROR",
};

export default Select;

export { SelectState };

