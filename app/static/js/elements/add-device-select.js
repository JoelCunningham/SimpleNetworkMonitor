import Select from "../elements/select.js";

class AddDeviceSelect {
  constructor(element) {
    this.select = new Select(element);
    this.initialised = false;
  }

  init(devices) {
    this.clean();

    const options = [
      ...devices
        .filter(device => device.id && device.name)
        .map(device => ({ value: device.id, label: device.name })),
    ];

    const onChange = value => {
      if (value) {
        // TODO: Implement logic for adding to device
      }
    };
    
    this.select.init(options, null, onChange);
  }

  isInitialised() {
    return this.select.isInitialised();
  }

  clean() {
    if (this.select.isInitialised()) this.select.clean();
    this.initialised = false;
  }
}

export default AddDeviceSelect;
