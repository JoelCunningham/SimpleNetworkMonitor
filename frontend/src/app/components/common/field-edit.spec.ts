import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FieldEdit } from './field-edit';

describe('FieldEdit', () => {
  let component: FieldEdit;
  let fixture: ComponentFixture<FieldEdit>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FieldEdit]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FieldEdit);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
