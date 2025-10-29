import { Mac } from './mac';

export interface Port {
  id: number;
  number: number;
  protocol: string;
  service: string;
  banner?: string;
  state: string;
  mac: Mac;
}
