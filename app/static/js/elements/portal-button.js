import { HTTP_LINK_TITLE } from "../services/constants.js";

class PortalButton {
  constructor(element) {
    this.element = element;
    this.initialised = false;
    this.url = null;

    this.elementOnClick = e => {
      e.preventDefault();
      window.open(this.url, "_blank");
    };
  }

  init(url) {
    this.url = url;
    
    this.clean();

    if (url) {
      this.element.style.display = "";
      this.element.title = HTTP_LINK_TITLE(url);
      this.element.addEventListener("click", this.elementOnClick);
    }
  }

  isInitialised() {
    return this.initialised;
  }

  clean() {
    this.element.title = "";
    this.element.style.display = "none";
    this.element.removeEventListener("click", this.elementOnClick);

    this.initialised = false;
  }
}

export default PortalButton;
