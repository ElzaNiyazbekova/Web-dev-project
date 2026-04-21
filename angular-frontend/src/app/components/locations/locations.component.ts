// src/app/components/locations/locations.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LocationService } from '../../services/location.service';
import { AuthService } from '../../services/auth.service';
import { Location, Category, TargetGroup } from '../../models/models';

@Component({
  selector: 'app-locations',
  templateUrl: './locations.component.html',
  styleUrls: ['./locations.component.css'],
})
export class LocationsComponent implements OnInit {
  locations: Location[] = [];
  categories: Category[] = [];
  targetGroups: TargetGroup[] = [];

  // [(ngModel)] filter controls - can be empty string, numeric ID string, or number
  filterCategory: any = '';
  filterTargetGroup: any = '';

  loading = false;
  errorMessage = '';

  constructor(
    private locationService: LocationService,
    public auth: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}
  

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.filterCategory = params['category'] || '';
      this.filterTargetGroup = params['target_group'] || '';
      this.loadLocations();
    });
    this.locationService.getCategories().subscribe(cats => this.categories = cats);
    this.locationService.getTargetGroups().subscribe(tgs => this.targetGroups = tgs);
  }

  loadLocations(): void {
    this.loading = true;
    this.errorMessage = '';
    this.locationService.getLocations({
      category: this.filterCategory ? String(this.filterCategory) : undefined,
      target_group: this.filterTargetGroup ? String(this.filterTargetGroup) : undefined,
    }).subscribe({
      next: (data) => { this.locations = data; this.loading = false; },
      error: (err) => {
        this.loading = false;
        this.errorMessage = 'Failed to load locations. Please try again.';
      },
    });
  }

  // (click) event #5 — apply filters
  applyFilters(): void {
    // Update URL with current filter values
    const queryParams: any = {};
    if (this.filterCategory) queryParams.category = this.filterCategory;
    if (this.filterTargetGroup) queryParams.target_group = this.filterTargetGroup;
    this.router.navigate([], { 
      relativeTo: this.route, 
      queryParams,
      queryParamsHandling: 'merge'
    });
    this.loadLocations();
  }

  // (click) event #6 — clear filters
  clearFilters(): void {
    this.filterCategory = '';
    this.filterTargetGroup = '';
    // Update URL to remove filter params
    this.router.navigate([], { 
      relativeTo: this.route,
      queryParams: {}
    });
    this.loadLocations();
  }

  // (click) event #7 — navigate to location detail
  viewLocation(id: number): void {
    this.router.navigate(['/locations', id]);
  }

  getCategoryName(id: number): string {
    return this.categories.find(c => c.id === id)?.name || '';
  }

  getStars(rating?: number): string {
    if (!rating) return '';
    return '★'.repeat(Math.round(rating)) + '☆'.repeat(5 - Math.round(rating));
  }
}
