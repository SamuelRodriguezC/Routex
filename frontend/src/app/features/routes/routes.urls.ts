import { Routes } from "@angular/router";
import { RoutesList } from "./routes-list/routes-list";
import { ImportPage } from "./import/import.page";
import { RouteDetail } from "./route-detail/route-detail";

export const ROUTES_URLS: Routes = [
    {path: '', component: RoutesList },
    {path: 'import', component: ImportPage},
    { path: ':id', component: RouteDetail }

]