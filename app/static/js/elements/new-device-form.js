import Select, { SelectState } from "../elements/select.js";
import { getElement } from "../common.js";
import { ENDPOINT } from "../constants.js";

class NewDeviceForm {
  constructor(element) {
    this.element = element;
    this.initialised = false;
    this.macs = null;

    this.modalInput = getElement("#deviceModelInput");
    this.categorySelect = new Select(getElement("#categorySelect"));
    this.locationSelect = new Select(getElement("#locationSelect"));
    this.ownerSelect = new Select(getElement("#ownerSelect"));

    this.cancelButton = getElement("#cancelDeviceButton");
    this.submitButton = getElement("#submitDeviceButton");

    this.onCancel = null;
    this.onSuccess = null;

    this.cancelButtonOnClick = event => {
      event.preventDefault();
      this.onCancel();
      this.clean();
    };
    this.submitButtonOnClick = async event => {
      event.preventDefault();
      const device = await this.saveDevice();
      if (device) this.onSuccess(device);
      this.clean();
    };
  }

  /* Construction methods --------------------------------------------------- */

  async init(macs, onCancel, onSuccess) {
    this.macs = macs;
    this.onCancel = onCancel;
    this.onSuccess = onSuccess;

    this.clean();

    const ownerAction = {
      label: "Add owner",
      icon: "/static/icons/add.svg",
      run: () => {
        this.clean();
        // TODO: Implement redirect to add owner page
      }
    };

    const options = await fetch(ENDPOINT.OPTIONS).then(res => res.json());

    const categories = this.getOptions(options.categories, "category");
    const locations = this.getOptions(options.locations, "location", true);
    const owners = this.getOptions(options.owners, "owner", true);

    this.categorySelect.init(categories, null);
    this.locationSelect.init(locations, null);
    this.ownerSelect.init(owners, ownerAction);

    this.cancelButton.addEventListener("click", this.cancelButtonOnClick);
    this.submitButton.addEventListener("click", this.submitButtonOnClick);

    this.show();
  }

  getOptions(items, fieldName, nullable) {
    const options = items.map(item => ({
      value: item.id,
      label: item.name,
    }));
    if (nullable) {
      options.push({
        value: 0,
        label: `No ${fieldName}`,
      });
    }
    return options;
  }

  /* Action methods --------------------------------------------------------- */

  async saveDevice() {
    const deviceData = {
      model: this.modalInput.value,
      category_id: this.categorySelect.getValue(),
      location_id: this.locationSelect.getValue(),
      owner_id: this.ownerSelect.getValue(),
      mac_ids: this.macs.map(mac => mac.id),
    };

    let hasError = false;
    if (!deviceData.category_id) {
      this.categorySelect.setState(SelectState.ERROR);
      hasError = true;
    }
    if (!deviceData.location_id) {
      this.locationSelect.setState(SelectState.ERROR);
      hasError = true;
    }
    if (!deviceData.owner_id && deviceData.owner_id !== 0) {
      this.ownerSelect.setState(SelectState.ERROR);
      hasError = true;
    }
    if (hasError) return false;

    try {
      const response = await fetch(ENDPOINT.ADD_DEVICE, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(deviceData),
      });
      const device = await response.json();
      return device;
    } catch (error) {
      console.error("Error saving device:", error);
    }
    return false;
  }

  show() {
    this.element.style.display = "";
  }

  hide() {
    this.element.style.display = "none";
  }

  /* Cleanup methods -------------------------------------------------------- */

  isInitialised() {
    return this.initialised;
  }

  clean() {
    this.hide();

    this.element.reset();

    if (this.categorySelect.isInitialised()) this.categorySelect.clean();
    if (this.locationSelect.isInitialised()) this.locationSelect.clean();
    if (this.ownerSelect.isInitialised()) this.ownerSelect.clean();

    this.cancelButton.removeEventListener("click", this.cancelButtonOnClick);
    this.submitButton.removeEventListener("click", this.submitButtonOnClick);

    this.initialised = false;
  }
}

export default NewDeviceForm;
