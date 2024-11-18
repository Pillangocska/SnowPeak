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
import { StatusPipe } from '../api/shared/pipe/status.pipe';
import { InternalKeycloakService } from '../shared/services/internal-keycloak.service';
import { PublicComponent } from '../public/public.component';

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
    StatusPipe,
    PublicComponent,
  ],
  templateUrl: './operator.component.html',
  styleUrl: './operator.component.scss',
})
export class OperatorComponent implements OnInit {
  @ViewChild('temperatureLogContainer')
  private temperatureLogContainer!: ElementRef;
  @ViewChild('windLogContainer') private windLogContainer!: ElementRef;
  @ViewChild('commandContainer') private commandContainer!: ElementRef;

  keycloakService = inject(KeycloakService);
  internalKeycloakService = inject(InternalKeycloakService);
  rabbitMqService = inject(RabbitmqService);
  rxStompService = inject(RxStompService);
  logService = inject(LogControllerService);
  liftService = inject(LiftControllerService);
  cdr = inject(ChangeDetectorRef);
  dialog = inject(MatDialog);

  liftTemperatureSensorSubscription?: Subscription;
  liftWindSensorSubscription?: Subscription;
  liftStatusSubscription?: Subscription;
  liftCommandSubscription?: Subscription;

  lifts?: Array<PrivateLiftResponseModel>;
  selectedLiftId?: string;

  operatorId?: string;

  liftStatus?: 'FULL_STEAM' | 'HALF_STEAM' | 'STOPPED';

  temperatureLogs: string[] = [];
  windLogs: string[] = [];
  commands: string[] = [];

  message?: string;

  ngOnInit(): void {
    this.keycloakService.getToken().then((val) => console.log(val));

    console.log(this.internalKeycloakService.getUserId());

    this.operatorId = this.internalKeycloakService.getUserId();
    this.liftService
      .getPrivateLiftsByOperatorId({
        operatorId: this.operatorId ?? '',
      })
      .subscribe((lifts) => (this.lifts = lifts));
  }

  private watchSelectedLiftTemperatureSensors(): void {
    console.log(this.selectedLiftId);
    if (this.selectedLiftId) {
      this.liftTemperatureSensorSubscription = this.rabbitMqService
        .watchTemperatureSensorsByLiftId(this.selectedLiftId)
        .subscribe((message: any) => {
          console.log(JSON.parse(message.body));
          this.temperatureLogs = [
            JSON.parse(message.body),
            ...this.temperatureLogs,
          ];
          setTimeout(() => {
            this.scrollToBottom(
              false,
              this.temperatureLogContainer.nativeElement,
            );
          });
        });
    } else {
      this.liftTemperatureSensorSubscription?.unsubscribe();
      this.temperatureLogs = [];
    }
  }

  private watchSelectedLiftWindSensors(): void {
    console.log(this.selectedLiftId);
    if (this.selectedLiftId) {
      this.liftWindSensorSubscription = this.rabbitMqService
        .watchWindSensorsByLiftId(this.selectedLiftId)
        .subscribe((message: any) => {
          console.log(JSON.parse(message.body));
          this.windLogs = [JSON.parse(message.body), ...this.windLogs];
          setTimeout(() => {
            this.scrollToBottom(false, this.windLogContainer.nativeElement);
          });
        });
    } else {
      this.liftWindSensorSubscription?.unsubscribe();
      this.windLogs = [];
    }
  }

  private watchSelectedLiftStatus(): void {
    console.log(this.selectedLiftId);
    if (this.selectedLiftId) {
      this.liftStatusSubscription = this.rabbitMqService
        .watchPublicLiftsMessagesByLiftId(this.selectedLiftId)
        .subscribe((message: any) => {
          console.log(JSON.parse(message.body));
          this.liftStatus = JSON.parse(message?.body)?.skiLiftState;
        });
    } else {
      this.liftStatusSubscription?.unsubscribe();
      this.liftStatus = undefined;
    }
  }

  private watchSelectedLiftCommands(): void {
    console.log(this.selectedLiftId);
    if (this.selectedLiftId) {
      this.liftCommandSubscription = this.rabbitMqService
        .watchCommandsByLiftId(this.selectedLiftId)
        .subscribe((command: any) => {
          console.log(JSON.parse(command.body));
          this.commands = [JSON.parse(command.body), ...this.commands];
          setTimeout(() => {
            this.scrollToBottom(false, this.commandContainer.nativeElement);
          });
        });
    } else {
      this.liftCommandSubscription?.unsubscribe();
      this.commands = [];
    }
  }

  scrollToBottom(force: boolean = false, element: any): void {
    const isAtBottom =
      element.scrollHeight - element.scrollTop <= element.clientHeight + 50;

    if (force || isAtBottom) {
      element.scrollTop = element.scrollHeight;
    }
  }

  goToLift(liftId: string) {
    console.log(liftId);
    this.selectedLiftId = this.selectedLiftId === liftId ? undefined : liftId;
    this.temperatureLogs = [];
    this.windLogs = [];
    this.commands = [];
    this.liftStatus = undefined;

    this.watchSelectedLiftTemperatureSensors();
    this.watchSelectedLiftWindSensors();
    this.watchSelectedLiftStatus();
    this.watchSelectedLiftCommands();
  }

  sendMessage() {
    console.log(this.message);
    let body: any = {};
    body.messageKind = 'suggestion';
    body.severity = 'INFO';
    body.message = this.message;
    body.user = this.operatorId;
    body.timestamp = new Date().toISOString().slice(0, -1);
    this.rabbitMqService.sendSuggestion(this.selectedLiftId ?? '', body);
    this.message = undefined;
  }

  emergencyStop() {
    const dialogRef = this.dialog.open(EmergencyStopDialogComponent);

    dialogRef.afterClosed().subscribe((result) => {
      if (result && this.selectedLiftId) {
        result.user = this.operatorId;
        result.timestamp = new Date().toISOString().slice(0, -1);
        this.rabbitMqService.sendEmergencyStop(this.selectedLiftId, result);
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
