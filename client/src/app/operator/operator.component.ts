import { Component, OnInit, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { KeycloakService } from 'keycloak-angular';

@Component({
  selector: 'app-operator',
  standalone: true,
  imports: [MatButtonModule],
  templateUrl: './operator.component.html',
  styleUrl: './operator.component.scss',
})
export class OperatorComponent implements OnInit {
  keycloakService = inject(KeycloakService);

  ngOnInit(): void {
    this.keycloakService.getToken().then((val) => console.log(val));
    console.log(this.keycloakService.getUsername());
    console.log(this.keycloakService.getUserRoles());
  }

  login(): void {
    this.keycloakService.login();
  }

  logout(): void {
    this.keycloakService.logout();
  }
}
