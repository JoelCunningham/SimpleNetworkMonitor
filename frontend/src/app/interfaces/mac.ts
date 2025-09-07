import { Device } from '#interfaces/device';
import { Discovery } from '#interfaces/discovery';
import { Port } from '#interfaces/port';

export interface Mac {
  id: number;
  address: string;
  last_ip: string;
  last_seen: string;
  ping_time_ms?: number | null;
  arp_time_ms?: number | null;
  hostname?: string | null;
  vendor?: string | null;
  os_guess?: string | null;
  ttl?: number | null;
  device?: Device | null;
  ports?: Port[] | null;
  discoveries?: Discovery[] | null;
}
