import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FieldView } from './field-view';

describe('FieldView', () => {
  let component: FieldView;
  let fixture: ComponentFixture<FieldView>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FieldView]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FieldView);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
