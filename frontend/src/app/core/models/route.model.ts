import { Status } from "./status.model";

export interface Route {
  id: number;
  origin: string;
  destination: string;
  distance_km: number;
  
  time_window_start: string;
  time_window_end: string;

  created_at: string; 
  updated_at: string; 

  status: number;
  priority: number;

  status_detail?: Status; // 👈 importante

}