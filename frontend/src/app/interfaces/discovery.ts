import { Mac } from '#interfaces/mac';

export interface Discovery {
  id: number;
  protocol: string;
  device_name: string;
  device_type: string;
  manufacturer?: string;
  model?: string;
  mac: Mac;
}
