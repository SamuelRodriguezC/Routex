import { Routes } from "@angular/router";
import { RoutesList } from "./routes-list/routes-list";
import { ImportPage } from "./import/import.page";

export const ROUTES_URLS: Routes = [
    {path: '', component: RoutesList },
    {path: 'import', component: ImportPage}
]