import { CommonModule } from '@angular/common';
import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
  inject,
} from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { KeycloakService } from 'keycloak-angular';
import { PrivateLiftResponseModel } from '../api/models';
import { LiftControllerService, LogControllerService } from '../api/services';
import { RxStompService } from '../rx-stomp.service';
import { FormsModule } from '@angular/forms';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { EmergencyStopDialogComponent } from '../shared/components/emergency-stop-dialog/emergency-stop-dialog.component';
import { Subscription } from 'rxjs';
import { RabbitmqService } from '../shared/services/rabbitmq.service';

@Component({
  selector: 'app-operator',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatChipsModule,
    MatDividerModule,
    MatCardModule,
    MatDialogModule,
  ],
  templateUrl: './operator.component.html',
  styleUrl: './operator.component.scss',
})
export class OperatorComponent implements OnInit {
  @ViewChild('logContainer') private logContainer!: ElementRef;

  keycloakService = inject(KeycloakService);
  rabbitMqService = inject(RabbitmqService);
  rxStompService = inject(RxStompService);
  logService = inject(LogControllerService);
  liftService = inject(LiftControllerService);
  cdr = inject(ChangeDetectorRef);
  dialog = inject(MatDialog);

  liftSubscription?: Subscription;

  lifts?: Array<PrivateLiftResponseModel>;
  selectedLiftId?: string;

  liftStatus: 'FULL_STEAM' | 'HALF_STEAM' | 'STOPPED' = 'HALF_STEAM';

  logs: string[] = [];

  message?: string;

  ngOnInit(): void {
    this.keycloakService.getToken().then((val) => console.log(val));

    this.liftService
      .getPrivateLiftsByOperatorId({
        operatorId: 'b21f687b-02fc-4556-b2a4-17a9eb905033',
      })
      .subscribe((lifts) => (this.lifts = lifts));
  }

  private watchSelectedLift(): void {
    console.log(this.selectedLiftId);
    if (this.selectedLiftId) {
      this.liftSubscription = this.rabbitMqService
        .watchSensorsByLiftId(this.selectedLiftId)
        .subscribe((message: any) => {
          console.log(JSON.parse(message.body));
          this.logs = [JSON.parse(message.body), ...this.logs];
          setTimeout(() => {
            this.scrollToBottom();
          });
        });
    } else {
      this.liftSubscription?.unsubscribe();
    }
  }

  scrollToBottom(force: boolean = false): void {
    const element = this.logContainer.nativeElement;
    const isAtBottom =
      element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

    if (force || isAtBottom) {
      element.scrollTop = element.scrollHeight;
    }
  }

  goToLift(liftId: string) {
    console.log(liftId);
    this.selectedLiftId = this.selectedLiftId === liftId ? undefined : liftId;
    this.logs = [];

    this.watchSelectedLift();
  }

  sendMessage() {
    console.log(this.message);
    this.message = undefined;
  }

  emergencyStop() {
    const dialogRef = this.dialog.open(EmergencyStopDialogComponent);

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        console.log('EMERGENCY STOP');
      }
    });
  }

  login(): void {
    this.keycloakService.login();
  }

  logout(): void {
    this.keycloakService.logout();
  }
}
