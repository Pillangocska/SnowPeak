import { Injectable, inject } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';

@Injectable({
  providedIn: 'root',
})
export class InternalKeycloakService {
  keycloakService = inject(KeycloakService);

  getUserId(): string | undefined {
    return this.keycloakService.getKeycloakInstance().subject;
  }
}
