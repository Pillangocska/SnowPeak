import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';

import { catchError, from, of, switchMap } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const keycloakService = inject(KeycloakService);

  return from(keycloakService.getToken()).pipe(
    switchMap((token) => {
      const requestWithAuth = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`,
        },
      });
      return of(requestWithAuth);
    }),
    catchError(() => {
      return of(req);
    }),
    switchMap((finalRequest) => next(finalRequest)),
  );
};
