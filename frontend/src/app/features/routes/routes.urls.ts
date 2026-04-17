import { Routes } from "@angular/router";
import { RoutesList } from "./routes-list/routes-list";
import { ImportPage } from "./import/import.page";
import { RouteDetail } from "./route-detail/route-detail";
import { RouteLogs } from "./route-logs/route-logs";

export const ROUTES_URLS: Routes = [
    {path: '', component: RoutesList },
    {path: 'import', component: ImportPage},
    {path: ':id', component: RouteDetail },
    {path: ':id', component: RouteDetail },
    {path: 'logs/:id', component: RouteLogs}


]