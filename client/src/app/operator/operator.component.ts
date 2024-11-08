import { Component, OnInit, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { KeycloakService } from 'keycloak-angular';
import { RxStompService } from '../rx-stomp.service';

@Component({
  selector: 'app-operator',
  standalone: true,
  imports: [MatButtonModule],
  templateUrl: './operator.component.html',
  styleUrl: './operator.component.scss',
})
export class OperatorComponent implements OnInit {
  keycloakService = inject(KeycloakService);
  rxStompService = inject(RxStompService);

  ngOnInit(): void {
    this.keycloakService.getToken().then((val) => console.log(val));

    this.rxStompService
      .watch('/exchange/broadcast-exchange')
      .subscribe((message) => {
        console.log('Received message:', message);
      });
  }

  login(): void {
    this.keycloakService.login();
  }

  logout(): void {
    this.keycloakService.logout();
  }
}