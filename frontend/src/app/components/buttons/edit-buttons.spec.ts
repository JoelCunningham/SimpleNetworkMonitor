import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewButtons } from '../forms/owner-form/view-buttons';

describe('ViewButtons', () => {
  let component: ViewButtons;
  let fixture: ComponentFixture<ViewButtons>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewButtons],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewButtons);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
