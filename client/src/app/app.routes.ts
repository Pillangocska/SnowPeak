import { Routes } from '@angular/router';
import { PublicComponent } from './public/public.component';
import { OperatorComponent } from './operator/operator.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'public',
    pathMatch: 'full',
  },
  {
    path: 'public',
    component: PublicComponent,
  },
  {
    path: 'operator',
    component: OperatorComponent,
  },
];
