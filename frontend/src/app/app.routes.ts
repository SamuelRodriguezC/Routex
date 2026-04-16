import { Routes } from '@angular/router';

export const routes: Routes = [
//   {
//     path: '',
//     loadComponent: () =>
//       import('./features/dashboard/dashboard.page')
//         .then(m => m.DashboardPage)
//   },
  {
    path: 'routes',
    loadChildren: () => import('./features/routes/routes.urls')
      .then(m => m.ROUTES_URLS)
  },
//   {
//     path: 'logs',
//     loadComponent: () =>
//       import('./features/execution-logs/pages/logs.page')
//         .then(m => m.LogsPage)
//   }
  {
    path: 'import',
    loadComponent: () =>
      import('./features/routes/import/import.page')
        .then(m => m.ImportPage)
  }
];
