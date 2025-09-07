import { Category } from '#interfaces/category';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class CategoryService {
  private apiUrl = 'http://localhost:5000/api/categories';
  private categoriesSubject = new BehaviorSubject<Category[]>([]);

  public categories = this.categoriesSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadCategories();
  }

  private loadCategories(): void {
    this.http.get<Category[]>(this.apiUrl).subscribe((categories) => {
      this.categoriesSubject.next(categories);
    });
  }

  currentCategories(): Observable<Category[]> {
    return this.categories;
  }

  refreshCategories(): void {
    this.loadCategories();
  }
}
