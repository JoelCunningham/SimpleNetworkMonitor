export interface Option<T> {
  label: string;
  value?: T;
  event?: any;
  selected?: boolean;
}
