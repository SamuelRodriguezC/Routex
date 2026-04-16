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
    loadComponent: () =>
      import('./features/routes/routes.component')
        .then(m => m.RoutesComponent)
  },
//   {
//     path: 'logs',
//     loadComponent: () =>
//       import('./features/execution-logs/pages/logs.page')
//         .then(m => m.LogsPage)
//   }
];
