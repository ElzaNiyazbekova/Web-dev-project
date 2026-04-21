// src/app/components/home/home.component.ts
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LocationService } from '../../services/location.service';
import { Location } from '../../models/models';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  recentLocations: Location[] = [];
  searchQuery = '';
  loading = false;

  constructor(
    public auth: AuthService,
    private locationService: LocationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loading = true;
    this.locationService.getLocations().subscribe({
      next: (data) => {
        this.recentLocations = data.slice(0, 6);
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }

  // (click) event #1 — search by city or person's name
  onSearch(): void {
    if (this.searchQuery.trim()) {
      const query = this.searchQuery.trim();
      if (query.includes(' ')) {
        this.router.navigate(['/locations'], {
          queryParams: { created_by: query }
        });
      } else {
        this.router.navigate(['/locations'], {
          queryParams: { city: query }
        });
      }
    }
  }

  // (click) event #2 — view all locations
  goToLocations(): void {
    this.router.navigate(['/locations']);
  }

  getStars(rating?: number): string {
    if (!rating) return '—';
    return '★'.repeat(Math.round(rating)) + '☆'.repeat(5 - Math.round(rating));
  }
}
