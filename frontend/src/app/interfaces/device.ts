import { Category } from '#interfaces/category';
import { Location } from '#interfaces/location';
import { Mac } from '#interfaces/mac';
import { Owner } from '#interfaces/owner';

export interface Device {
  id: number;
  name: string | null;
  model: string | null;
  category: Category | null;
  location: Location | null;
  owner: Owner | null;
  macs: Mac[];
  primary_mac: Mac;
}

export interface DeviceRequest {
  name: string | null;
  model: string | null;
  category_id: number | null;
  location_id: number | null;
  owner_id: number | null;
  mac_ids: number[];
}
