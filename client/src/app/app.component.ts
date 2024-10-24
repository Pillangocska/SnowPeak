import { AfterViewInit, Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';
import L, * as Leaflet from 'leaflet';
import { LatLngExpression } from 'leaflet';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, LeafletModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements AfterViewInit {
  title = 'snow-peak-client';

  map: any;

  constructor() {}

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

    const latlngs = [
      new Leaflet.LatLng(46.69539731050563, 13.914595364129971),
      new Leaflet.LatLng(46.693828878676364, 13.92304607372536),
    ] as LatLngExpression[];

    var polyline = L.polyline(latlngs, { color: 'red' }).addTo(this.map);

    var tooltip = L.tooltip({
      permanent: true,
      direction: 'right',
      offset: L.point(5, -5),
    })
      .setLatLng(new Leaflet.LatLng(46.693828878676364, 13.92304607372536))
      .setContent('45min.')
      .addTo(this.map);
  }
}
