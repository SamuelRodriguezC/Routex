export interface ImportResult {
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  errors: { row: number; messages: string[] }[];
  message: string;
}