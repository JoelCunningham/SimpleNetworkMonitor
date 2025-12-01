import { Port } from '#interfaces';

export interface PortInfo {
  port: Port;
  isHttp: boolean;
  address?: string;
}
