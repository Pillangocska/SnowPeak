import { LeafletModule } from '@asymmetrik/ngx-leaflet';
import { AfterViewInit, Component, OnInit, inject } from '@angular/core';
import L, * as Leaflet from 'leaflet';
import { LatLngExpression } from 'leaflet';
import { LiftControllerService } from '../api/services';
import { LiftResponseModel } from '../api/models';
import { RabbitmqService } from '../shared/services/rabbitmq.service';

@Component({
  selector: 'app-public',
  standalone: true,
  imports: [LeafletModule],
  templateUrl: './public.component.html',
  styleUrl: './public.component.scss',
})
export class PublicComponent implements OnInit, AfterViewInit {
  map: any;
  private liftLayers: Map<
    string,
    { polyline?: L.Polyline; tooltip?: L.Tooltip }
  > = new Map();

  liftService = inject(LiftControllerService);
  rabbitMqService = inject(RabbitmqService);

  lifts?: Array<LiftResponseModel>;

  publicMessages: Array<any> = [];

  constructor() {}

  ngOnInit(): void {
    this.liftService.getPublicLifts().subscribe((lifts) => {
      this.lifts = lifts;
      this.drawLifts();
    });

    this.rabbitMqService
      .watchPublicLiftsMessages()
      .subscribe((publicLiftMessage) => {
        console.log(publicLiftMessage);
        this.publicMessages.unshift(publicLiftMessage);
        this.drawLifts();
      });
  }

  ngAfterViewInit(): void {
    this.map = L.map('map', {
      dragging: false,
      zoomControl: false,
      doubleClickZoom: false,
      touchZoom: false,
      scrollWheelZoom: false,
    }).setView([46.69677386797277, 13.914833305225734], 14);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
    } as Leaflet.TileLayerOptions).addTo(this.map);
  }

  private clearLiftLayers(liftId: string): void {
    const layers = this.liftLayers.get(liftId);
    if (layers) {
      if (layers.polyline) {
        this.map.removeLayer(layers.polyline);
      }
      if (layers.tooltip) {
        this.map.removeLayer(layers.tooltip);
      }
    }
  }

  drawLifts(): void {
    console.log(this.lifts);
    this.lifts?.forEach((lift) => {
      if (lift.id) {
        this.clearLiftLayers(lift.id);
      }

      const startPoint = new Leaflet.LatLng(
        lift.startLatitude ?? 0,
        lift.startLongitude ?? 0,
      );
      const endPoint = new Leaflet.LatLng(
        lift.endLatitude ?? 0,
        lift.endLongitude ?? 0,
      );

      const latlngs = [startPoint, endPoint] as LatLngExpression[];

      const latestLiftPublicMessage = this.publicMessages.find(
        (message) => message.headers.lift_id === lift.id,
      );

      const messageBody = latestLiftPublicMessage?.body
        ? JSON.parse(latestLiftPublicMessage?.body)
        : undefined;

      console.log(messageBody);

      var lineColor = 'grey';

      if (messageBody?.waitingTime >= 30) {
        lineColor = 'red';
      } else if (messageBody?.waitingTime >= 15) {
        lineColor = 'orange';
      } else if (messageBody?.waitingTime >= 5) {
        lineColor = 'yellow';
      } else if (messageBody?.waitingTime > 0) {
        lineColor = 'black';
      }

      var lineWeight = 3;

      switch (messageBody?.skiLiftState) {
        case 'HALF_STEAM':
          lineWeight = 5;
          break;
        case 'FULL_STEAM':
          lineWeight = 7;
      }

      const polyline = L.polyline(latlngs, {
        color: messageBody?.skiLiftState === 'STOPPED' ? 'red' : lineColor,
        weight: lineWeight,
        dashArray: '30, 10',
        dashOffset: '20',
      }).addTo(this.map);

      const layers: { polyline: L.Polyline; tooltip?: L.Tooltip } = {
        polyline: polyline,
      };

      if (messageBody?.waitingTime >= 0) {
        const tooltip = L.tooltip({
          permanent: true,
          direction: 'right',
          offset: L.point(5, -5),
        })
          .setLatLng(endPoint)
          .setContent(messageBody?.waitingTime.toString() + ' min')
          .addTo(this.map);

        layers.tooltip = tooltip;
      }

      if (lift.id) {
        this.liftLayers.set(lift.id, layers);
      }
    });
  }

  ngOnDestroy(): void {
    this.liftLayers.forEach((layers) => {
      if (layers.polyline) {
        this.map.removeLayer(layers.polyline);
      }
      if (layers.tooltip) {
        this.map.removeLayer(layers.tooltip);
      }
    });
    this.liftLayers.clear();
  }
}
