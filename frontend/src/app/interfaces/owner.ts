import { Device } from '#interfaces/device';

export interface Owner {
  id: number;
  name: string;
  devices: Device[];
}

export interface OwnerRequest {
  name: string;
  device_ids: number[];
}
