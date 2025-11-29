import { Select } from '#components/common';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('Select', () => {
  let component: Select<any>;
  let fixture: ComponentFixture<Select<any>>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Select],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(Select);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
