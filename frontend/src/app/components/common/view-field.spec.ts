import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewField } from './view-field';

describe('ViewField', () => {
  let component: ViewField;
  let fixture: ComponentFixture<ViewField>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewField],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewField);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
